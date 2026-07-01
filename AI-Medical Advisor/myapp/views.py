from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import *
from django.contrib.auth import authenticate, logout as auth_logout
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import date as date, datetime as dt
from datetime import datetime, timedelta
from django.db import transaction  
from django.db.models import Q, Sum
from django.utils.timezone import now 
from functools import wraps
from calendar import month_abbr
import random
import re
from django.views.decorators.clickjacking import xframe_options_sameorigin

from .chatbot_service import (
    analyze_care_image,
    build_care_summary,
    build_doctor_handoff_items,
    build_precaution_items,
    classify_message,
    generate_reply,
    get_default_chat_history,
    get_condition_profile,
    get_quick_prompts,
    get_welcome_message,
)

# Create your views here.

# Helper function to get or create user
def get_or_create_user(login_id):
    """Get existing user or create a new one if it doesn't exist"""
    try:
        user = User.objects.get(loginId=login_id)
        return user
    except User.DoesNotExist:
        # Create a default user if it doesn't exist
        login_obj = Login.objects.get(id=login_id)
        user = User.objects.create(
            loginId=login_obj,
            name=login_obj.username,
            email=login_obj.username
        )
        return user


def get_doctor_placeholder(login_obj):
    display_name = getattr(login_obj, "first_name", "") or getattr(login_obj, "username", "")
    return {
        "id": "",
        "name": display_name,
        "email": getattr(login_obj, "username", ""),
        "phone": "",
        "address": "",
        "specialization": "",
        "medical_license_number": "",
        "image": "",
    }


ACTIVE_CHAT_SESSION_KEY = "active_chat_session_id"
DOCTOR_SPECIALTY_ALIASES = {
    "Cardiologist": ["cardiologist", "cardiology", "heart", "palpitations"],
    "General Physician": [
        "general physician",
        "general medicine",
        "general practitioner",
        "family medicine",
        "internal medicine",
        "physician",
    ],
    "Neurologist": ["neurologist", "neurology", "migraine", "headache", "nerve"],
    "Gynecologist": ["gynecologist", "gynaecologist", "gynecology", "gynaecology", "women's health", "period"],
    "ENT": ["ent", "ear nose throat", "sinus", "ear", "throat", "tonsil"],
    "Allergy Specialist": ["allergy", "allergist", "immunology", "immunologist"],
    "Dermatologist": ["dermatologist", "dermatology", "skin"],
    "Gastroenterologist": ["gastroenterologist", "gastro", "digestive", "stomach"],
    "Pulmonologist": ["pulmonologist", "pulmonary", "respiratory", "lung", "chest"],
    "Ophthalmologist": [
        "ophthalmologist",
        "opthalmologist",
        "ophthalmology",
        "eye",
        "eyes",
        "eye specialist",
        "vision",
        "eye pain",
        "red eye",
        "red eyes",
        "dry eye",
        "blurry vision",
    ],
    "Emergency Care": ["emergency", "critical care", "trauma"],
    "Mental Health Specialist": [
        "mental health",
        "psychiatrist",
        "psychologist",
        "psychotherapy",
        "counselor",
        "therapy",
    ],
    "Orthopedic Specialist": ["orthopedic", "orthopaedic", "bone", "joint", "spine"],
}


def _set_active_chat_session_id(request, chat_session_id):
    request.session[ACTIVE_CHAT_SESSION_KEY] = chat_session_id
    request.session.modified = True


def _create_chat_session(user):
    chat_session = CareChatSession.objects.create(
        user=user,
        title="Care chat",
        symptom_summary="No user details provided yet.",
    )
    CareChatMessage.objects.create(
        session=chat_session,
        role="assistant",
        text=get_welcome_message(),
    )
    return chat_session


def _build_chat_history(chat_session):
    history = [
        {
            "role": message.role,
            "text": message.text,
            "sender_name": getattr(message.sender_doctor, "name", "") if message.role == "doctor" else "",
            "is_read_by_patient": bool(message.patient_read_at) if message.role == "doctor" else True,
        }
        for message in CareChatMessage.objects.filter(session=chat_session).select_related("sender_doctor").order_by("created_at", "id")
    ]
    return history or get_default_chat_history()


def _is_ajax_request(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def _update_chat_session_summary(chat_session):
    summary = _session_care_summary(chat_session)
    chat_session.title = summary["title"]
    chat_session.symptom_summary = summary["summary"]
    chat_session.structured_symptoms = summary["symptoms_display"]
    chat_session.primary_intent = summary["primary_intent"]
    chat_session.recommended_specialty = summary["recommended_specialty"]
    chat_session.urgency_level = summary["urgency_level"]
    chat_session.last_user_message = summary["last_user_message"]
    chat_session.save()
    return summary


def _session_care_summary(chat_session):
    user_messages = list(
        chat_session.messages.filter(role="user").values_list("text", flat=True)
    )
    return build_care_summary(user_messages)


def _mark_doctor_messages_as_read(chat_session):
    CareChatMessage.objects.filter(
        session=chat_session,
        role="doctor",
        patient_read_at__isnull=True,
    ).update(patient_read_at=now())


def _get_active_chat_session(request, user):
    chat_session_id = request.session.get(ACTIVE_CHAT_SESSION_KEY)
    chat_session = None

    if chat_session_id:
        chat_session = (
            CareChatSession.objects.filter(id=chat_session_id, user=user)
            .prefetch_related("messages")
            .first()
        )
        if chat_session and not chat_session.is_active:
            chat_session = None

    if chat_session is None:
        chat_session = (
            CareChatSession.objects.filter(user=user, is_active=True)
            .prefetch_related("messages")
            .first()
        )

    if chat_session is None:
        chat_session = _create_chat_session(user)
        chat_session = (
            CareChatSession.objects.filter(id=chat_session.id)
            .prefetch_related("messages")
            .get()
        )

    _set_active_chat_session_id(request, chat_session.id)
    return chat_session


def _close_chat_session(chat_session):
    if chat_session.is_active:
        chat_session.is_active = False
        chat_session.save(update_fields=["is_active", "updated_at"])


def _get_latest_patient_chat(user):
    return (
        CareChatSession.objects.filter(user=user)
        .exclude(last_user_message="")
        .order_by("-updated_at", "-id")
        .first()
    )


def _get_requested_chat_session(request, user):
    selected_chat_id = request.GET.get("chat_session_id") or request.POST.get("chat_session_id")
    if selected_chat_id:
        selected_session = CareChatSession.objects.filter(
            id=selected_chat_id,
            user=user,
        ).first()
        if selected_session:
            _set_active_chat_session_id(request, selected_session.id)
            return selected_session
    return _get_active_chat_session(request, user)


def _normalize_specialty(value):
    return " ".join((value or "").strip().lower().split())


def _specialty_keywords(recommended_specialty, symptoms_text=""):
    normalized_specialty = _normalize_specialty(recommended_specialty)
    keywords = set()

    if normalized_specialty:
        keywords.add(normalized_specialty)

    for label, aliases in DOCTOR_SPECIALTY_ALIASES.items():
        candidate_values = {_normalize_specialty(label)}
        candidate_values.update(_normalize_specialty(alias) for alias in aliases)
        if normalized_specialty in candidate_values or any(
            normalized_specialty and (
                normalized_specialty in candidate or candidate in normalized_specialty
            )
            for candidate in candidate_values
        ):
            keywords.update(candidate_values)

    for symptom in (symptoms_text or "").split(","):
        normalized_symptom = _normalize_specialty(symptom)
        if normalized_symptom:
            keywords.add(normalized_symptom)

    return [keyword for keyword in keywords if keyword]


def _doctor_match_score(doctor, recommended_specialty="", symptoms_text=""):
    specialization = _normalize_specialty(getattr(doctor, "specialization", ""))
    if not specialization:
        return 0

    normalized_specialty = _normalize_specialty(recommended_specialty)
    score = 0

    if normalized_specialty and specialization == normalized_specialty:
        score += 120

    for keyword in _specialty_keywords(recommended_specialty, symptoms_text):
        if keyword == specialization:
            score += 90
        elif keyword in specialization:
            score += 28

    if normalized_specialty and normalized_specialty in specialization:
        score += 24

    if normalized_specialty == "general physician" and "general" in specialization:
        score += 16

    return score


def _has_doctor_recommendation_signal(recommended_specialty="", symptoms_text=""):
    normalized_specialty = _normalize_specialty(recommended_specialty)
    normalized_symptoms = _normalize_specialty(symptoms_text)

    if normalized_symptoms and normalized_symptoms != "no clear symptom markers yet":
        return True

    return bool(normalized_specialty and normalized_specialty != "general physician")


def _recommended_doctors_for_chat(recommended_specialty="", symptoms_text="", limit=4):
    if not _has_doctor_recommendation_signal(recommended_specialty, symptoms_text):
        return [], False

    doctors = list(
        Doctor.objects.filter(loginId__is_active=True)
        .select_related("loginId")
        .order_by("name")
    )
    ranked_doctors = []

    for doctor in doctors:
        score = _doctor_match_score(doctor, recommended_specialty, symptoms_text)
        if score <= 0:
            continue
        doctor.match_score = score
        doctor.match_reason = recommended_specialty or "Suggested by symptom match"
        ranked_doctors.append(doctor)

    ranked_doctors.sort(key=lambda doctor: (-doctor.match_score, doctor.name.lower()))

    if ranked_doctors:
        return ranked_doctors[:limit], True

    return [], False


def _build_doctor_note(recommended_doctors, has_specialty_match, recommended_specialty=""):
    if not recommended_doctors:
        if recommended_specialty:
            return f"I would usually suggest booking a {recommended_specialty}, but I could not find a matching doctor in the current list."
        return "I could not find a specific doctor match from the current message yet."

    top_doctor = recommended_doctors[0]
    if has_specialty_match:
        return (
            f"The best doctor match available here is {top_doctor.name}, "
            f"{top_doctor.specialization}, located in {top_doctor.address}."
        )

    return (
        f"I could not find an exact specialty match, but {top_doctor.name} "
        f"is available as a nearby next option."
    )


def _doctor_summary_text(chat_session, care_summary=None):
    override_text = (getattr(chat_session, "doctor_summary_override", "") or "").strip()
    if override_text:
        return override_text

    generated_summary = (chat_session.symptom_summary or "").strip()
    if generated_summary:
        return generated_summary

    return ((care_summary or {}).get("summary") or "").strip()


def _chat_session_medicine_guidance(chat_session, care_summary=None):
    if not chat_session:
        return ""
    summary = care_summary or _session_care_summary(chat_session)
    return (summary.get("medicine_guidance") or "").strip()


def _latest_relevant_chat_session_for_user(user, doctor=None):
    if not user:
        return None

    base_qs = CareChatSession.objects.filter(user=user).exclude(last_user_message="")

    if doctor:
        appointment_chat_ids = Appointments.objects.filter(
            uid=user,
            did=doctor,
        ).exclude(chat_session=None).values_list("chat_session_id", flat=True)
        matched_session = (
            base_qs.filter(Q(linked_doctor=doctor) | Q(id__in=appointment_chat_ids))
            .order_by("-updated_at", "-id")
            .first()
        )
        if matched_session:
            return matched_session

    return base_qs.order_by("-updated_at", "-id").first()


def _latest_user_ai_medicine_support(user, doctor=None):
    chat_session = _latest_relevant_chat_session_for_user(user, doctor)
    return _chat_session_medicine_guidance(chat_session) if chat_session else ""


def _reset_doctor_approvals(chat_session, summary=True, medicine=True):
    fields_to_update = []

    if summary and chat_session.doctor_approved_summary:
        chat_session.doctor_approved_summary = False
        fields_to_update.append("doctor_approved_summary")

    if medicine and chat_session.doctor_approved_medicine:
        chat_session.doctor_approved_medicine = False
        fields_to_update.append("doctor_approved_medicine")

    if fields_to_update:
        fields_to_update.append("updated_at")
        chat_session.save(update_fields=fields_to_update)


def _clean_reply_sentence(text):
    cleaned = " ".join((text or "").strip().split())
    if not cleaned:
        return ""
    if cleaned.endswith((".", "!", "?")):
        return cleaned
    return f"{cleaned}."


def _medicine_guidance_line(care_summary):
    guidance = _clean_reply_sentence(care_summary.get("medicine_guidance", ""))
    if not guidance:
        return ""
    return _pick_chat_variant(
        f"Medicine support to ask your doctor about: {guidance}",
        f"Possible medicines to discuss with your doctor: {guidance}",
    )


def _book_appointment_url(chat_session_id, doctor=None):
    url = f"/book_appoinment?chat_session_id={chat_session_id}"
    if doctor and getattr(doctor, "id", None):
        url = f"{url}&doctor_id={doctor.id}"
    return url


def _care_report_url(chat_session_id):
    return f"/care-report/?chat_session_id={chat_session_id}"


def _serialize_chat_doctor(doctor, chat_session_id):
    return {
        "id": doctor.id,
        "name": doctor.name,
        "specialization": doctor.specialization or "General Care",
        "address": doctor.address or "",
        "match_reason": getattr(doctor, "match_reason", "Suggested doctor"),
        "booking_url": _book_appointment_url(chat_session_id, doctor),
    }


def _build_chat_view_payload(chat_session):
    care_summary = _update_chat_session_summary(chat_session)
    recommended_doctors, has_specialty_match = _recommended_doctors_for_chat(
        care_summary["recommended_specialty"],
        care_summary["symptoms_display"],
    )
    top_recommended_doctor = recommended_doctors[0] if recommended_doctors else None
    precaution_doctor = chat_session.linked_doctor or top_recommended_doctor
    condition_profile = get_condition_profile(care_summary)
    precautions = build_precaution_items(
        care_summary,
        chat_session.visual_analysis_summary,
        getattr(precaution_doctor, "specialization", ""),
        getattr(precaution_doctor, "name", ""),
    )
    doctor_handoff = build_doctor_handoff_items(
        care_summary,
        top_doctor_name=(
            f"{top_recommended_doctor.name} - {top_recommended_doctor.specialization}"
            if top_recommended_doctor
            else ""
        ),
        visual_analysis_label=chat_session.visual_analysis_label,
        visual_analysis_summary=chat_session.visual_analysis_summary,
    )
    doctor_note = _build_doctor_note(
        recommended_doctors,
        has_specialty_match,
        care_summary.get("recommended_specialty", ""),
    )
    doctor_summary_text = _doctor_summary_text(chat_session, care_summary)
    medicine_guidance_text = _chat_session_medicine_guidance(chat_session, care_summary)

    return {
        "chat_history": _build_chat_history(chat_session),
        "chat_prompts": get_quick_prompts(),
        "care_summary": care_summary,
        "active_chat_session_id": chat_session.id,
        "recommended_doctors": [
            _serialize_chat_doctor(doctor, chat_session.id) for doctor in recommended_doctors
        ],
        "has_specialty_match": has_specialty_match,
        "top_recommended_doctor": (
            _serialize_chat_doctor(top_recommended_doctor, chat_session.id)
            if top_recommended_doctor
            else None
        ),
        "condition_profile": condition_profile,
        "precautions": precautions,
        "doctor_handoff": doctor_handoff,
        "doctor_summary_text": doctor_summary_text,
        "medicine_guidance_text": medicine_guidance_text,
        "doctor_approved_summary": bool(chat_session.doctor_approved_summary),
        "doctor_approved_medicine": bool(chat_session.doctor_approved_medicine),
        "doctor_section_note": doctor_note,
        "summary_booking_url": _book_appointment_url(chat_session.id, top_recommended_doctor),
        "care_report_url": _care_report_url(chat_session.id),
        "visual_analysis_label": chat_session.visual_analysis_label,
        "visual_analysis_summary": chat_session.visual_analysis_summary,
        "visual_analysis_details": chat_session.visual_analysis_details,
        "care_image_url": chat_session.care_image.url if chat_session.care_image else "",
    }


def _build_care_report_payload(chat_session):
    care_summary = _update_chat_session_summary(chat_session)
    recommended_doctors, has_specialty_match = _recommended_doctors_for_chat(
        care_summary["recommended_specialty"],
        care_summary["symptoms_display"],
    )
    top_recommended_doctor = recommended_doctors[0] if recommended_doctors else None
    precaution_doctor = chat_session.linked_doctor or top_recommended_doctor
    condition_profile = get_condition_profile(care_summary)
    precautions = build_precaution_items(
        care_summary,
        chat_session.visual_analysis_summary,
        getattr(precaution_doctor, "specialization", ""),
        getattr(precaution_doctor, "name", ""),
    )
    doctor_handoff = build_doctor_handoff_items(
        care_summary,
        top_doctor_name=(
            f"{top_recommended_doctor.name} - {top_recommended_doctor.specialization}"
            if top_recommended_doctor
            else ""
        ),
        visual_analysis_label=chat_session.visual_analysis_label,
        visual_analysis_summary=chat_session.visual_analysis_summary,
    )
    doctor_summary_text = _doctor_summary_text(chat_session, care_summary)
    medicine_guidance_text = _chat_session_medicine_guidance(chat_session, care_summary)
    return {
        "care_summary": care_summary,
        "condition_profile": condition_profile,
        "top_recommended_doctor": top_recommended_doctor,
        "recommended_doctors": recommended_doctors,
        "has_specialty_match": has_specialty_match,
        "precautions": precautions,
        "doctor_handoff": doctor_handoff,
        "doctor_summary_text": doctor_summary_text,
        "medicine_guidance_text": medicine_guidance_text,
        "doctor_approved_summary": bool(chat_session.doctor_approved_summary),
        "doctor_approved_medicine": bool(chat_session.doctor_approved_medicine),
        "summary_booking_url": _book_appointment_url(chat_session.id, top_recommended_doctor),
        "care_report_url": _care_report_url(chat_session.id),
        "visual_analysis_label": chat_session.visual_analysis_label,
        "visual_analysis_summary": chat_session.visual_analysis_summary,
        "visual_analysis_details": chat_session.visual_analysis_details,
        "care_image_url": chat_session.care_image.url if chat_session.care_image else "",
    }


def _recommended_doctor_for_session(chat_session):
    if getattr(chat_session, "linked_doctor", None):
        return chat_session.linked_doctor

    care_summary = _update_chat_session_summary(chat_session)
    recommended_doctors, _has_specialty_match = _recommended_doctors_for_chat(
        care_summary.get("recommended_specialty", ""),
        care_summary.get("symptoms_display", ""),
    )
    return recommended_doctors[0] if recommended_doctors else None


def _doctor_accessible_chat_session(doctor, chat_session_id):
    if not doctor or not chat_session_id:
        return None

    appointment_chat_ids = Appointments.objects.filter(did=doctor).exclude(chat_session=None).values_list("chat_session_id", flat=True)
    return (
        CareChatSession.objects.filter(id=chat_session_id)
        .filter(Q(linked_doctor=doctor) | Q(id__in=appointment_chat_ids))
        .first()
    )


def _latest_doctor_reply(chat_session):
    return (
        chat_session.messages.filter(role="doctor")
        .select_related("sender_doctor")
        .order_by("-created_at", "-id")
        .first()
    )


def _doctor_intake_records(doctor):
    appointments = list(
        Appointments.objects.filter(did=doctor)
        .exclude(chat_session=None)
        .select_related("uid", "did", "chat_session")
        .order_by("-date", "-time")
    )
    appointment_chat_ids = [appointment.chat_session_id for appointment in appointments if appointment.chat_session_id]
    direct_sessions = list(
        CareChatSession.objects.filter(linked_doctor=doctor)
        .exclude(id__in=appointment_chat_ids)
        .select_related("user", "linked_doctor")
        .order_by("-updated_at", "-id")
    )

    records = []
    for appointment in appointments:
        care_summary = _session_care_summary(appointment.chat_session)
        latest_reply = _latest_doctor_reply(appointment.chat_session)
        records.append(
            {
                "kind": "appointment",
                "patient": appointment.uid,
                "chat_session": appointment.chat_session,
                "doctor": appointment.did,
                "appointment": appointment,
                "status_label": appointment.status or "Booked",
                "submitted_at": dt.combine(appointment.date, appointment.time) if appointment.date and appointment.time else appointment.chat_session.updated_at,
                "latest_doctor_reply": latest_reply,
                "medicine_guidance_text": care_summary.get("medicine_guidance", ""),
                "doctor_approved_summary": bool(appointment.chat_session.doctor_approved_summary),
                "doctor_approved_medicine": bool(appointment.chat_session.doctor_approved_medicine),
                "reply_status": (
                    "Unread by patient"
                    if latest_reply and not latest_reply.patient_read_at
                    else ("Read by patient" if latest_reply else "No doctor reply yet")
                ),
            }
        )

    for chat_session in direct_sessions:
        care_summary = _session_care_summary(chat_session)
        latest_reply = _latest_doctor_reply(chat_session)
        records.append(
            {
                "kind": "direct",
                "patient": chat_session.user,
                "chat_session": chat_session,
                "doctor": doctor,
                "appointment": None,
                "status_label": "Direct care chat",
                "submitted_at": chat_session.updated_at,
                "latest_doctor_reply": latest_reply,
                "medicine_guidance_text": care_summary.get("medicine_guidance", ""),
                "doctor_approved_summary": bool(chat_session.doctor_approved_summary),
                "doctor_approved_medicine": bool(chat_session.doctor_approved_medicine),
                "reply_status": (
                    "Unread by patient"
                    if latest_reply and not latest_reply.patient_read_at
                    else ("Read by patient" if latest_reply else "No doctor reply yet")
                ),
            }
        )

    records.sort(key=lambda record: record["submitted_at"] or dt.min, reverse=True)
    return records


def _format_chat_list(values):
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return f"{', '.join(cleaned[:-1])}, and {cleaned[-1]}"


def _pick_chat_variant(*options):
    choices = [option for option in options if option]
    if not choices:
        return ""
    return random.choice(choices)


def _chat_signal_text(care_summary):
    symptoms_display = care_summary.get("symptoms_display", "").strip()
    if symptoms_display and symptoms_display != "No clear symptom markers yet":
        return symptoms_display

    if care_summary.get("symptoms"):
        return _format_chat_list(care_summary["symptoms"])

    return ""


def _doctor_recommendation_line(recommended_doctors, has_specialty_match, recommended_specialty=""):
    if not recommended_doctors:
        if recommended_specialty:
            return f"I would usually suggest a {recommended_specialty}, but I could not find one in the current doctor list."
        return ""

    top_doctor = recommended_doctors[0]
    location_text = f" in {top_doctor.address}" if getattr(top_doctor, "address", "") else ""
    if has_specialty_match:
        return _pick_chat_variant(
            f"Best match: {top_doctor.name} ({top_doctor.specialization}){location_text}.",
            f"The closest fit I found is {top_doctor.name} ({top_doctor.specialization}){location_text}.",
            f"You could start with {top_doctor.name} ({top_doctor.specialization}){location_text}.",
        )

    return _pick_chat_variant(
        f"Closest available doctor: {top_doctor.name}{location_text}.",
        f"The nearest available option I found is {top_doctor.name}{location_text}.",
        f"A practical next option is {top_doctor.name}{location_text}.",
    )


def _brief_condition_overview(care_summary):
    overview = (care_summary.get("condition_overview") or "").strip()
    if not overview:
        return ""
    first_sentence = re.split(r"(?<=[.!?])\s+", overview)[0].strip()
    return first_sentence[:180].rstrip(", ")


def _health_opening_line(care_summary):
    signal_text = _chat_signal_text(care_summary)
    condition_name = care_summary.get("condition_name", "a health concern")
    duration_text = care_summary.get("duration_text", "")
    if signal_text:
        timing_text = f" {duration_text}" if duration_text else ""
        return _pick_chat_variant(
            f"From your message, this sounds closer to {condition_name} with {signal_text}{timing_text}.",
            f"What you described points more to {condition_name}, mainly because of {signal_text}{timing_text}.",
            f"This reads more like {condition_name} given the {signal_text}{timing_text}.",
        )

    return _pick_chat_variant(
        f"From your message, this looks more like {condition_name}.",
        f"This seems closer to {condition_name}.",
        f"What you described fits better with {condition_name}.",
    )


def _message_tokens(message_text):
    return set(re.findall(r"[a-z0-9]+", (message_text or "").lower()))


def _message_requests_doctor(message_text):
    normalized = " ".join((message_text or "").lower().split())
    doctor_phrases = (
        "which doctor",
        "what doctor",
        "who should i see",
        "who should i consult",
        "which specialist",
        "what specialist",
        "recommend doctor",
    )
    if any(phrase in normalized for phrase in doctor_phrases):
        return True

    tokens = _message_tokens(message_text)
    return "doctor" in tokens or "specialist" in tokens


def _message_requests_precautions(message_text):
    normalized = " ".join((message_text or "").lower().split())
    precaution_phrases = (
        "what should i do",
        "what can i do",
        "what precautions",
        "warning signs",
        "what should i watch",
        "how do i manage",
        "how to manage",
        "what now",
        "is it serious",
    )
    if any(phrase in normalized for phrase in precaution_phrases):
        return True

    tokens = _message_tokens(message_text)
    return bool(tokens.intersection({"precaution", "precautions", "warning", "warnings", "manage", "care"}))


def _message_requests_condition_details(message_text):
    normalized = " ".join((message_text or "").lower().split())
    condition_phrases = (
        "what disease",
        "which disease",
        "what condition",
        "what is this",
        "what could this be",
        "what problem is this",
        "why is this happening",
        "what is happening",
        "tell me about this condition",
    )
    if any(phrase in normalized for phrase in condition_phrases):
        return True

    tokens = _message_tokens(message_text)
    return bool(tokens.intersection({"disease", "condition", "cause", "causing", "problem"}))


def _message_is_portal_help_request(message_text, latest_intent):
    if latest_intent in {"greeting", "thanks", "goodbye", "prescription_help", "order_payment_help"}:
        return True

    tokens = _message_tokens(message_text)
    return bool(tokens.intersection({"prescription", "prescriptions", "rx", "order", "orders", "invoice", "payment", "cart"}))


def _message_is_medicine_help_request(message_text, latest_intent):
    if latest_intent in {"medicine_info", "dosage_guidance", "medication_side_effects"}:
        return True

    normalized = " ".join((message_text or "").lower().split())
    if "side effect" in normalized:
        return True

    tokens = _message_tokens(message_text)
    return bool(tokens.intersection({"medicine", "medicines", "tablet", "tablets", "capsule", "capsules", "dosage", "dose"}))


def _message_is_acknowledgement(message_text):
    normalized = " ".join((message_text or "").lower().split())
    if not normalized:
        return False

    acknowledgement_phrases = {
        "ok",
        "okay",
        "k",
        "kk",
        "fine",
        "alright",
        "all right",
        "sure",
        "got it",
        "understood",
        "noted",
        "i see",
        "cool",
    }
    if normalized in acknowledgement_phrases:
        return True

    tokens = _message_tokens(message_text)
    return bool(tokens) and tokens.issubset({"ok", "okay", "fine", "sure", "got", "it", "understood", "noted", "cool"})


def _acknowledgement_reply(care_summary, recommended_doctors, has_specialty_match):
    has_health_signal = bool(
        care_summary
        and (
            care_summary.get("symptoms")
            or care_summary.get("specialty_hints")
            or care_summary.get("condition_name") != "General health concern"
        )
    )

    if not has_health_signal:
        return _pick_chat_variant(
            "Okay. Tell me the main symptom, where it is, and how long it has been happening, and I will guide you better.",
            "Okay. Share the symptom, when it started, and how strong it feels, and I can help more clearly.",
            "Alright. Tell me what problem you are having and how long it has been going on, and I will narrow it down.",
        )

    clarification_prompt = (care_summary.get("focus_clarification_prompt") or "").strip()
    if clarification_prompt:
        return _pick_chat_variant(
            f"Okay. {clarification_prompt}",
            f"Alright. {clarification_prompt}",
            f"Sure. {clarification_prompt}",
        )

    condition_name = care_summary.get("condition_name", "this concern").lower()
    doctor_line = _doctor_recommendation_line(
        recommended_doctors,
        has_specialty_match,
        care_summary.get("recommended_specialty", ""),
    )

    reply = _pick_chat_variant(
        f"Okay. I am tracking this as {condition_name}. If you want, ask about precautions, medicines, or the right doctor.",
        f"Alright. This still looks closer to {condition_name}. If you want, I can explain precautions, medicines, or doctor choice.",
        f"Okay. I am following this as {condition_name}. You can ask about precautions, medicines, or which doctor fits best.",
    )

    if doctor_line:
        reply = f"{reply} {doctor_line}"

    return reply.strip()


def _follow_up_closing(care_summary, recommended_doctors, has_specialty_match):
    closing_parts = []

    clarification_prompt = (care_summary.get("focus_clarification_prompt") or "").strip()
    if clarification_prompt:
        return clarification_prompt

    if care_summary.get("urgency_level") == "high":
        closing_parts.append(
            _pick_chat_variant(
                f"Get urgent care if you notice {care_summary.get('red_flags', '')}.",
                f"Please seek urgent care if you develop {care_summary.get('red_flags', '')}.",
            )
        )
    elif care_summary.get("red_flags"):
        closing_parts.append(
            _pick_chat_variant(
                f"Watch for warning signs like {care_summary.get('red_flags', '')}.",
                f"Keep an eye out for {care_summary.get('red_flags', '')}.",
            )
        )

    doctor_line = _doctor_recommendation_line(
        recommended_doctors,
        has_specialty_match,
        care_summary.get("recommended_specialty", ""),
    )
    if doctor_line:
        closing_parts.append(doctor_line)
    elif care_summary.get("follow_up_prompt"):
        closing_parts.append(care_summary["follow_up_prompt"])

    return " ".join(part.strip() for part in closing_parts if part).strip()


def _compose_chat_assistant_reply(message_text, care_summary, recommended_doctors, has_specialty_match):
    base_reply = generate_reply(message_text)
    if care_summary["urgency_level"] == "emergency":
        return base_reply

    latest_summary = build_care_summary([message_text])
    latest_intent = latest_summary.get("primary_intent", "")
    latest_has_health_signal = bool(
        latest_summary.get("symptoms")
        or latest_summary.get("specialty_hints")
        or latest_summary.get("condition_name") != "General health concern"
    )
    response_summary = latest_summary if latest_has_health_signal else care_summary
    response_doctors = recommended_doctors
    response_has_specialty_match = has_specialty_match
    if latest_has_health_signal:
        latest_doctors, latest_has_match = _recommended_doctors_for_chat(
            response_summary.get("recommended_specialty", ""),
            response_summary.get("symptoms_display", ""),
        )
        if latest_doctors:
            response_doctors = latest_doctors
            response_has_specialty_match = latest_has_match

    if _message_is_acknowledgement(message_text):
        return _acknowledgement_reply(
            response_summary,
            response_doctors,
            response_has_specialty_match,
        )

    has_health_signal = bool(
        care_summary.get("symptoms")
        or care_summary.get("specialty_hints")
        or care_summary.get("condition_name") != "General health concern"
    )
    if not has_health_signal:
        return base_reply

    if _message_is_portal_help_request(message_text, latest_intent):
        return base_reply

    if _message_is_medicine_help_request(message_text, latest_intent) and not latest_has_health_signal:
        return base_reply

    if _message_is_medicine_help_request(message_text, latest_intent) and latest_has_health_signal:
        parts = [_health_opening_line(response_summary)]
        medicine_line = _medicine_guidance_line(response_summary)
        if medicine_line:
            parts.append(medicine_line)
        closing = _follow_up_closing(response_summary, response_doctors, response_has_specialty_match)
        if closing:
            parts.append(closing)
        return "\n\n".join(part.strip() for part in parts if part).strip() or base_reply

    if response_summary.get("focus_clarification_prompt"):
        return "\n\n".join(
            [
                _pick_chat_variant(
                    "This sounds more like an ENT concern.",
                    f"This seems closer to {response_summary.get('condition_name', 'an ENT concern')}.",
                ),
                response_summary["focus_clarification_prompt"],
            ]
        ).strip()

    if _message_requests_doctor(message_text):
        parts = [
            _pick_chat_variant(
                f"This sounds more like {response_summary.get('condition_name', 'a health concern')}.",
                f"I would place this closer to {response_summary.get('condition_name', 'a health concern')}.",
            )
        ]
        doctor_line = _doctor_recommendation_line(
            response_doctors,
            response_has_specialty_match,
            response_summary.get("recommended_specialty", ""),
        )
        if doctor_line:
            parts.append(doctor_line)
        elif response_summary.get("recommended_specialty") == "General Physician":
            parts.append(
                _pick_chat_variant(
                    "A General Physician is the best first doctor to review this.",
                    "A General Physician would be the best first step for this.",
                )
            )
        elif response_summary.get("recommended_specialty"):
            parts.append(
                _pick_chat_variant(
                    f"A {response_summary.get('recommended_specialty')} is the best fit to review this.",
                    f"I would start with a {response_summary.get('recommended_specialty')} for this.",
                )
            )

        if not doctor_line and response_summary.get("follow_up_prompt"):
            parts.append(response_summary["follow_up_prompt"])
        return "\n\n".join(part.strip() for part in parts if part).strip()

    if _message_requests_precautions(message_text):
        parts = []
        if response_summary.get("care_tips"):
            parts.append(
                _pick_chat_variant(
                    f"For now, {response_summary.get('care_tips')}.",
                    f"For now, you can {response_summary.get('care_tips')}.",
                    f"For now, try to {response_summary.get('care_tips')}.",
                )
            )
        closing = _follow_up_closing(response_summary, response_doctors, response_has_specialty_match)
        if closing:
            parts.append(closing)
        return "\n\n".join(part.strip() for part in parts if part).strip() or base_reply

    if _message_requests_condition_details(message_text):
        parts = [_health_opening_line(response_summary)]
        overview = _brief_condition_overview(response_summary)
        if overview:
            parts.append(overview)
        doctor_line = _doctor_recommendation_line(
            response_doctors,
            response_has_specialty_match,
            response_summary.get("recommended_specialty", ""),
        )
        if doctor_line:
            parts.append(doctor_line)
        return "\n\n".join(part.strip() for part in parts if part).strip()

    if not latest_has_health_signal:
        return base_reply

    parts = [_health_opening_line(response_summary)]

    care_tips = response_summary.get("care_tips", "")
    if care_tips:
        parts.append(
            _pick_chat_variant(
                f"For now, {care_tips}.",
                f"For now, you can {care_tips}.",
                f"For now, try to {care_tips}.",
            )
        )

    medicine_line = _medicine_guidance_line(response_summary)
    if medicine_line:
        parts.append(medicine_line)

    closing = _follow_up_closing(response_summary, response_doctors, response_has_specialty_match)
    if closing:
        parts.append(closing)

    return "\n\n".join(part.strip() for part in parts if part).strip()

def index(request):
    return render(request, "index.html")



def is_admin_user(user):
    if not user:
        return False
    usertype = str(getattr(user, "usertype", "")).lower()
    return user.is_superuser or user.is_staff or usertype == "admin"


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        uid = request.session.get('uid')
        if not uid:
            return redirect('/adminpage/')
        try:
            admin_user = Login.objects.get(id=uid)
        except Login.DoesNotExist:
            return redirect('/adminpage/')
        if not is_admin_user(admin_user):
            return redirect('/adminpage/')
        return view_func(request, *args, **kwargs)
    return _wrapped

def shift_month(year, month, delta):
    new_month = month + delta
    new_year = year + (new_month - 1) // 12
    new_month = (new_month - 1) % 12 + 1
    return new_year, new_month

def get_financial_context():
    orders = MedicineOrder.objects.filter(status="Paid")
    totals = orders.aggregate(total_sales=Sum("total"), total_profit=Sum("profit"))
    total_sales = totals["total_sales"] or 0
    total_profit = totals["total_profit"] or 0
    order_count = orders.count()
    avg_order = (total_sales / order_count) if order_count else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0
    profit_margin = max(0, min(100, profit_margin))

    today = now().date()
    months = []
    for i in range(5, -1, -1):
        y, m = shift_month(today.year, today.month, -i)
        label = f"{month_abbr[m]} {y}"
        months.append((y, m, label))

    monthly = {(y, m): {"sales": 0, "profit": 0} for y, m, _ in months}
    for order in orders:
        key = (order.date.year, order.date.month)
        if key in monthly:
            monthly[key]["sales"] += order.total or 0
            monthly[key]["profit"] += order.profit or 0

    sales_values = [monthly[(y, m)]["sales"] for y, m, _ in months]
    profit_values = [monthly[(y, m)]["profit"] for y, m, _ in months]
    max_sales = max(sales_values) if sales_values else 1
    max_profit = max(profit_values) if profit_values else 1

    chart_data = []
    for (y, m, label), sales, profit in zip(months, sales_values, profit_values):
        chart_data.append({
            "label": label,
            "sales": sales,
            "profit": profit,
            "sales_pct": round((sales / max_sales) * 100, 2) if max_sales else 0,
            "profit_pct": round((profit / max_profit) * 100, 2) if max_profit else 0,
        })

    return {
        "total_sales": total_sales,
        "total_profit": total_profit,
        "order_count": order_count,
        "avg_order": avg_order,
        "profit_margin": round(profit_margin, 1),
        "chart_data": chart_data,
    }

def get_place_options(queryset, field_name="address"):
    seen = {}
    for value in queryset.values_list(field_name, flat=True):
        if value:
            cleaned = str(value).strip()
            if not cleaned:
                continue
            place = cleaned.split(",")[0].strip()
            if not place:
                continue
            key = place.lower()
            if key not in seen:
                seen[key] = place
    return sorted(seen.values(), key=lambda v: v.lower())

def get_medicine_place_options(queryset):
    pharmacist_ids = queryset.values_list("pid_id", flat=True).distinct()
    return get_place_options(Pharmacist.objects.filter(id__in=pharmacist_ids))

def apply_medicine_filters(request, queryset):
    q = request.GET.get("q", "").strip()
    place = request.GET.get("place", "").strip()
    stock = request.GET.get("stock", "").strip()
    expiry = request.GET.get("expiry", "").strip()
    sort = request.GET.get("sort", "").strip()

    if q:
        queryset = queryset.filter(
            Q(name__icontains=q)
            | Q(desc__icontains=q)
            | Q(side_effects__icontains=q)
        )

    if place:
        queryset = queryset.filter(pid__address__icontains=place)

    if stock == "in":
        queryset = queryset.filter(qty__gt=0)
    elif stock == "low":
        queryset = queryset.filter(qty__gt=0, qty__lte=10)
    elif stock == "out":
        queryset = queryset.filter(qty__lte=0)

    today = now().date()
    if expiry == "valid":
        queryset = queryset.filter(expiry__gte=today)
    elif expiry == "expired":
        queryset = queryset.filter(expiry__lt=today)
    elif expiry == "soon":
        queryset = queryset.filter(expiry__gte=today, expiry__lte=today + timedelta(days=30))

    if sort == "name_asc":
        queryset = queryset.order_by("name")
    elif sort == "price_asc":
        queryset = queryset.order_by("price")
    elif sort == "price_desc":
        queryset = queryset.order_by("-price")
    elif sort == "expiry_asc":
        queryset = queryset.order_by("expiry")
    elif sort == "expiry_desc":
        queryset = queryset.order_by("-expiry")

    return queryset, {"q": q, "place": place, "stock": stock, "expiry": expiry, "sort": sort}
def admin_portal(request):
    return render(request, "admin_portal.html")






#Login--
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email,password=password)
        if user is not None:
            if is_admin_user(user):
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical')
                return redirect('/adminHome')
            elif user.usertype == 'User':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical')
                return redirect('/userHome')
            elif user.usertype == 'Doctor':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical ')
                return redirect('/doctorHome')
            elif user.usertype == 'Pharmacist':
                request.session['uid'] = user.id
                messages.success(request, 'Welcome to Medical')
                return redirect('/pharmaHome')
            else:
                messages.info(request, "type Not Defined")

        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'login.html')


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None and is_admin_user(user):
            request.session['uid'] = user.id
            messages.success(request, 'Welcome to Medical Advisor')
            return redirect('/adminHome')
        messages.error(request, "Admin credentials required")
    return render(request, "admin_login.html")


def logout_view(request):
    auth_logout(request)
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('/')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Login.objects.filter(username=email).exists():
            messages.success(request, "If this email is registered, a reset link has been sent.")
        else:
            messages.error(request, "No account found with that email.")
        return redirect("/forgot-password/")
    return render(request, "forgot_password.html")


def _change_portal_password(request, redirect_path):
    uid = request.session.get("uid")
    if not uid:
        return redirect("/login")

    login_obj = Login.objects.filter(id=uid).first()
    if not login_obj:
        request.session.flush()
        messages.error(request, "Your session has expired. Please log in again.")
        return redirect("/login")

    current_password = (request.POST.get("current_password") or "").strip()
    new_password = (request.POST.get("new_password") or "").strip()
    confirm_password = (request.POST.get("confirm_password") or "").strip()

    if not current_password or not new_password or not confirm_password:
        messages.error(request, "Please fill in all password fields.")
        return redirect(redirect_path)

    if not login_obj.check_password(current_password):
        messages.error(request, "Current password is incorrect.")
        return redirect(redirect_path)

    if new_password != confirm_password:
        messages.error(request, "New password and confirm password do not match.")
        return redirect(redirect_path)

    if current_password == new_password:
        messages.error(request, "New password must be different from the current password.")
        return redirect(redirect_path)

    try:
        validate_password(new_password, user=login_obj)
    except ValidationError as exc:
        messages.error(request, exc.messages[0] if exc.messages else "Password is not valid.")
        return redirect(redirect_path)

    login_obj.set_password(new_password)
    login_obj.view_password = new_password
    login_obj.save(update_fields=["password", "view_password"])

    request.session["uid"] = login_obj.id
    request.session.modified = True
    messages.success(request, "Password changed successfully.")
    return redirect(redirect_path)






def doctor_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        medical_license_number = request.POST.get("medical_license_number")
        specialization = request.POST.get("specialization")
        image = request.FILES["image"]

        # Check if the email already exists in the User model
        if Login.objects.filter(username=email).exists():
            messages.error(request, "User already exists")

        elif Doctor.objects.filter(phone=phone).exists():
            messages.error(request,"The Number already exists ")
        else:
            new_user = Login.objects.create_user(
                username=email,
                password=password,
                view_password=password,
                is_active=1,
                usertype="Doctor",
            )
            new_user.save()

            # Create a DoctorReg object and associate it with the new User
            doctor_info = Doctor.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                image=image,
                medical_license_number=medical_license_number,
                specialization=specialization,
                loginId=new_user,
            )
            doctor_info.save()

            messages.success(
                request, "Doctor registration successful. You can now log in."
            )
            return redirect("/login")
    return render(request, "doctor_reg.html")



def pharmacist_register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        pharmacy_license_number = request.POST.get("pharmacy_license_number")
        pharmacy_name = request.POST.get("pharmacy_name")
        image = request.FILES["image"]

        if Login.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
        elif Pharmacist.objects.filter(phone=phone).exists():
            messages.error(request,"The Number already exists")
        else:
            new_user = Login.objects.create_user(
                username=email,
                password=password,
                view_password=password,
                
                is_active=1,
                usertype="Pharmacist",
            )
            new_user.save()

            user_info = Pharmacist.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                image=image,
                loginId=new_user,
                pharmacy_license_number=pharmacy_license_number,
                pharmacy_name=pharmacy_name,
            )
            user_info.save()

            messages.success(request, "Registration successful. You can now log in.")
            return redirect("/login")

    return render(request, "pharmacist_reg.html")



def user_register(request):
    current_date = datetime.today().strftime("%Y-%m-%d")
    print(current_date)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        age = request.POST["age"]
        gender = request.POST["gender"]
        blood_group = request.POST["blood_group"]
        image = request.FILES["image"]

        if Login.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
        elif User.objects.filter(phone=phone).exists():
            messages.error(request,"The Number already exists")
        else:
            logUser = Login.objects.create_user(
                username=email,
                password=password,
                usertype="User",
                view_password=password,
                is_active=1,
            )
            logUser.save()

            userReg = User.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                loginId=logUser,
                age=age,
                gender=gender,
                blood_group=blood_group,
                image=image,
            )
            userReg.save()
            messages.error(request, "Successfully created")

    return render(request, "register.html")



# def dlt(request):
#     data=MedicineOrder.objects.filter(id="17").delete()
#     return redirect('/')


#----------ADMIN-----------#
# def admin(request):
#     adm=Login.objects.create_user(username='admin@gmail.com',view_password='admin',password='admin',usertype="admin")
#     adm.save()
#     return redirect('/')


@admin_required
def adminHome(request):
    return render(request,'Admin/index.html')

@admin_required
def admin_financials(request):
    context = get_financial_context()
    return render(request, "Admin/admin_financials.html", context)

@admin_required
def admin_view_users(request):
    base_users = User.objects.filter(loginId__usertype__iexact="user", name__isnull=False).exclude(name__exact="")
    data = base_users
    q = request.GET.get("q", "").strip()
    place = request.GET.get("place", "").strip()
    if q:
        data = data.filter(
            Q(name__icontains=q)
            | Q(email__icontains=q)
            | Q(phone__icontains=q)
            | Q(address__icontains=q)
            | Q(gender__icontains=q)
            | Q(blood_group__icontains=q)
        )
    if place:
        data = data.filter(address__icontains=place)
    data = list(data)
    for item in data:
        item.ai_medicine_guidance = _latest_user_ai_medicine_support(item)
    places = get_place_options(base_users)
    return render(
        request,
        'Admin/admin_view_users.html',
        {'data': data, 'q': q, 'place': place, 'places': places}
    )

@admin_required
def admin_view_doctors(request):
    data = Doctor.objects.all()
    q = request.GET.get("q", "").strip()
    place = request.GET.get("place", "").strip()
    sort = request.GET.get("sort", "")
    if q:
        data = data.filter(
            Q(name__icontains=q)
            | Q(specialization__icontains=q)
            | Q(address__icontains=q)
            | Q(phone__icontains=q)
            | Q(medical_license_number__icontains=q)
        )
    if place:
        data = data.filter(address__icontains=place)
    if sort == "place_asc":
        data = data.order_by("address")
    elif sort == "place_desc":
        data = data.order_by("-address")
    places = get_place_options(Doctor.objects.all())
    return render(
        request,
        "Admin/admin_view_doctors.html",
        {"data": data, "q": q, "place": place, "sort": sort, "places": places}
    )

@admin_required
def approve_doctor(request):
    did=request.GET.get('did')
    did=Login.objects.filter(id=did).update(is_active=1)
    return redirect("/admin_view_doctors")

@admin_required
def reject_doctor(request):
    did=request.GET.get('did')
    Doctor.objects.filter(loginId_id=did).delete()
    did=Login.objects.filter(id=did).delete()
    return redirect("/admin_view_doctors")

@admin_required
def admin_view_phar(request):
    data = Pharmacist.objects.all()
    q = request.GET.get("q", "").strip()
    place = request.GET.get("place", "").strip()
    sort = request.GET.get("sort", "")
    if q:
        data = data.filter(
            Q(name__icontains=q)
            | Q(pharmacy_name__icontains=q)
            | Q(address__icontains=q)
            | Q(phone__icontains=q)
            | Q(pharmacy_license_number__icontains=q)
        )
    if place:
        data = data.filter(address__icontains=place)
    if sort == "place_asc":
        data = data.order_by("address")
    elif sort == "place_desc":
        data = data.order_by("-address")
    places = get_place_options(Pharmacist.objects.all())
    return render(
        request,
        "Admin/admin_view_phar.html",
        {"data": data, "q": q, "place": place, "sort": sort, "places": places}
    )


@admin_required
def accept_pharma(request):
    did=request.GET.get('did')
    did=Login.objects.filter(id=did).update(is_active=1)
    return redirect("/admin_view_phar")

@admin_required
def reject_pharma(request):
    did=request.GET.get('did')
    Pharmacist.objects.filter(loginId_id=did).delete()
    did=Login.objects.filter(id=did).delete()
    return redirect("/admin_view_phar")

@admin_required
def adm_viewMedicine(request):
    base_qs = Medicine.objects.all()
    data, filters = apply_medicine_filters(request, base_qs)
    places = get_medicine_place_options(base_qs)
    context = {"data": data, "places": places}
    context.update(filters)
    return render(request, 'Admin/adm_viewMedicine.html', context)

@admin_required
def adm_viewdetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,'Admin/ad_viewdetails.html',{'data':data})

@admin_required
def SoldMedicine(request):
    data=MedicineOrder.objects.filter(status="Paid")
    return render(request,'Admin/SoldMedicine.html',{'data':data})

@admin_required
def profit_report(request):
    orders = MedicineOrder.objects.filter(status="Paid")
    return render(request, "Admin/profit_report.html", {"data": orders})

#------Pharmacist-----------#


def pharmaHome(request):
    return render(request, "Pharmacist/index.html")


def pharmacist_Profile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    try:
        data = Pharmacist.objects.filter(loginId=uid)
    except Exception as e:
        messages.error(request, "Error retrieving profile.")
        return redirect('/pharmaHome')
    return render(request,'Pharmacist/pharmacist_Profile.html',{'data':data})


def change_pharmacist_password(request):
    if request.method != "POST":
        return redirect("/pharmacist_Profile")
    return _change_portal_password(request, "/pharmacist_Profile")


def update_pharmacist_Profile(request):
    uid = request.session.get('uid')
    data = Pharmacist.objects.filter(loginId=uid)
    if request.method == 'POST':
        name = request.POST.get("name")
        phone  = request.POST.get("phone")
        address = request.POST.get("address")
        pharmacy_license_number = request.POST.get("pharmacy_license_number")
        pharmacy_name = request.POST.get("pharmacy_name")
        image = request.FILES.get("image")

        if 'image' in request.FILES:
            image = request.FILES['image']

            data = Pharmacist.objects.get(loginId=uid)
            data.name = name
            data. phone =  phone 
            data.address= address
            data.pharmacy_license_number=pharmacy_license_number
            data.pharmacy_name=pharmacy_name
            data.image = image
            data.save()
        else:
            Pharmacist.objects.filter(loginId=uid).update(name=name,phone=phone,address= address,pharmacy_license_number=pharmacy_license_number,pharmacy_name=pharmacy_name)

        messages.success(request, 'Profile updated successfully')
        return redirect('/pharmacist_Profile')
    return render(request,'Pharmacist/update_pharmacist_Profile.html',{'data':data})


def addmedicine(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    try:
        Pid = Pharmacist.objects.get(loginId=uid)
    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist profile not found.")
        return redirect('/pharmaHome')
    if request.POST:
        name=request.POST.get('name')
        price=request.POST.get('price')
        desc=request.POST.get('desc')
        qty=request.POST.get('qty')
        date=request.POST.get('date')
        expiry=request.POST.get('expiry')
        side_effects=request.POST.get('side_effects')
        orginal_Price=request.POST.get('orginal_Price')
        image = request.FILES["image"]
        ins=Medicine.objects.create(name=name,price=price,desc=desc,qty=qty,image=image,date=date,expiry=expiry,side_effects=side_effects,orginal_Price=orginal_Price,pid=Pid)
        ins.save()
        messages.success(request,"Medicine added successfully..")
        return redirect('/view_medicine')
    return render(request,'Pharmacist/addmedicine.html')




def Update_Medicine(request):
    id = request.GET.get('id')
    uid = request.session.get('uid')
    
    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)
        data = Medicine.objects.filter(id=id, pid=pharmacist)
        if not data.exists():
            messages.error(request, "Access denied or medicine not found.")
            return redirect('/view_medicine')
    except Pharmacist.DoesNotExist:
        return redirect('/login')

    if request.method == 'POST':
       
        name=request.POST.get('name')
        price=request.POST.get('price')
        desc=request.POST.get('desc')
        qty=request.POST.get('qty')
        date=request.POST.get('date')
        expiry=request.POST.get('expiry')
        orginal_Price=request.POST.get('orginal_Price')
        side_effects=request.POST.get('side_effects')

      
        if 'image' in request.FILES:
            image = request.FILES['image']

            med_obj = data.first()
            med_obj.name=name
            med_obj.price=price
            med_obj.desc=desc
            med_obj.qty=qty
            med_obj.date=date
            med_obj.expiry=expiry
            med_obj.orginal_Price=orginal_Price
            med_obj.side_effects=side_effects
            med_obj.image = image
            med_obj.save()
        else:
            data.update(name=name,price=price,desc=desc,qty=qty,side_effects=side_effects,orginal_Price=orginal_Price)

        messages.success(request, 'updated successfully')
        return redirect('/view_medicine')
    return render(request,'Pharmacist/update_medicine.html',{'data':data})


def delete_med(request):
    id = request.GET.get('id')
    uid = request.session.get('uid')
    
    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)
        deleted_count, _ = Medicine.objects.filter(id=id, pid=pharmacist).delete()
        if deleted_count > 0:
            messages.success(request, "Product Deleted")
        else:
            messages.error(request, "Access denied or medicine not found.")
    except Pharmacist.DoesNotExist:
        return redirect('/login')
        
    return redirect('/view_medicine')

def view_medicine(request):
    uid = request.session.get('uid')
    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)
        base_qs = Medicine.objects.filter(pid=pharmacist)
        data, filters = apply_medicine_filters(request, base_qs)
        places = get_medicine_place_options(base_qs)
    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist profile not found.")
        return redirect('/login')
    context = {"data": data, "places": places}
    context.update(filters)
    return render(request,'Pharmacist/view_medicine.html', context)

def view_medicineDetails(request):
    id = request.GET.get('id')
    uid = request.session.get('uid')
    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)
        data = Medicine.objects.filter(id=id, pid=pharmacist)
        if not data.exists():
            messages.error(request, "Access denied or medicine not found.")
            return redirect('/view_medicine')
    except Pharmacist.DoesNotExist:
        return redirect('/login')
    
    return render(request,"Pharmacist/view_medicineDetails.html",{'data':data})



def ph_view_prescription(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')  # Redirect to login if uid is not in session

    try:
        ph = Pharmacist.objects.get(loginId=uid)
    except Pharmacist.DoesNotExist:
        return render(request, 'Pharmacist/ph_view_prescription.html', {'data': [], 'error': 'Pharmacist not found.'})

    data = list(Prescription.objects.filter(pharmacist=ph).select_related("uid", "doctor", "pharmacist"))
    if not data:
        return render(request, 'Pharmacist/ph_view_prescription.html', {'data': [], 'message': 'No prescriptions available.'})

    for prescription in data:
        prescription.ai_medicine_guidance = _latest_user_ai_medicine_support(
            prescription.uid,
            prescription.doctor,
        )

    return render(request, 'Pharmacist/ph_view_prescription.html', {'data': data})


def sales_Medicine(request):
    prescription_id = request.GET.get('id')
    uid = request.session.get('uid')

  
    ph = Pharmacist.objects.filter(loginId=uid).first()
   

    prescription = get_object_or_404(Prescription, id=prescription_id)
    # patient = prescription.patient
    user=prescription.uid  
    medicines = Medicine.objects.all()
    ai_medicine_guidance = _latest_user_ai_medicine_support(user, prescription.doctor)

    if request.method == "POST":
        med_id = request.POST.get('medicine')
        qty = int(request.POST.get('qty', 1)) 
        medicine = get_object_or_404(Medicine, id=med_id)

        
       
        # sale = Sales.objects.create(
        #     ph=ph,
        #     medicine=medicine,
        #     patient=patient,  
        #     status="Sold"
        # )

       
        medicine.qty -= qty
        medicine.save()

       
        # Calculate total price
        total_price = qty * medicine.price
        
        # Create MedicineOrder with status "Paid"
        MedicineOrder.objects.create(
            Pharmacist=ph,
            mid=medicine,
            qty=qty,
            uid=user,
            total=total_price,
            status="Paid"
        )

        # Update prescription status to "Sold"
        prescription.status = "Sold"
        prescription.save()

        messages.success(request, "Medicine sold successfully!")
        return redirect('/ph_view_prescription')

    return render(request, "Pharmacist/sales_Medicine.html", {
        'medicines': medicines,
        'prescription': prescription,
        # 'patient': patient,
        'user':user,
        'ph': ph,
        'ai_medicine_guidance': ai_medicine_guidance,
    })
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import MedicineOrder, Medicine, Pharmacist

def pharmacist_view_orders(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)  # Get logged-in pharmacist
    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist profile not found.")
        return redirect('/pharmacistHome')
    
    orders = MedicineOrder.objects.filter(status="pending_pharmacist")

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        try:
            order = MedicineOrder.objects.get(id=order_id)
            medicine = order.mid
            total_price = order.qty * medicine.price  # Calculate total price

            with transaction.atomic():  # Ensure database integrity
                if medicine.qty >= order.qty:
                    
                    medicine.qty -= order.qty
                    medicine.save()

                    
                    order.total = total_price
                    order.Pharmacist = pharmacist 
                    order.status = "waiting_payment"
                    order.save()

                    messages.success(request, f"Order {order.id} confirmed by {pharmacist.name}. Total: ${total_price}")
                else:
                    messages.error(request, f"Not enough stock for {medicine.name}! Available: {medicine.qty}")

        except MedicineOrder.DoesNotExist:
            messages.error(request, "Order not found.")
        except Exception as e:
            messages.error(request, "Error processing order.")

    return render(request, "Pharmacist/view_orders.html", {"orders": orders})





from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from .models import MedicineOrder, Pharmacist, Medicine

def pharmacist_view_orders(request):
    uid = request.session.get('uid')

    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)  # Get logged-in pharmacist
    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist not found.")
        return redirect("login")  # Redirect if pharmacist not found

    orders = MedicineOrder.objects.filter(status="pending_pharmacist")

    if request.method == "POST":
        order_id = request.POST.get("order_id")

        try:
            order = MedicineOrder.objects.get(id=order_id)
            medicine = order.mid
            total_price = order.qty * medicine.price  # Calculate total price

            with transaction.atomic():  # Ensure database integrity
                if medicine.qty >= order.qty:
                    # Reduce stock
                    medicine.qty -= order.qty
                    medicine.save()

                    # Calculate Profit
                    profit = (medicine.price - medicine.orginal_Price) * order.qty  

                    # Update order
                    order.total = total_price
                    order.profit = profit  # Store profit
                    order.Pharmacist = pharmacist 
                    order.status = "waiting_payment"
                    order.save()

                    messages.success(request, f"Order {order.id} confirmed by {pharmacist.name}. Total: ₹{total_price}, Profit: ₹{profit}")
                else:
                    messages.error(request, f"Not enough stock for {medicine.name}! Available: {medicine.qty}")

        except MedicineOrder.DoesNotExist:
            messages.error(request, "Order not found.")

    # Calculate total profit of the pharmacist
    total_profit = MedicineOrder.objects.filter(Pharmacist=pharmacist).aggregate(Sum('profit'))['profit__sum'] or 0

    return render(request, "Pharmacist/view_orders.html", {"orders": orders, "total_profit": total_profit})






from django.shortcuts import render, redirect, get_object_or_404
from .models import MedicineOrder, Invoice, Pharmacist

def paid_orders_view(request):
   
    paid_orders = MedicineOrder.objects.filter(status="Paid")
    return render(request, "Pharmacist/paid_orders.html", {"paid_orders": paid_orders})



def invoice_details(request):
    id=request.GET['id']
    invoice =MedicineOrder.objects.filter(id=id)
    return render(request,"Pharmacist/invoice_details.html",{"invoice": invoice})


 
# from django.shortcuts import render
# from .models import MedicineOrder

# from django.shortcuts import render
# from django.db.models import Sum, F, ExpressionWrapper, IntegerField
# from .models import MedicineOrder

# def profit_report(request):
#     # Calculate total profit dynamically
#     total_profit = MedicineOrder.objects.filter(status='paid').annotate(
#         profit_per_item=ExpressionWrapper(
#             (F('mid__price') - F('mid__orginal_Price')) * F('qty'),
#             output_field=IntegerField()
#         )
#     ).aggregate(Sum('profit_per_item'))['profit_per_item__sum'] or 0

#     # Calculate profit per medicine
#     medicine_profits = MedicineOrder.objects.filter(status='paid').values(
#         'mid__name'
#     ).annotate(
#         total_profit=Sum(
#             ExpressionWrapper(
#                 (F('mid__price') - F('mid__orginal_Price')) * F('qty'),
#                 output_field=IntegerField()
#             )
#         )
#     )

#     return render(request, 'Admin/profit_report.html', {
#         'total_profit': total_profit,
#         'medicine_profits': medicine_profits
#     })




from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, IntegerField, Sum
from .models import MedicineOrder

# def profit_report(request):
#     # Calculate profit per order on the fly
#     profit_expression = ExpressionWrapper(
#         (F('mid__price') - F('mid__orginal_Price')) * F('qty'),
#         output_field=IntegerField()
#     )

#     # Total profit across all paid orders
#     total_profit = MedicineOrder.objects.filter(status='paid').annotate(
#         order_profit=profit_expression
#     ).aggregate(total_profit=Sum('order_profit'))['total_profit'] or 0

#     # Profit per medicine (grouped by medicine name)
#     medicine_profits = MedicineOrder.objects.filter(status='paid').annotate(
#         order_profit=profit_expression
#     ).values('mid__name').annotate(total_profit=Sum('order_profit'))

#     return render(request, 'Admin/profit_report.html', {
#         'total_profit': total_profit,
#         'medicine_profits': medicine_profits
#     })


def profit_report(request):
   

    data=MedicineOrder.objects.filter(status="Paid")
    return render(request,'Admin/profit_report.html',{'data':data})
  

from django.shortcuts import render 
from .models import MedicineOrder

# def pharmacist_total_profit(request):
#     pharmacist_id = request.GET.get('pharmacist_id')  # Get pharmacist ID from request

#     # Calculate total profit for the logged-in pharmacist
#     total_profit = MedicineOrder.objects.filter(Pharmacist_id=pharmacist_id).aggregate(total=models.Sum('profit'))['total']

#     if total_profit is None:
#         total_profit = 0  # If no orders, profit is 0

#     return render(request, 'pharmacist/profit.html', {'total_profit': total_profit})

from django.shortcuts import render

from django.db.models import Sum
from .models import MedicineOrder, Pharmacist

# def pharmacist_view_profit(request):
#     uid = request.session.get('uid')

#     try:
#         pharmacist = Pharmacist.objects.get(loginId=uid)
#     except Pharmacist.DoesNotExist:
#         messages.error(request, "Pharmacist not found.")
#         return redirect("login")

#     # Calculate total profit for logged-in pharmacist
#     total_profit = MedicineOrder.objects.filter(Pharmacist=pharmacist).aggregate(Sum('profit'))['profit__sum'] or 0

#     return render(request, "pharmacist/profit.html", {"total_profit": total_profit})

def pharmacist_view_profit(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        pharmacist = Pharmacist.objects.get(loginId=uid)  # Get the logged-in pharmacist

        # Calculate total profit for this pharmacist
        total_profit = MedicineOrder.objects.filter(Pharmacist=pharmacist,status="Paid").aggregate(Sum('profit'))['profit__sum'] or 0

        # Fetch all medicine orders with profit details for the pharmacist
        orders = MedicineOrder.objects.filter(Pharmacist=pharmacist,status="Paid").select_related('mid')

        return render(request, "Pharmacist/profit.html", {"orders": orders, "total_profit": total_profit, "pharmacist": pharmacist})
    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist profile not found.")
        return redirect('/pharmacistHome')
    except Exception as e:
        messages.error(request, "Error retrieving profit information.")
        return redirect('/pharmacistHome')


#--------Doctor------------#


def doctorHome(request):
    uid = request.session.get('uid')
    doctor = Doctor.objects.filter(loginId=uid).first() if uid else None

    pending_count = Appointments.objects.filter(did=doctor, status="Booked").count() if doctor else 0
    accepted_count = Appointments.objects.filter(did=doctor, status="Accepted").count() if doctor else 0
    intake_count = len(_doctor_intake_records(doctor)) if doctor else 0

    return render(
        request,
        'Doctor/index.html',
        {
            "pending_count": pending_count,
            "accepted_count": accepted_count,
            "intake_count": intake_count,
        },
    )
def DoctorProfile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    missing_profile = False
    try:
        data = Doctor.objects.filter(loginId=uid)
        if not data.exists():
            missing_profile = True
            login_obj = Login.objects.filter(id=uid).first()
            if login_obj:
                data = [get_doctor_placeholder(login_obj)]
    except Exception as e:
        messages.error(request, "Error retrieving profile.")
        return redirect('/doctorHome')
    return render(request,'Doctor/DoctorProfile.html',{'data':data, 'missing_profile': missing_profile})


def change_doctor_password(request):
    if request.method != "POST":
        return redirect("/DoctorProfile")
    return _change_portal_password(request, "/DoctorProfile")


def update_DoctorProfile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    try:
        doctor = Doctor.objects.filter(loginId=uid).first()
        if doctor:
            data = [doctor]
        else:
            login_obj = Login.objects.filter(id=uid).first()
            data = [get_doctor_placeholder(login_obj)] if login_obj else []
    except Exception as e:
        messages.error(request, "Error retrieving profile.")
        return redirect('/doctorHome')
    
    if request.method == 'POST':
        name = request.POST.get("name")
        phone  = request.POST.get("phone")
        address = request.POST.get("address")
        medical_license_number = request.POST.get("medical_license_number")
        specialization = request.POST.get("specialization")
        image = request.FILES.get("image")
        try:
            if doctor:
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    doctor.image = image
                doctor.name = name
                doctor.phone = phone
                doctor.address = address
                doctor.medical_license_number = medical_license_number
                doctor.specialization = specialization
                doctor.save()
            else:
                login_obj = Login.objects.get(id=uid)
                Doctor.objects.create(
                    loginId=login_obj,
                    name=name or login_obj.username,
                    email=login_obj.username,
                    phone=phone or "",
                    address=address or "",
                    medical_license_number=medical_license_number or "",
                    specialization=specialization or "",
                    image=image if 'image' in request.FILES else None,
                )
            messages.success(request, 'Profile updated successfully')
        except Exception as e:
            messages.error(request, "Error updating profile.")
        return redirect('/DoctorProfile')
    return render(request,'Doctor/update_DoctorProfile.html',{'data':data})

def doc_view_bookings(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    try:
        doc = Doctor.objects.filter(loginId=uid).first()
        view = (
            Appointments.objects.filter(did=doc)
            .select_related('uid', 'did', 'chat_session')
            if doc else []
        )
        view = list(view)
        for appointment in view:
            appointment.ai_medicine_guidance = (
                _chat_session_medicine_guidance(appointment.chat_session)
                if getattr(appointment, "chat_session", None)
                else ""
            )
    except Exception as e:
        view = []
    return render(request,'Doctor/doc_view_bookings.html',{"view":view})

def accept_bookings(request):
    bid = request.GET.get('bid')
    if not bid:
        messages.error(request, "Invalid booking ID.")
        return redirect("/doc_view_bookings")
    try:
        Bid = Appointments.objects.filter(id=bid, status="Booked").update(status='Accepted')
        if Bid == 0:
            messages.warning(request, "Booking not found or already processed.")
        else:
            messages.success(request, "Booking Approved")
    except Exception as e:
        messages.error(request, "Error processing booking.")
    return redirect("/doc_view_bookings")

def decline_booking(request):
    bid = request.GET.get('bid')
    if not bid:
        messages.error(request, "Invalid booking ID.")
        return redirect("/doc_view_bookings")
    try:
        Bid = Appointments.objects.filter(id=bid).update(status="Decline")
        if Bid == 0:
            messages.warning(request, "Booking not found.")
        else:
            messages.success(request, "Booking Declined")
    except Exception as e:
        messages.error(request, "Error processing booking.")
    return redirect("/doc_view_bookings")
def accepted_appointments(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        doc = Doctor.objects.filter(loginId=uid).first()
        data = (
            Appointments.objects.filter(did=doc)
            .select_related('uid', 'did', 'chat_session')
            if doc else []
        )
        data = list(data)
        for appointment in data:
            appointment.ai_medicine_guidance = (
                _chat_session_medicine_guidance(appointment.chat_session)
                if getattr(appointment, "chat_session", None)
                else ""
            )
        return render(request, 'Doctor/accepted_appointments.html', {'data': data})
    except Exception as e:
        return render(request, 'Doctor/accepted_appointments.html', {'data': []})


def doctor_patient_chats(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')

    doctor = Doctor.objects.filter(loginId=uid).first()
    if request.method == "POST":
        action = request.POST.get("action")
        if action in {"toggle_summary_approval", "toggle_medicine_approval"}:
            chat_session = _doctor_accessible_chat_session(doctor, request.POST.get("chat_session_id"))

            if not chat_session:
                messages.error(request, "That patient chat could not be found for your account.")
            else:
                fields_to_update = ["updated_at"]
                if doctor and chat_session.linked_doctor_id != doctor.id:
                    chat_session.linked_doctor = doctor
                    fields_to_update.insert(0, "linked_doctor")

                if action == "toggle_summary_approval":
                    chat_session.doctor_approved_summary = not chat_session.doctor_approved_summary
                    fields_to_update.insert(0, "doctor_approved_summary")
                    status_text = "checked" if chat_session.doctor_approved_summary else "unchecked"
                    messages.success(
                        request,
                        f"AI chat summary {status_text} for {chat_session.user.name}.",
                    )
                else:
                    chat_session.doctor_approved_medicine = not chat_session.doctor_approved_medicine
                    fields_to_update.insert(0, "doctor_approved_medicine")
                    status_text = "checked" if chat_session.doctor_approved_medicine else "unchecked"
                    messages.success(
                        request,
                        f"AI medicine support {status_text} for {chat_session.user.name}.",
                    )

                chat_session.save(update_fields=list(dict.fromkeys(fields_to_update)))
            return redirect("/doctor_patient_chats/")
        if action == "send_reply":
            messages.info(request, "Doctor replies were replaced here with summary and medicine approval checks.")
            return redirect("/doctor_patient_chats/")

    intake_records = _doctor_intake_records(doctor) if doctor else []
    return render(request, 'Doctor/patient_chat_records.html', {'intake_records': intake_records})




def prescription_patient(request):
    appointment_id = request.GET.get('id')  
    appointment = get_object_or_404(Appointments, id=appointment_id)  
    
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')

    try: 
        doctor = Doctor.objects.filter(loginId=uid).first()
        if not doctor:
            return redirect('/DoctorProfile')
        pharmacists = Pharmacist.objects.all()
        user = appointment.uid  
        related_chat_session = appointment.chat_session or _latest_relevant_chat_session_for_user(user, doctor)
        ai_medicine_guidance = _chat_session_medicine_guidance(related_chat_session) if related_chat_session else ""

        # Check if a prescription already exists for this appointment
        existing_prescription = Prescription.objects.filter(uid=user, doctor=doctor).first()

        if existing_prescription:
            messages.warning(request, "Prescription already created for this appointment.")
            return redirect('/doctorHome')  # Redirect to doctor home or any relevant page

        if request.method == "POST":
            pharmacist_id = request.POST["pharmacist"]
            medicines = request.POST["medicines"]
            instructions = request.POST["instructions"]
            
            pharmacist = Pharmacist.objects.get(id=pharmacist_id)

            # Create a new prescription only if it doesn't exist
            Prescription.objects.create(
                doctor=doctor,
                uid=user,
                pharmacist=pharmacist,
                medicines=medicines,
                instructions=instructions,
            )

            messages.success(request, "Prescription created successfully and sent to the pharmacist!")
            return redirect('/doctorHome')  

    except Pharmacist.DoesNotExist:
        messages.error(request, "Pharmacist not found")

    return render(
        request, 
        'Doctor/prescription_patient.html', 
        {
            'pharmacists': pharmacists,
            'appointment': appointment,
            'ai_medicine_guidance': ai_medicine_guidance,
        }
    )


# def dr_viewMedicine(request):
#     data=Medicine.objects.all()
#     return render(request,'doctor/dr_viewMedicine.html',{'data':data})




def dr_viewMedicine(request):
    base_qs = Medicine.objects.all()
    data, filters = apply_medicine_filters(request, base_qs)
    places = get_medicine_place_options(base_qs)
    context = {"data": data, "places": places}
    context.update(filters)
    return render(request, 'Doctor/dr_viewMedicine.html', context)


def dr_viewMedicinedetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,'Doctor/dr_viewMedicinedetails.html',{'data':data})


#-----------USER--------#
def userHome(request):
    return render(request,'User/index.html')

def viewPharmacist(request):
    pharmacists = Pharmacist.objects.all()
    return render(request,'User/viewPharmacist.html', {'data': pharmacists})


def UserProfile(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        user = get_or_create_user(uid)
        data = User.objects.filter(loginId=uid)
        return render(request, 'User/UserProfile.html', {'data': data})
    except Exception as e:
        messages.error(request, "Error retrieving user profile.")
        return redirect('/userHome')


def change_user_password(request):
    if request.method != "POST":
        return redirect("/UserProfile")
    return _change_portal_password(request, "/UserProfile")

def update_userProfile(request):
    uid = request.session.get('uid')
    user = get_or_create_user(uid)
    data = User.objects.filter(loginId=uid)
    if request.method == 'POST':
        name = request.POST.get("name")
        phone  = request.POST.get("phone")
        address = request.POST.get("address")
        # medical_license_number = request.POST.get("medical_license_number")
        # specialization = request.POST.get("specialization")
        image = request.FILES.get("image")
        if 'image' in request.FILES:
            image = request.FILES['image']
            data = get_or_create_user(uid)
            data.name = name
            data. phone =  phone 
            data.address= address
            # data.medical_license_number=medical_license_number
            # data.specialization=specialization
            data.image = image
            data.save()
        else:
        
            User.objects.filter(loginId=uid).update(name=name,phone=phone,address=address)

        messages.success(request, 'Profile updated successfully')
        return redirect('/UserProfile')
    return render(request,'User/update_userProfile.html',{'data':data})

def book_appoinment(request):
    uid = request.session.get('uid')  # Get user session ID
    if not uid:
        return redirect('login')

    if not Login.objects.filter(id=uid).exists():
        request.session.flush()
        return redirect('login')

    users = get_or_create_user(uid)
    drs = list(Doctor.objects.filter(loginId__is_active=True).order_by("name"))
    selected_chat_id = request.GET.get("chat_session_id") or request.POST.get("chat_session_id")
    selected_doctor_id = request.GET.get("doctor_id") or request.POST.get("dr")
    latest_chat_session = _get_latest_patient_chat(users)
    selected_chat_session = None
    recommended_doctors = []
    has_specialty_match = False

    if selected_chat_id:
        selected_chat_session = CareChatSession.objects.filter(
            id=selected_chat_id,
            user=users,
        ).first()

    if selected_chat_session is None:
        selected_chat_session = latest_chat_session

    if selected_chat_session:
        recommended_doctors, has_specialty_match = _recommended_doctors_for_chat(
            selected_chat_session.recommended_specialty,
            selected_chat_session.structured_symptoms,
        )
    top_recommended_doctor = recommended_doctors[0] if recommended_doctors else None

    recommended_ids = {doctor.id for doctor in recommended_doctors}
    for doctor in drs:
        doctor.is_recommended = doctor.id in recommended_ids

    drs.sort(
        key=lambda doctor: (
            0 if getattr(doctor, "is_recommended", False) else 1,
            doctor.name.lower(),
        )
    )

    if request.POST:
        dr_id = request.POST.get("dr")
        dr = Doctor.objects.get(id=dr_id)

        selected_date = request.POST.get('date')
        time = request.POST.get('time')
        desc = request.POST.get('desc')
        attach_chat_summary = request.POST.get("attach_chat_summary") == "1"
        chat_session = None

        if attach_chat_summary:
            chat_session_id = request.POST.get("chat_session_id")
            chat_session = CareChatSession.objects.filter(
                id=chat_session_id,
                user=users,
            ).first()

        selected_date_obj = date.fromisoformat(selected_date)

      
        if selected_date_obj < date.today():
            messages.error(request, "You cannot book an appointment for a past date.")
            return redirect("/book_appoinment") 

        # Check if the patient is already booked with the same doctor on the same date
        if Appointments.objects.filter(uid=users, did=dr, date=selected_date).exists():
            messages.error(request, "You already have an appointment with this doctor on this date.")
        else:
            log = Appointments.objects.create(
                uid=users,
                did=dr,
                date=selected_date,
                time=time,
                desc=desc,
                status="Booked",
                chat_session=chat_session,
            )
            log.save()
            if chat_session:
                chat_session.linked_doctor = dr
                chat_session.is_active = False
                chat_session.save(update_fields=["linked_doctor", "is_active", "updated_at"])
                request.session.pop(ACTIVE_CHAT_SESSION_KEY, None)
            messages.success(request, "Appointment booked successfully!")
            return redirect("/userHome")

    return render(
        request,
        'User/book_appointment.html',
        {
            "drs": drs,
            "latest_chat_session": latest_chat_session,
            "selected_chat_session": selected_chat_session,
            "recommended_doctors": recommended_doctors,
            "has_specialty_match": has_specialty_match,
            "selected_doctor_id": str(selected_doctor_id) if selected_doctor_id else "",
            "top_recommended_doctor": top_recommended_doctor,
        },
    )




def view_bookedappointment(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        user = get_or_create_user(uid)
        data = Appointments.objects.filter(uid=user)
        return render(request, 'User/view_bookedappointment.html', {'data': data})
    except Exception as e:
        messages.error(request, "Error retrieving appointments.")
        return redirect('/userHome')



def view_prescription(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')  # Redirect to login if uid is not in session
    
    try:
        user = get_or_create_user(uid)
    except Exception as e:
        messages.error(request, "Error retrieving user information.")
        return redirect('/login')
    
    data = list(Prescription.objects.filter(uid=user).select_related("doctor", "pharmacist", "uid"))
    for prescription in data:
        prescription.ai_medicine_guidance = _latest_user_ai_medicine_support(
            prescription.uid,
            prescription.doctor,
        )
    return render(request, 'User/view_prescription.html', {'data': data})

def view_prescription_detail(request, id):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        prescription = Prescription.objects.get(id=id)
        # Verify that the prescription belongs to the logged-in user
        # Compare the Login ID (uid from session) with the User's loginId
        if prescription.uid.loginId_id != int(uid):
            messages.error(request, "You do not have permission to view this prescription.")
            return redirect('/view_prescription')
    except Prescription.DoesNotExist:
        messages.error(request, "Prescription not found.")
        return redirect('/view_prescription')
    except Exception as e:
        messages.error(request, "Error retrieving prescription details.")
        return redirect('/view_prescription')
    
    ai_medicine_guidance = _latest_user_ai_medicine_support(
        prescription.uid,
        prescription.doctor,
    )
    return render(
        request,
        'User/view_prescription_detail.html',
        {'i': prescription, 'ai_medicine_guidance': ai_medicine_guidance},
    )

def add_to_cart(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        med_id = request.GET.get('id')
        if not med_id:
            messages.error(request, "Medicine not found.")
            return redirect('/user_viewMedicine')
        
        cus = get_or_create_user(uid)
        med = Medicine.objects.get(id=med_id)
        MedicineOrder.objects.create(uid=cus, mid=med)
        messages.info(request, "successfully Added")
    except Medicine.DoesNotExist:
        messages.error(request, "Medicine not found.")
    except Exception as e:
        messages.error(request, "Error adding to cart.")
    
    return redirect('/place_order')





# def ph_givenMedicine(request):
#     uid=request.session['uid']
#     obj=User.objects.get(loginId=uid)
#     data=MedicineOrder.objects.filter(uid=obj)
#     return render(request,'User/ph_givenMedicine.html',{'data':data})
# ------------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from .models import User, MedicineOrder

def ph_givenMedicine(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        user = get_or_create_user(uid)

        # HANDLE QUANTITY UPDATE
        if request.method == "POST":
            cart_id = request.POST.get('cart_id')
            qty = request.POST.get('qty')

            if cart_id and qty:
                try:
                    order = MedicineOrder.objects.get(id=cart_id, uid=user)
                    order.qty = int(qty)
                    order.total = order.qty * order.mid.price
                    order.save()
                except MedicineOrder.DoesNotExist:
                    messages.error(request, "Order not found.")
                except ValueError:
                    messages.error(request, "Invalid quantity entered.")

        data = MedicineOrder.objects.filter(uid=user)

        return render(
            request,
            'User/ph_givenMedicine.html',
            {'data': data}
        )
    except Exception as e:
        messages.error(request, "Error processing your request.")
        return redirect('/userHome')
# ------------------------------------------------------------------------------------

def user_payment_page(request):
    mid = request.GET['mid']
    product = MedicineOrder.objects.select_related("mid").get(id=mid)
    if product.qty is None or product.qty <= 0:
        product.qty = 1
    if product.total is None:
        product.total = product.qty * product.mid.price
    MedicineOrder.objects.filter(id=product.id).update(qty=product.qty, total=product.total)
    if request.POST:
        MedicineOrder.objects.filter(id=mid).update(
            qty=product.qty,
            total=product.total,
            status="Paid",
        )
        # return redirect("/userHome")
    return render(request,'User/user_payment_page.html',{'product':product})



def user_viewMedicine(request):
    base_qs = Medicine.objects.all()
    data, filters = apply_medicine_filters(request, base_qs)
    places = get_medicine_place_options(base_qs)
    context = {"data": data, "places": places}
    context.update(filters)
    return render(request, 'User/user_viewMedicine.html', context)


def user_viewMedicineDetails(request):
    id=request.GET['id']
    data=Medicine.objects.filter(id=id)
    return render(request,'User/user_viewMedicineDetails.html',{'data':data})






def medicine_payment(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        cus = get_or_create_user(uid)
        pro = MedicineOrder.objects.filter(uid=cus)

        if request.method == "POST":
            try:
                qty = int(request.POST.get('qty', 0))
                id = request.POST.get('id')

                if not id or qty <= 0:
                    messages.error(request, "Invalid input. Please enter a valid quantity.")
                    return redirect('/medicine_payment')

                cart_item = MedicineOrder.objects.get(id=id)
                product = cart_item.mid
                if product.qty is None:
                    messages.error(request, f"Stock information is unavailable for {product.name}.")
                elif qty > product.qty:
                    messages.error(request, f"Only {product.qty} items are available in stock for {product.name}.")
                else:
                    with transaction.atomic(): 
                        total = qty * int(product.price)
                        cart_item.qty = qty
                        cart_item.total = total
                        cart_item.status = "Paid"
                        cart_item.save()

                        product.qty -= qty
                        product.save()

                        messages.success(request, f"Order placed successfully for {product.name}! Remaining stock: {product.qty}")
            except ValueError:
                messages.error(request, "Invalid quantity entered.")
            except MedicineOrder.DoesNotExist:
                messages.error(request, "The selected product does not exist.")
            return redirect('/medicine_payment')
        return render(request, 'User/medicine_payment.html', {'pro': pro})
    except Exception as e:
        messages.error(request, "Error processing payment.")
        return redirect('/userHome')


from django.shortcuts import render, redirect
from .models import MedicineOrder, Medicine

# def place_order(request):
#     uid = request.session['uid']
#     user = User.objects.get(loginId=uid)
#     pro = MedicineOrder.objects.filter(uid=user)
#     ph=Pharmacist.objects.all()
#     if request.method == "POST":
#         pharmacist_id=request.POST.get('pharmacist_id')
#         medicine_id = request.POST.get("medicine_id")
#         qty = int(request.POST.get("qty"))
#         pharmacist = Pharmacist.objects.get(id=pharmacist_id)
#         medicine = Medicine.objects.get(id=medicine_id)

#         order = MedicineOrder.objects.create(
#             uid=user, mid=medicine, qty=qty, pharmacist=pharmacist, status="pending_pharmacist"
#         )

#         return redirect("/userHome")  # Redirect user to their orders page

#     medicines = Medicine.objects.all()
#     return render(request, "user/place_order.html", {"medicines": medicines,"ph":ph})

# from django.shortcuts import render, redirect
# from pharmacyapp.models import MedicineOrder, Medicine, Pharmacist, User

def place_order(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        user = get_or_create_user(uid)
        ph = Pharmacist.objects.all()  # Fetch all pharmacists
        medicines = Medicine.objects.all()  # Fetch all medicines

        if request.method == "POST":
            try:
                pharmacist_id = request.POST.get('pharmacist_id')
                medicine_id = request.POST.get("medicine_id")
                qty = int(request.POST.get("qty", 0))

                if not pharmacist_id or not medicine_id or qty <= 0:
                    messages.error(request, "Invalid input. Please select a valid pharmacist, medicine, and quantity.")
                    return redirect('/place_order')

                pharmacist = Pharmacist.objects.get(id=pharmacist_id)
                medicine = Medicine.objects.get(id=medicine_id)

                # Create Medicine Order
                order = MedicineOrder.objects.create(
                    uid=user, mid=medicine, qty=qty, Pharmacist=pharmacist, status="pending_pharmacist"
                )
                messages.success(request, "Order placed successfully!")
                return redirect("/userHome")  # Redirect user to their orders page
            except Pharmacist.DoesNotExist:
                messages.error(request, "Selected pharmacist not found.")
            except Medicine.DoesNotExist:
                messages.error(request, "Selected medicine not found.")
            except ValueError:
                messages.error(request, "Invalid quantity entered.")
            except Exception as e:
                messages.error(request, "Error placing order.")
            return redirect('/place_order')

        return render(request, "User/place_order.html", {"medicines": medicines, "ph": ph})
    except Exception as e:
        messages.error(request, "Error processing your request.")
        return redirect('/userHome')


def confirmorder(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')
    
    try:
        user = get_or_create_user(uid)
        orders = MedicineOrder.objects.filter(uid=user, status="Paid")
        return render(request, "User/confirmorder.html", {"orders": orders})
    except Exception as e:
        messages.error(request, "Error retrieving orders.")
        return redirect('/userHome')

def confirm_payment(request, order_id):
    try:
        order = MedicineOrder.objects.get(id=order_id, status="waiting_payment")
        order.status = "Paid"
        order.save()
        messages.success(request, "Payment successful!")
    except MedicineOrder.DoesNotExist:
        messages.error(request, "Invalid order.")

    return redirect("/userHome")


def invoice(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('/login')  # Redirect to login if uid is not in session

    try:
        user = get_or_create_user(uid)
        invoice = MedicineOrder.objects.filter(uid=user).order_by('-id')
    except Exception as e:
        messages.error(request, "Error retrieving invoices.")
        return redirect('/userHome')

    if not invoice.exists():
        return render(request, 'User/Invoice_details.html', {'invoice': [], 'message': 'No invoices found.'})

    return render(request, 'User/Invoice_details.html', {'invoice': invoice})

def invoice_detail(request, id):
    invoice = MedicineOrder.objects.get(id=id)
    return render(request, 'User/invoice_print.html', {'invoice': invoice})


def _save_care_image_analysis(chat_session, uploaded_file):
    care_summary = _update_chat_session_summary(chat_session)
    uploaded_file.seek(0)
    image_bytes = uploaded_file.read()
    uploaded_file.seek(0)
    analysis = analyze_care_image(
        image_bytes,
        getattr(uploaded_file, "name", ""),
        care_summary,
    )
    chat_session.care_image = uploaded_file
    chat_session.visual_analysis_label = analysis.get("label", "")
    chat_session.visual_analysis_summary = analysis.get("summary", "")
    chat_session.visual_analysis_details = analysis.get("details", "")
    chat_session.save(
        update_fields=[
            "care_image",
            "visual_analysis_label",
            "visual_analysis_summary",
            "visual_analysis_details",
            "updated_at",
        ]
    )
    return analysis


@xframe_options_sameorigin
def care_report(request):
    uid = request.session.get("uid")
    if not uid:
        return redirect("/login/")

    user = get_or_create_user(uid)
    chat_session = _get_requested_chat_session(request, user)
    _mark_doctor_messages_as_read(chat_session)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "analyze_image":
            uploaded_file = request.FILES.get("care_image")
            if not uploaded_file:
                messages.error(request, "Please choose an image before running photo review.")
            else:
                analysis = _save_care_image_analysis(chat_session, uploaded_file)
                _reset_doctor_approvals(chat_session)
                if analysis.get("summary"):
                    messages.success(request, "Photo review updated for this care report.")
                else:
                    messages.error(request, "The image could not be analyzed clearly.")
        elif action == "send_to_doctor":
            edited_summary = (request.POST.get("edited_summary") or "").strip()
            current_summary_text = _doctor_summary_text(chat_session)
            fields_to_update = []
            summary_changed = bool(edited_summary and edited_summary != current_summary_text)

            if summary_changed:
                chat_session.doctor_summary_override = edited_summary
                fields_to_update.insert(0, "doctor_summary_override")
                if chat_session.doctor_approved_summary:
                    chat_session.doctor_approved_summary = False
                    fields_to_update.insert(0, "doctor_approved_summary")

            target_doctor = _recommended_doctor_for_session(chat_session)
            if not target_doctor:
                if fields_to_update:
                    fields_to_update.append("updated_at")
                    chat_session.save(update_fields=list(dict.fromkeys(fields_to_update)))
                messages.error(request, "No doctor match is ready yet. Add a bit more symptom detail first.")
            else:
                if chat_session.linked_doctor_id != target_doctor.id:
                    chat_session.linked_doctor = target_doctor
                    fields_to_update.insert(0, "linked_doctor")
                    if chat_session.doctor_approved_summary:
                        chat_session.doctor_approved_summary = False
                        fields_to_update.insert(0, "doctor_approved_summary")
                    if chat_session.doctor_approved_medicine:
                        chat_session.doctor_approved_medicine = False
                        fields_to_update.insert(0, "doctor_approved_medicine")

                fields_to_update.append("updated_at")
                chat_session.save(update_fields=list(dict.fromkeys(fields_to_update)))
                messages.success(
                    request,
                    f"Care summary sent directly to Dr. {target_doctor.name} in the doctor portal.",
                )
            return redirect(_care_report_url(chat_session.id))
        return redirect(_care_report_url(chat_session.id))

    report_payload = _build_care_report_payload(chat_session)
    chat_payload = _build_chat_view_payload(chat_session)
    return render(
        request,
        "User/care_report.html",
        {
            "active_chat_session": chat_session,
            "chat_history": chat_payload["chat_history"],
            "chat_state": chat_payload,
            **report_payload,
        },
    )

@xframe_options_sameorigin
def chat(request):
    uid = request.session.get("uid")
    if not uid:
        return redirect("/login/")

    user = get_or_create_user(uid)
    chat_session = _get_requested_chat_session(request, user)
    _mark_doctor_messages_as_read(chat_session)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "clear":
            _close_chat_session(chat_session)
            chat_session = _create_chat_session(user)
            _set_active_chat_session_id(request, chat_session.id)
            if _is_ajax_request(request):
                return JsonResponse({"ok": True, **_build_chat_view_payload(chat_session)})
        elif action == "analyze_image":
            uploaded_file = request.FILES.get("care_image")
            if not uploaded_file:
                if _is_ajax_request(request):
                    return JsonResponse(
                        {"ok": False, "error": "Please choose an image before running photo review."},
                        status=400,
                    )
                messages.error(request, "Please choose an image before running photo review.")
            else:
                analysis = _save_care_image_analysis(chat_session, uploaded_file)
                _reset_doctor_approvals(chat_session)
                if _is_ajax_request(request):
                    if analysis.get("summary"):
                        return JsonResponse({"ok": True, **_build_chat_view_payload(chat_session)})
                    return JsonResponse(
                        {"ok": False, "error": "The image could not be analyzed clearly."},
                        status=400,
                    )
                if analysis.get("summary"):
                    messages.success(request, "Photo review updated in Care Chat.")
                else:
                    messages.error(request, "The image could not be analyzed clearly.")
        else:
            message_text = (request.POST.get("message") or "").strip()
            if message_text:
                classification = classify_message(message_text)
                existing_user_messages = list(
                    chat_session.messages.filter(role="user").values_list("text", flat=True)
                )
                transient_summary = build_care_summary(existing_user_messages + [message_text])
                recommended_doctors, has_specialty_match = _recommended_doctors_for_chat(
                    transient_summary["recommended_specialty"],
                    transient_summary["symptoms_display"],
                )
                assistant_text = _compose_chat_assistant_reply(
                    message_text,
                    transient_summary,
                    recommended_doctors,
                    has_specialty_match,
                )
                CareChatMessage.objects.create(
                    session=chat_session,
                    role="user",
                    text=message_text,
                    detected_intent=classification["intent"],
                    confidence=classification["confidence"],
                )
                CareChatMessage.objects.create(
                    session=chat_session,
                    role="assistant",
                    text=assistant_text,
                    detected_intent=classification["intent"],
                    confidence=classification["confidence"],
                )
                _reset_doctor_approvals(chat_session)
                if _is_ajax_request(request):
                    return JsonResponse({"ok": True, **_build_chat_view_payload(chat_session)})
                _update_chat_session_summary(chat_session)
            elif _is_ajax_request(request):
                return JsonResponse(
                    {"ok": False, "error": "Please type a message before sending."},
                    status=400,
                )
        return redirect("/chat/")

    chat_payload = _build_chat_view_payload(chat_session)
    report_payload = _build_care_report_payload(chat_session)
    return render(
        request,
        "User/care_report.html",
        {
            "active_chat_session": chat_session,
            "chat_history": chat_payload["chat_history"],
            "chat_state": chat_payload,
            **report_payload,
        },
    )






@admin_required
def expiredStock(request):
    data = Medicine.objects.filter(expiry__lt=now().date())
    return render(request, 'Admin/expiredStock.html', {'data': data})

# Feedback views
def add_feedback(request):
    uid = request.session.get('uid')
    if not uid:
        return redirect('login')

    user = get_or_create_user(uid)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')

        Feedback.objects.create(
            user=user,
            feedback_text=feedback_text,
            rating=rating
        )

        messages.success(request, 'Feedback submitted successfully!')
        return redirect('/add_feedback')  # reload page to show new feedback

    # 🔹 Fetch feedbacks (all or user-specific)
    feedbacks = Feedback.objects.select_related('user').order_by('-date_submitted')

    return render(request, 'User/add_feedback.html', {
        'feedbacks': feedbacks
    })


@admin_required
def view_feedbacks(request):
    feedbacks = Feedback.objects.select_related('user').order_by('-date_submitted')
    return render(request, 'Admin/view_feedbacks.html', {
        'feedbacks': feedbacks
    })
