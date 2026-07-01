import tempfile

from datetime import date, timedelta

from django.contrib.auth import authenticate
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from .chatbot_service import build_care_summary, generate_reply
from .models import (
    Appointments,
    CareChatMessage,
    CareChatSession,
    Doctor,
    Login,
    Medicine,
    MedicineOrder,
    Pharmacist,
    Prescription,
    User,
)


class ChatbotServiceTests(TestCase):
    def test_emergency_messages_bypass_normal_flow(self):
        reply = generate_reply("I have chest pain and cannot breathe")
        reply_lower = reply.lower()
        self.assertTrue(
            "emergency" in reply_lower or "urgent" in reply_lower or "hospital" in reply_lower
        )

    def test_structured_summary_extracts_symptoms_and_specialty(self):
        summary = build_care_summary(["I have fever and cough for two days"])
        self.assertIn("fever", summary["symptoms"])
        self.assertIn("cough", summary["symptoms"])
        self.assertEqual(summary["recommended_specialty"], "General Physician")

    def test_symptom_reply_mentions_which_doctor_to_book(self):
        reply = generate_reply("I have fever and cough for two days")
        self.assertIn("general physician", reply.lower())

    def test_structured_summary_includes_condition_details(self):
        summary = build_care_summary(["I have dizziness and numbness in my hand"])
        self.assertEqual(summary["recommended_specialty"], "Neurologist")
        self.assertIn("brain and nerve", summary["condition_overview"].lower())

    def test_structured_summary_captures_duration_and_follow_up(self):
        summary = build_care_summary(["I have fever and cough for two days"])
        self.assertEqual(summary["duration_text"], "for two days")
        self.assertEqual(summary["condition_name"], "Respiratory concern")
        self.assertIn("breathing trouble", summary["follow_up_prompt"].lower())
        self.assertNotIn("Latest user message", summary["summary"])
        self.assertIn("Patient reports", summary["summary"])

    def test_specialty_topic_summary_handles_neuro_related_language(self):
        summary = build_care_summary(["This feels neuro related and may be a nerve problem"])
        self.assertEqual(summary["recommended_specialty"], "Neurologist")
        self.assertEqual(summary["condition_name"], "Neurology-related concern")
        self.assertIn("neurology", summary["symptoms_display"].lower())

    def test_specialty_topic_reply_avoids_generic_fallback(self):
        reply = generate_reply("This feels neuro related and I need the correct doctor")
        self.assertIn("neurologist", reply.lower())
        self.assertNotIn("could not fully understand", reply.lower())

    def test_ent_summary_requests_specific_part_before_detail(self):
        summary = build_care_summary(["This is ENT related"])
        self.assertEqual(summary["recommended_specialty"], "ENT")
        self.assertEqual(summary["condition_name"], "Ear, nose, and throat concern")
        self.assertIn("ear, nose or sinus, or throat or tonsil", summary["follow_up_prompt"].lower())

    def test_ent_summary_narrows_to_ear_after_follow_up(self):
        summary = build_care_summary(["This is ENT related", "ear"])
        self.assertEqual(summary["recommended_specialty"], "ENT")
        self.assertEqual(summary["focused_area_label"], "Ear")
        self.assertEqual(summary["condition_name"], "Ear-related concern")
        self.assertIn("ear symptoms", summary["symptoms_display"].lower())
        self.assertIn("ear symptoms", summary["summary"].lower())

    def test_summary_includes_medicine_guidance_for_fever_pattern(self):
        summary = build_care_summary(["I have fever and cough for two days"])
        self.assertIn("paracetamol", summary["medicine_guidance"].lower())
        self.assertIn("doctor", summary["medicine_guidance"].lower())
        self.assertNotIn("medicine support", summary["summary"].lower())

    def test_eye_summary_routes_to_ophthalmologist_with_eye_medicine_guidance(self):
        summary = build_care_summary(["I have red eyes and blurry vision since yesterday"])
        self.assertEqual(summary["recommended_specialty"], "Ophthalmologist")
        self.assertEqual(summary["condition_name"], "Eye-related concern")
        self.assertIn("eye", summary["symptoms_display"].lower())
        self.assertIn("eye drops", summary["medicine_guidance"].lower())
        self.assertIn("ophthalmologist", summary["medicine_guidance"].lower())

    def test_body_pain_summary_uses_orthopedic_medicine_guidance(self):
        summary = build_care_summary(["I have joint pain and body ache after lifting weight"])
        self.assertEqual(summary["recommended_specialty"], "Orthopedic Specialist")
        self.assertIn("ibuprofen", summary["medicine_guidance"].lower())
        self.assertIn("diclofenac", summary["medicine_guidance"].lower())


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class MedicineImageTests(TestCase):
    def setUp(self):
        self.login = Login.objects.create_user(
            username="pharmacist-one",
            password="secret123",
            usertype="pharmacist",
        )
        self.pharmacist = Pharmacist.objects.create(
            loginId=self.login,
            name="Pharma One",
            email="pharma@example.com",
            phone="9999999999",
            address="Main road",
        )

    def test_generated_seeded_medicine_image_uses_neutral_fallback(self):
        medicine = Medicine.objects.create(
            pid=self.pharmacist,
            name="Paracetamol 500mg",
            price=10,
            qty=5,
            image="profile/medicine_paracetamol_500mg.png",
        )

        self.assertFalse(medicine.has_exact_image)
        self.assertEqual(
            medicine.display_image_url,
            "/static/assets/images/pharmacy/shop/medicine.jpg",
        )

    def test_uploaded_pack_photo_uses_uploaded_media_url(self):
        medicine = Medicine.objects.create(
            pid=self.pharmacist,
            name="Exact Pack",
            price=25,
            qty=2,
            image=SimpleUploadedFile("exact-pack.jpg", b"fake-image", content_type="image/jpeg"),
        )

        self.assertTrue(medicine.has_exact_image)
        self.assertTrue(medicine.display_image_url.startswith("/assets/profile/exact-pack"))


class UserPaymentPageTests(TestCase):
    def setUp(self):
        self.user_login = Login.objects.create_user(
            username="buyer@example.com",
            password="secret123",
            usertype="User",
        )
        self.user = User.objects.create(
            loginId=self.user_login,
            name="Buyer",
            email="buyer@example.com",
        )
        self.pharmacist_login = Login.objects.create_user(
            username="pharmacist-two",
            password="secret123",
            usertype="Pharmacist",
        )
        self.pharmacist = Pharmacist.objects.create(
            loginId=self.pharmacist_login,
            name="Pharma Two",
            email="pharma2@example.com",
            phone="9999999998",
            address="Main road",
            pharmacy_name="Medi Two",
        )
        self.medicine = Medicine.objects.create(
            pid=self.pharmacist,
            name="Nitroglycerin",
            price=155,
            qty=444,
            desc="For angina relief",
        )

    def test_payment_page_backfills_missing_order_qty_and_total(self):
        order = MedicineOrder.objects.create(
            uid=self.user,
            mid=self.medicine,
            status="in_cart",
        )

        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.get(f"/user_payment_page/?mid={order.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Price per unit: ₹155")
        self.assertContains(response, "Selected Quantity: 1")
        self.assertContains(response, "Pay ₹155")

        order.refresh_from_db()
        self.assertEqual(order.qty, 1)
        self.assertEqual(order.total, 155)


class PortalPasswordChangeTests(TestCase):
    def setUp(self):
        self.user_login = Login.objects.create_user(
            username="user@example.com",
            password="OldSecret123!",
            usertype="User",
            view_password="OldSecret123!",
        )
        self.user = User.objects.create(
            loginId=self.user_login,
            name="Portal User",
            email="user@example.com",
        )

        self.doctor_login = Login.objects.create_user(
            username="doctor@example.com",
            password="OldSecret123!",
            usertype="Doctor",
            view_password="OldSecret123!",
        )
        self.doctor = Doctor.objects.create(
            loginId=self.doctor_login,
            name="Portal Doctor",
            email="doctor@example.com",
            phone="9999999999",
            address="Clinic Road",
            specialization="General Physician",
        )

        self.pharmacist_login = Login.objects.create_user(
            username="pharma@example.com",
            password="OldSecret123!",
            usertype="Pharmacist",
            view_password="OldSecret123!",
        )
        self.pharmacist = Pharmacist.objects.create(
            loginId=self.pharmacist_login,
            name="Portal Pharmacist",
            email="pharma@example.com",
            phone="8888888888",
            address="Pharmacy Road",
            pharmacy_license_number="LIC-100",
            pharmacy_name="Good Health Pharmacy",
        )

    def _set_session_uid(self, login_obj):
        session = self.client.session
        session["uid"] = login_obj.id
        session.save()

    def test_user_can_change_password_from_profile(self):
        self._set_session_uid(self.user_login)

        response = self.client.post(
            "/change_user_password/",
            {
                "current_password": "OldSecret123!",
                "new_password": "NewSecret123!",
                "confirm_password": "NewSecret123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/UserProfile")

        self.user_login.refresh_from_db()
        self.assertTrue(self.user_login.check_password("NewSecret123!"))
        self.assertEqual(self.user_login.view_password, "NewSecret123!")
        self.assertIsNotNone(authenticate(username="user@example.com", password="NewSecret123!"))

    def test_doctor_password_change_rejects_wrong_current_password(self):
        self._set_session_uid(self.doctor_login)

        response = self.client.post(
            "/change_doctor_password/",
            {
                "current_password": "WrongSecret123!",
                "new_password": "DoctorNew123!",
                "confirm_password": "DoctorNew123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/DoctorProfile")

        self.doctor_login.refresh_from_db()
        self.assertTrue(self.doctor_login.check_password("OldSecret123!"))
        self.assertIsNone(authenticate(username="doctor@example.com", password="DoctorNew123!"))

    def test_pharmacist_can_change_password_from_profile(self):
        self._set_session_uid(self.pharmacist_login)

        response = self.client.post(
            "/change_pharmacist_password/",
            {
                "current_password": "OldSecret123!",
                "new_password": "PharmaNew123!",
                "confirm_password": "PharmaNew123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/pharmacist_Profile")

        self.pharmacist_login.refresh_from_db()
        self.assertTrue(self.pharmacist_login.check_password("PharmaNew123!"))
        self.assertEqual(self.pharmacist_login.view_password, "PharmaNew123!")
        self.assertIsNotNone(authenticate(username="pharma@example.com", password="PharmaNew123!"))


class ChatPersistenceTests(TestCase):
    def setUp(self):
        self.login = Login.objects.create_user(
            username="chatuser",
            password="secret123",
            usertype="user",
        )
        self.user = User.objects.create(
            loginId=self.login,
            name="Chat User",
            email="chat@example.com",
        )

    def test_chat_requires_login_session(self):
        response = self.client.get("/chat/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")

    def test_chat_post_saves_conversation_to_database(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        response = self.client.post("/chat/", {"message": "How do I view my prescription?"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.get(user=self.user)
        messages = list(chat_session.messages.values_list("role", "text"))

        self.assertEqual(messages[0][0], "assistant")
        self.assertEqual(messages[1][0], "user")
        self.assertEqual(messages[1][1], "How do I view my prescription?")
        self.assertEqual(messages[2][0], "assistant")
        self.assertTrue(chat_session.last_user_message)
        self.assertTrue(chat_session.symptom_summary)

    def test_chat_ajax_post_returns_json_state(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        response = self.client.post(
            "/chat/",
            {"message": "I have fever and cough for two days"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["care_summary"]["recommended_specialty"], "General Physician")
        self.assertEqual(payload["chat_history"][-2]["role"], "user")
        self.assertEqual(payload["chat_history"][-1]["role"], "assistant")
        self.assertIn("summary_booking_url", payload)
        self.assertIn("care_report_url", payload)
        self.assertIn("doctor_summary_text", payload)
        self.assertNotIn("Latest user message", payload["doctor_summary_text"])

    def test_follow_up_portal_question_does_not_repeat_symptom_reply(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        self.client.post("/chat/", {"message": "I have fever and cough for two days"})
        response = self.client.post("/chat/", {"message": "How do I view my prescription?"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        self.assertIn("prescription", assistant_message.text.lower())
        self.assertNotIn("for now, rest", assistant_message.text.lower())

    def test_ok_follow_up_gets_contextual_reply_instead_of_generic_fallback(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        self.client.post("/chat/", {"message": "I have fever and cough for two days"})
        response = self.client.post("/chat/", {"message": "ok"})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        assistant_text = assistant_message.text.lower()
        self.assertNotIn("could not fully understand", assistant_text)
        self.assertTrue("if you want" in assistant_text or "you can ask" in assistant_text)
        self.assertTrue(
            "precautions" in assistant_text
            or "medicines" in assistant_text
            or "doctor" in assistant_text
        )

    def test_ok_as_first_message_prompts_for_symptom_detail(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        response = self.client.post("/chat/", {"message": "ok"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        assistant_text = assistant_message.text.lower()
        self.assertNotIn("could not fully understand", assistant_text)
        self.assertTrue("tell me" in assistant_text or "share the symptom" in assistant_text)

    def test_general_portal_help_does_not_set_default_doctor(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        response = self.client.post(
            "/chat/",
            {"message": "How do I view my prescription?"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["recommended_doctors"], [])
        self.assertIsNone(payload["top_recommended_doctor"])

    def test_care_report_page_loads_for_active_chat(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        self.client.post("/chat/", {"message": "I have fever and cough for two days"})
        response = self.client.get("/care-report/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Care Report")
        self.assertContains(response, "Data Shared With Doctor")

    def test_clear_chat_archives_previous_session_and_starts_new_one(self):
        session = self.client.session
        session["uid"] = self.login.id
        session.save()

        self.client.post("/chat/", {"message": "I have headache"})
        old_session = CareChatSession.objects.get(user=self.user, is_active=True)

        response = self.client.post("/chat/", {"action": "clear"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        old_session.refresh_from_db()
        self.assertFalse(old_session.is_active)

        new_session = CareChatSession.objects.filter(user=self.user, is_active=True).exclude(id=old_session.id).get()
        self.assertEqual(new_session.messages.count(), 1)
        self.assertEqual(new_session.messages.first().role, "assistant")


class AppointmentChatIntegrationTests(TestCase):
    def setUp(self):
        self.user_login = Login.objects.create_user(
            username="patient",
            password="secret123",
            usertype="user",
        )
        self.user = User.objects.create(
            loginId=self.user_login,
            name="Patient One",
            email="patient@example.com",
        )

        self.doctor_login = Login.objects.create_user(
            username="doctor",
            password="secret123",
            usertype="doctor",
        )
        self.doctor = Doctor.objects.create(
            loginId=self.doctor_login,
            name="Dr Example",
            email="doctor@example.com",
            phone="1234567890",
            address="Clinic street",
            specialization="General Physician",
        )
        self.skin_doctor_login = Login.objects.create_user(
            username="skin-doctor",
            password="secret123",
            usertype="doctor",
        )
        self.skin_doctor = Doctor.objects.create(
            loginId=self.skin_doctor_login,
            name="Dr Skin",
            email="skin@example.com",
            phone="9999999999",
            address="Skin clinic",
            specialization="Dermatologist",
        )
        self.neuro_login = Login.objects.create_user(
            username="rahul-neuro",
            password="secret123",
            usertype="doctor",
        )
        self.neuro_doctor = Doctor.objects.create(
            loginId=self.neuro_login,
            name="Rahul K",
            email="rahul@example.com",
            phone="8888888888",
            address="Kottayam",
            specialization="Neurologist",
        )
        self.ent_login = Login.objects.create_user(
            username="manu-ent",
            password="secret123",
            usertype="doctor",
        )
        self.ent_doctor = Doctor.objects.create(
            loginId=self.ent_login,
            name="Manu",
            email="manu@example.com",
            phone="7777777777",
            address="Kochi",
            specialization="ENT",
        )
        self.eye_doctor_login = Login.objects.create_user(
            username="harold-eye",
            password="secret123",
            usertype="doctor",
        )
        self.eye_doctor = Doctor.objects.create(
            loginId=self.eye_doctor_login,
            name="Harold",
            email="harold@example.com",
            phone="6666666666",
            address="Thrissur",
            specialization="Ophthalmologist",
        )
        self.pharmacist_login = Login.objects.create_user(
            username="pharmacist",
            password="secret123",
            usertype="pharmacist",
        )
        self.pharmacist = Pharmacist.objects.create(
            loginId=self.pharmacist_login,
            name="Pharma One",
            email="pharma@example.com",
            phone="5555555555",
            address="Kochi",
            pharmacy_name="Medi Pharmacy",
        )
        self.admin_login = Login.objects.create_user(
            username="admin-test",
            password="secret123",
            usertype="admin",
        )

    def _create_saved_chat_session(self):
        chat_session = CareChatSession.objects.create(
            user=self.user,
            title="Fever concern",
            symptom_summary="Reported symptoms: fever, cough. Latest user message: I have fever and cough",
            structured_symptoms="fever, cough",
            recommended_specialty="General Physician",
            urgency_level="routine",
            last_user_message="I have fever and cough",
            is_active=True,
        )
        CareChatMessage.objects.create(session=chat_session, role="assistant", text="Hello")
        CareChatMessage.objects.create(session=chat_session, role="user", text="I have fever and cough")
        CareChatMessage.objects.create(session=chat_session, role="assistant", text="Please monitor your symptoms.")
        return chat_session

    def _create_neuro_chat_session(self):
        chat_session = CareChatSession.objects.create(
            user=self.user,
            title="Neuro concern",
            symptom_summary="Reported symptoms: neuro symptoms, headache. Latest user message: I have dizziness and numbness",
            structured_symptoms="neuro symptoms, headache",
            recommended_specialty="Neurologist",
            urgency_level="routine",
            last_user_message="I have dizziness and numbness",
            is_active=True,
        )
        CareChatMessage.objects.create(session=chat_session, role="assistant", text="Hello")
        CareChatMessage.objects.create(session=chat_session, role="user", text="I have dizziness and numbness")
        CareChatMessage.objects.create(session=chat_session, role="assistant", text="Please book Rahul K.")
        return chat_session

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_care_report_image_upload_saves_visual_review(self):
        import tensorflow as tf

        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "I have a skin rash on my arm"})
        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()

        image_tensor = tf.constant([[[220, 40, 40], [230, 55, 55]], [[220, 35, 35], [240, 70, 70]]], dtype=tf.uint8)
        image_bytes = tf.io.encode_png(image_tensor).numpy()
        upload = SimpleUploadedFile("rash.png", image_bytes, content_type="image/png")

        response = self.client.post(
            "/care-report/",
            {
                "action": "analyze_image",
                "chat_session_id": chat_session.id,
                "care_image": upload,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/care-report/", response.url)

        chat_session.refresh_from_db()
        self.assertTrue(bool(chat_session.visual_analysis_label))
        self.assertTrue(bool(chat_session.visual_analysis_summary))
        self.assertTrue(bool(chat_session.care_image))

    def test_booking_can_attach_saved_chat_session(self):
        chat_session = self._create_saved_chat_session()

        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.post(
            "/book_appoinment/",
            {
                "dr": self.doctor.id,
                "date": str(date.today() + timedelta(days=1)),
                "time": "10:30",
                "desc": "Need doctor review",
                "attach_chat_summary": "1",
                "chat_session_id": chat_session.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/userHome")

        appointment = Appointments.objects.get(uid=self.user, did=self.doctor)
        self.assertEqual(appointment.chat_session, chat_session)

        chat_session.refresh_from_db()
        self.assertEqual(chat_session.linked_doctor, self.doctor)
        self.assertFalse(chat_session.is_active)

    def test_chat_page_shows_matching_doctor_recommendations(self):
        self._create_saved_chat_session()

        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.get("/chat/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr Example")

    def test_neuro_chat_page_mentions_rahul_k_and_condition_guidance(self):
        neuro_session = self._create_neuro_chat_session()

        session = self.client.session
        session["uid"] = self.user_login.id
        session["active_chat_session_id"] = neuro_session.id
        session.save()

        response = self.client.get("/chat/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rahul K")
        self.assertContains(response, "Neurology-related concern")

    def test_booking_page_prefills_recommended_doctor(self):
        chat_session = self._create_saved_chat_session()

        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.get(f"/book_appoinment/?chat_session_id={chat_session.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr Example - General Physician (Recommended)")

    def test_booking_page_does_not_auto_select_doctor(self):
        chat_session = self._create_saved_chat_session()

        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.get(f"/book_appoinment/?chat_session_id={chat_session.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_doctor_id"], "")

    def test_chat_post_creates_doctor_named_reply_for_neuro_symptoms(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.post("/chat/", {"message": "I have dizziness and numbness in my hand"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        self.assertIn("Rahul K", assistant_message.text)
        self.assertIn("Neurology-related concern", assistant_message.text)

    def test_chat_post_reply_uses_symptom_details_instead_of_generic_block(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "I have fever and cough for two days"})
        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()

        self.assertIn("fever", assistant_message.text.lower())
        self.assertIn("cough", assistant_message.text.lower())
        self.assertIn("for two days", assistant_message.text.lower())
        self.assertIn("for now", assistant_message.text.lower())
        self.assertIn("general physician", assistant_message.text.lower())

    def test_chat_post_medicine_question_uses_condition_specific_guidance(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.post("/chat/", {"message": "What medicine can I take for fever and cough?"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        self.assertTrue(
            "medicine support" in assistant_message.text.lower()
            or "medicines to discuss with your doctor" in assistant_message.text.lower()
        )
        self.assertIn("paracetamol", assistant_message.text.lower())
        self.assertIn("doctor", assistant_message.text.lower())

    def test_chat_post_uses_specialty_hint_for_neuro_related_query(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.post("/chat/", {"message": "This feels neuro related. Which doctor should I book?"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        self.assertIn("Rahul K", assistant_message.text)
        self.assertIn("Neurology-related concern", assistant_message.text)
        self.assertNotIn("could not fully understand", assistant_message.text.lower())

    def test_chat_post_generic_ent_message_asks_for_specific_part(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.post("/chat/", {"message": "This is ENT related"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()
        assistant_text = assistant_message.text.lower()
        self.assertTrue(
            "ent concern" in assistant_text
            or "ear, nose, and throat concern" in assistant_text
        )
        self.assertIn("ear, nose or sinus, or throat or tonsil", assistant_text)

    def test_chat_post_ent_follow_up_focuses_on_ear_and_updates_doctor_summary(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "This is ENT related"})
        response = self.client.post("/chat/", {"message": "ear"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        assistant_message = chat_session.messages.filter(role="assistant").order_by("-id").first()

        self.assertIn("ear-related concern", assistant_message.text.lower())
        self.assertIn("ear", chat_session.symptom_summary.lower())
        self.assertNotIn("latest user message", chat_session.symptom_summary.lower())
        self.assertEqual(chat_session.recommended_specialty, "ENT")

        report_response = self.client.get("/care-report/")
        self.assertEqual(report_response.status_code, 200)
        self.assertIn("ear", report_response.context["doctor_summary_text"].lower())

    def test_eye_chat_recommends_ophthalmologist_doctor_and_eye_medicines(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        response = self.client.post(
            "/chat/",
            {"message": "My eyes are red, dry, and blurry since yesterday"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["care_summary"]["recommended_specialty"], "Ophthalmologist")
        self.assertEqual(payload["top_recommended_doctor"]["name"], "Harold")
        self.assertIn("eye drops", payload["medicine_guidance_text"].lower())

    def test_care_report_precautions_change_with_matched_doctor(self):
        neuro_session = self._create_neuro_chat_session()

        session = self.client.session
        session["uid"] = self.user_login.id
        session["active_chat_session_id"] = neuro_session.id
        session.save()

        response = self.client.get("/care-report/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any("Rahul K" in item for item in response.context["precautions"]))

    def test_care_report_send_to_doctor_stays_on_report_and_links_doctor(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "I have dizziness and numbness in my hand"})
        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()

        response = self.client.post(
            "/care-report/",
            {
                "action": "send_to_doctor",
                "chat_session_id": chat_session.id,
                "edited_summary": "Short neuro summary for doctor review.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/care-report/", response.url)

        chat_session.refresh_from_db()
        self.assertEqual(chat_session.linked_doctor, self.neuro_doctor)
        self.assertEqual(chat_session.doctor_summary_override, "Short neuro summary for doctor review.")

    def test_doctor_portal_shows_direct_care_chat_submission(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "I have dizziness and numbness in my hand"})
        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        self.client.post(
            "/care-report/",
            {
                "action": "send_to_doctor",
                "chat_session_id": chat_session.id,
                "edited_summary": "Short neuro summary for doctor review.",
            },
        )

        session = self.client.session
        session["uid"] = self.neuro_login.id
        session.save()

        response = self.client.get("/doctor_patient_chats/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient One")
        self.assertContains(response, "Direct care chat")
        self.assertContains(response, "Short neuro summary for doctor review.")
        self.assertContains(response, "AI medicine support")

    def test_user_prescription_pages_show_ai_medicine_support(self):
        chat_session = self._create_neuro_chat_session()
        Prescription.objects.create(
            uid=self.user,
            doctor=self.neuro_doctor,
            pharmacist=self.pharmacist,
            medicines="Paracetamol",
            instructions="Take after food",
        )

        session = self.client.session
        session["uid"] = self.user_login.id
        session["active_chat_session_id"] = chat_session.id
        session.save()

        list_response = self.client.get("/view_prescription/")
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "AI medicine support")
        self.assertContains(list_response, "paracetamol")

        prescription = Prescription.objects.filter(uid=self.user).first()
        detail_response = self.client.get(f"/view_prescription_detail/{prescription.id}/")
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "AI Medicine Support")
        self.assertContains(detail_response, "paracetamol")

    def test_doctor_prescription_page_shows_ai_medicine_support(self):
        chat_session = self._create_neuro_chat_session()
        appointment = Appointments.objects.create(
            uid=self.user,
            did=self.neuro_doctor,
            date=date.today() + timedelta(days=1),
            time="10:00",
            desc="Neuro review",
            status="Accepted",
            chat_session=chat_session,
        )

        session = self.client.session
        session["uid"] = self.neuro_login.id
        session.save()

        response = self.client.get(f"/prescription_patient/?id={appointment.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI medicine support")
        self.assertContains(response, "paracetamol")

    def test_pharmacist_portal_shows_ai_medicine_support(self):
        chat_session = self._create_neuro_chat_session()
        prescription = Prescription.objects.create(
            uid=self.user,
            doctor=self.neuro_doctor,
            pharmacist=self.pharmacist,
            medicines="Paracetamol",
            instructions="Take after food",
        )

        session = self.client.session
        session["uid"] = self.pharmacist_login.id
        session.save()

        list_response = self.client.get("/ph_view_prescription/")
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "AI Medicine Support")
        self.assertContains(list_response, "paracetamol")

        sale_response = self.client.get(f"/sales_Medicine/?id={prescription.id}")
        self.assertEqual(sale_response.status_code, 200)
        self.assertContains(sale_response, "AI Medicine Support")
        self.assertContains(sale_response, "paracetamol")

    def test_admin_user_list_shows_ai_medicine_support(self):
        self._create_neuro_chat_session()

        session = self.client.session
        session["uid"] = self.admin_login.id
        session.save()

        response = self.client.get("/admin_view_users/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI Medicine Support")
        self.assertContains(response, "paracetamol")

    def test_doctor_can_check_ai_summary_and_medicine_support(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "I have dizziness and numbness in my hand"})
        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        self.client.post(
            "/care-report/",
            {
                "action": "send_to_doctor",
                "chat_session_id": chat_session.id,
                "edited_summary": "Short neuro summary for doctor review.",
            },
        )

        session = self.client.session
        session["uid"] = self.neuro_login.id
        session.save()

        response = self.client.post(
            "/doctor_patient_chats/",
            {
                "action": "toggle_summary_approval",
                "chat_session_id": chat_session.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/doctor_patient_chats/")

        response = self.client.post(
            "/doctor_patient_chats/",
            {
                "action": "toggle_medicine_approval",
                "chat_session_id": chat_session.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/doctor_patient_chats/")

        chat_session.refresh_from_db()
        self.assertTrue(chat_session.doctor_approved_summary)
        self.assertTrue(chat_session.doctor_approved_medicine)

        doctor_response = self.client.get("/doctor_patient_chats/")
        self.assertContains(doctor_response, "Remove Summary Check")
        self.assertContains(doctor_response, "Remove Medicine Check")
        self.assertContains(doctor_response, "Checked")
        self.assertNotContains(doctor_response, "Send Reply to Care Chat")

        session = self.client.session
        session["uid"] = self.user_login.id
        session["active_chat_session_id"] = chat_session.id
        session.save()

        patient_response = self.client.get("/care-report/")
        self.assertEqual(patient_response.status_code, 200)
        self.assertContains(patient_response, "Doctor checked", count=2)

    def test_new_chat_message_clears_doctor_checks(self):
        session = self.client.session
        session["uid"] = self.user_login.id
        session.save()

        self.client.post("/chat/", {"message": "I have dizziness and numbness in my hand"})
        chat_session = CareChatSession.objects.filter(user=self.user).order_by("-id").first()
        self.client.post(
            "/care-report/",
            {
                "action": "send_to_doctor",
                "chat_session_id": chat_session.id,
                "edited_summary": "Short neuro summary for doctor review.",
            },
        )

        session = self.client.session
        session["uid"] = self.neuro_login.id
        session.save()

        self.client.post(
            "/doctor_patient_chats/",
            {"action": "toggle_summary_approval", "chat_session_id": chat_session.id},
        )
        self.client.post(
            "/doctor_patient_chats/",
            {"action": "toggle_medicine_approval", "chat_session_id": chat_session.id},
        )

        chat_session.refresh_from_db()
        self.assertTrue(chat_session.doctor_approved_summary)
        self.assertTrue(chat_session.doctor_approved_medicine)

        session = self.client.session
        session["uid"] = self.user_login.id
        session["active_chat_session_id"] = chat_session.id
        session.save()

        response = self.client.post("/chat/", {"message": "Now I also have headache"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/chat/")

        chat_session.refresh_from_db()
        self.assertFalse(chat_session.doctor_approved_summary)
        self.assertFalse(chat_session.doctor_approved_medicine)

    def test_doctor_can_view_patient_chat_intakes(self):
        chat_session = self._create_saved_chat_session()
        chat_session.visual_analysis_label = "Visible redness or irritation"
        chat_session.visual_analysis_summary = "The photo shows a noticeable red or inflamed-looking surface area."
        chat_session.save(update_fields=["visual_analysis_label", "visual_analysis_summary", "updated_at"])
        Appointments.objects.create(
            uid=self.user,
            did=self.doctor,
            date=date.today() + timedelta(days=1),
            time="11:00",
            desc="Appointment note",
            status="Booked",
            chat_session=chat_session,
        )

        session = self.client.session
        session["uid"] = self.doctor_login.id
        session.save()

        response = self.client.get("/doctor_patient_chats/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient One")
        self.assertContains(response, "fever, cough")
        self.assertContains(response, "Visible redness or irritation")
