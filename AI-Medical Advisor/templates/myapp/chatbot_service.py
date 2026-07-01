from __future__ import annotations

import json
import pickle
import random
import re
from functools import lru_cache
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
INTENTS_PATH = BASE_DIR / "intents.json"
WORDS_PATH = BASE_DIR / "words.pkl"
CLASSES_PATH = BASE_DIR / "classes.pkl"
MODEL_PATHS = [
    BASE_DIR / "chatbot_model.keras",
    BASE_DIR / "chatbot_model.h5",
]

DEFAULT_WELCOME_MESSAGE = (
    "Hello. Ask about symptoms, medicines, prescriptions, appointments, or orders."
)
DEFAULT_FALLBACK_RESPONSE = (
    "I could not fully understand that. Try symptoms, medicines, prescriptions, appointments, or orders."
)
QUICK_PROMPTS = [
    "What should I do for fever?",
    "How do I view my prescription?",
    "Tell me about medicine side effects",
    "How can I track my order?",
]

IMAGE_ANALYSIS_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

SYMPTOM_KEYWORDS = {
    "fever": ("fever", "temperature", "high temp", "chills", "hot body"),
    "cough": ("cough", "cold", "sore throat", "runny nose", "stuffy nose"),
    "headache": ("headache", "migraine", "head pain", "head ache"),
    "neuro symptoms": (
        "migraine",
        "dizziness",
        "vertigo",
        "numbness",
        "tingling",
        "seizure",
        "fits",
        "tremor",
        "memory loss",
        "weak hand",
        "weak leg",
        "balance issue",
        "nerve pain",
    ),
    "eye concern": (
        "eye",
        "eyes",
        "eye pain",
        "eye redness",
        "red eye",
        "red eyes",
        "eyes red",
        "itchy eyes",
        "watery eyes",
        "watering eyes",
        "dry eye",
        "dry eyes",
        "blurred vision",
        "blurry vision",
        "blurry",
        "vision change",
        "eye discharge",
        "vision problem",
        "sensitive to light",
    ),
    "allergy": ("allergy", "allergic", "itching", "itchy", "sneezing"),
    "skin rash": ("rash", "hives", "skin reaction", "red spots"),
    "stomach pain": ("stomach", "abdomen", "abdominal", "nausea", "vomiting", "diarrhea"),
    "breathing trouble": ("shortness of breath", "breathing", "wheezing", "breathless"),
    "chest pain": ("chest pain", "tight chest", "heart pain"),
    "heart concern": ("palpitations", "heart racing", "bp", "blood pressure", "heart beat", "pulse"),
    "ent concern": (
        "ear pain",
        "ear ache",
        "ear infection",
        "sinus",
        "sinusitis",
        "tonsil",
        "throat pain",
        "nose block",
        "blocked nose",
        "hearing issue",
    ),
    "women's health": (
        "period pain",
        "irregular period",
        "pregnancy",
        "pcos",
        "ovary",
        "uterus",
        "vaginal",
        "pelvic pain",
    ),
    "stress": ("stress", "anxiety", "panic", "overwhelmed"),
    "body pain": ("body pain", "body ache", "muscle pain", "joint pain"),
}

SPECIALTY_BY_SYMPTOM = {
    "fever": "General Physician",
    "cough": "General Physician",
    "headache": "Neurologist",
    "neuro symptoms": "Neurologist",
    "eye concern": "Ophthalmologist",
    "allergy": "Allergy Specialist",
    "skin rash": "Dermatologist",
    "stomach pain": "Gastroenterologist",
    "breathing trouble": "Pulmonologist",
    "chest pain": "Emergency Care",
    "heart concern": "Cardiologist",
    "ent concern": "ENT",
    "women's health": "Gynecologist",
    "stress": "Mental Health Specialist",
    "body pain": "Orthopedic Specialist",
}

SPECIALTY_TOPIC_KEYWORDS = {
    "Neurologist": (
        "neuro",
        "neurology",
        "neurologist",
        "brain",
        "brain issue",
        "brain problem",
        "nerve",
        "nerves",
        "nerve issue",
        "nerve problem",
        "stroke",
        "paralysis",
        "face droop",
        "speech trouble",
        "memory issue",
    ),
    "Cardiologist": (
        "cardio",
        "cardiac",
        "cardiology",
        "cardiologist",
        "heart issue",
        "heart problem",
        "heart related",
        "palpitation",
    ),
    "ENT": (
        "ent",
        "ear nose throat",
        "sinus issue",
        "ear issue",
        "throat issue",
        "nose issue",
    ),
    "Gynecologist": (
        "gyno",
        "gyne",
        "gynec",
        "gynaec",
        "gynecologist",
        "gynaecologist",
        "womens health",
        "women health",
        "female problem",
    ),
    "Ophthalmologist": (
        "ophthalmologist",
        "opthalmologist",
        "ophthalmology",
        "eye specialist",
        "eye problem",
        "eye issue",
        "eye related",
        "eye concern",
        "vision issue",
        "red eye",
        "dry eye",
        "blurry vision",
    ),
    "Dermatologist": ("derma", "dermatology", "skin issue", "skin problem"),
    "Gastroenterologist": ("gastro", "gastric issue", "stomach issue", "digestive problem"),
    "Pulmonologist": ("pulmo", "lung issue", "breathing issue", "respiratory issue"),
    "Mental Health Specialist": (
        "mental health",
        "panic issue",
        "anxiety issue",
        "stress issue",
    ),
    "Orthopedic Specialist": ("ortho", "orthopedic", "bone issue", "joint issue"),
}

INTENT_SPECIALTY_HINTS = {
    "mental_health_support": "Mental Health Specialist",
    "allergy_support": "Allergy Specialist",
    "headache_support": "Neurologist",
    "cough_cold_support": "General Physician",
    "fever_support": "General Physician",
    "prescription_help": "General Physician",
    "appointment_help": "General Physician",
}

INTENTS_WITH_DOCTOR_GUIDANCE = {
    "symptom_support",
    "mental_health_support",
    "allergy_support",
    "headache_support",
    "cough_cold_support",
    "fever_support",
}

HIGH_PRIORITY_TOKENS = {
    "severe",
    "worsening",
    "worse",
    "persistent",
    "unbearable",
    "vomiting",
    "blood",
    "dizzy",
    "weakness",
}

CONDITION_PROFILE_BY_SYMPTOM = {
    "neuro symptoms": "neurology",
    "headache": "neurology",
    "heart concern": "cardiology",
    "ent concern": "ent",
    "women's health": "gynecology",
    "eye concern": "ophthalmology",
    "fever": "general_fever",
    "cough": "respiratory",
    "allergy": "allergy",
    "skin rash": "dermatology",
    "stomach pain": "gastro",
    "breathing trouble": "respiratory",
    "stress": "mental_health",
    "body pain": "orthopedic",
}

PROFILE_KEY_BY_SPECIALTY = {
    "Neurologist": "neurology",
    "Cardiologist": "cardiology",
    "ENT": "ent",
    "Gynecologist": "gynecology",
    "Ophthalmologist": "ophthalmology",
    "Allergy Specialist": "allergy",
    "Dermatologist": "dermatology",
    "Gastroenterologist": "gastro",
    "Pulmonologist": "respiratory",
    "Mental Health Specialist": "mental_health",
    "Orthopedic Specialist": "orthopedic",
}

SPECIALTY_SIGNAL_LABELS = {
    "Neurologist": "neurology / brain and nerve concern",
    "Cardiologist": "heart-related concern",
    "ENT": "ear, nose, and throat concern",
    "Gynecologist": "women's health concern",
    "Ophthalmologist": "eye-related concern",
    "Allergy Specialist": "allergy-related concern",
    "Dermatologist": "skin-related concern",
    "Gastroenterologist": "digestive concern",
    "Pulmonologist": "breathing-related concern",
    "Mental Health Specialist": "stress or anxiety-related concern",
    "Orthopedic Specialist": "bone, joint, or muscle concern",
}

CONDITION_COMBINATION_RULES = (
    ({"fever", "cough"}, "respiratory"),
    ({"fever", "breathing trouble"}, "respiratory"),
    ({"headache", "neuro symptoms"}, "neurology"),
)

SYMPTOM_DISPLAY_LABELS = {
    "fever": "fever",
    "cough": "cough",
    "headache": "headache",
    "neuro symptoms": "neurological symptoms",
    "eye concern": "eye symptoms",
    "allergy": "allergy symptoms",
    "skin rash": "skin rash",
    "stomach pain": "stomach pain",
    "breathing trouble": "breathing trouble",
    "chest pain": "chest pain",
    "heart concern": "heart-related symptoms",
    "ent concern": "ear, nose, or throat symptoms",
    "women's health": "women's health symptoms",
    "stress": "stress or anxiety symptoms",
    "body pain": "body pain",
}

DURATION_PATTERNS = (
    r"\bfor\s+(?:about\s+)?(?:a|an|\d+|one|two|three|four|five|six|seven|eight|nine|ten|few|couple of)\s+(?:hour|hours|day|days|week|weeks|month|months)\b",
    r"\bsince\s+(?:yesterday|today|last night|this morning|this afternoon|this evening|morning|afternoon|evening)\b",
    r"\b(?:started|begin|began)\s+(?:today|yesterday|last night|this morning|this afternoon|this evening)\b",
)

SEVERITY_PATTERNS = (
    ("mild", "mild"),
    ("severe", "severe"),
    ("worsening", "getting worse"),
    ("worse", "getting worse"),
    ("persistent", "persistent"),
    ("sudden", "sudden"),
    ("suddenly", "sudden"),
    ("on and off", "on and off"),
    ("constant", "constant"),
)

PROFILE_FOLLOW_UP_HINTS = {
    "neurology": "whether you also have weakness, speech trouble, vision change, or balance problems",
    "cardiology": "whether you also have chest pressure, fainting, shortness of breath, or swelling",
    "ent": "whether there is fever, discharge, blocked nose, hearing change, or throat swelling",
    "gynecology": "whether the symptoms are linked with your cycle, bleeding, discharge, or pregnancy",
    "ophthalmology": "whether there is redness, discharge, blurred vision, itching, dryness, or light sensitivity",
    "general_fever": "your temperature, when it started, and whether you also have chills, body pain, or vomiting",
    "respiratory": "whether you have fever, wheezing, mucus, sore throat, or breathing trouble",
    "allergy": "what may have triggered it and whether there is swelling, wheezing, or rash",
    "dermatology": "where the rash started, whether it is spreading, and whether it is itchy or painful",
    "gastro": "whether the pain is after food, whether there is vomiting or diarrhea, and how strong the pain is",
    "mental_health": "whether this came with poor sleep, chest tightness, panic feelings, or ongoing stress",
    "orthopedic": "whether there was an injury, swelling, stiffness, or numbness in the limb",
    "general": "the main symptom, when it started, and whether it is getting worse",
}

DOCTOR_PRECAUTION_HINTS = {
    "neurologist": "Before seeing {doctor}, note when the dizziness, numbness, weakness, speech change, or vision change started.",
    "cardiologist": "Before seeing {doctor}, note chest discomfort timing, palpitations, activity triggers, and any recent BP readings.",
    "ent": "Before seeing {doctor}, note fever, ear discharge, blocked nose, throat swelling, or hearing change.",
    "dermatologist": "Before seeing {doctor}, avoid new creams and note spread, itch, pain, or any recent medicine trigger.",
    "general physician": "Before seeing {doctor}, note your temperature, main symptoms, fluids taken, and any medicines already used.",
    "gastroenterologist": "Before seeing {doctor}, note meal triggers, vomiting, diarrhea, and where the stomach pain is felt.",
    "pulmonologist": "Before seeing {doctor}, note cough pattern, fever, wheezing, mucus, and breathing difficulty.",
    "gynecologist": "Before seeing {doctor}, note cycle timing, bleeding, discharge, pain pattern, or pregnancy concerns.",
    "ophthalmologist": "Before seeing {doctor}, note redness, discharge, blurred vision, itching, dryness, eye pain, or light sensitivity.",
    "mental health specialist": "Before seeing {doctor}, note sleep changes, panic episodes, triggers, and how long the stress symptoms have lasted.",
    "orthopedic specialist": "Before seeing {doctor}, note injury history, swelling, stiffness, numbness, or trouble walking.",
    "orthopedic": "Before seeing {doctor}, note injury history, swelling, stiffness, numbness, or trouble walking.",
}

PROFILE_MEDICINE_GUIDANCE = {
    "neurology": "paracetamol or acetaminophen for a simple headache, or a migraine tablet already prescribed to you, may be options, but only with neurologist approval",
    "cardiology": "do not self-start medicines like aspirin, nitroglycerin, BP tablets, or heart tablets from chat advice alone and use them only if your cardiologist already prescribed them",
    "ent": "paracetamol or acetaminophen, ibuprofen if it is safe for you, saline nasal support, or simple throat lozenges may be possible options, but the exact choice should be based on the ENT area and used only with doctor approval",
    "gynecology": "paracetamol or ibuprofen may help period-type pain in some cases, but anti-inflammatory tablets, hormonal tablets, antibiotics, and pregnancy-related medicines should be used only with direct gynecologist approval",
    "ophthalmology": "lubricating eye drops such as artificial tears or carmellose-type drops may help dryness, and allergy-type eye symptoms may sometimes need antihistamine or sodium cromoglicate drops, but use eye drops only with ophthalmologist approval and never self-start steroid or antibiotic drops",
    "general_fever": "paracetamol or acetaminophen may be possible options for fever, but use them only if your doctor says they are safe for you and avoid doubling up with cold medicines that also contain them",
    "respiratory": "paracetamol or acetaminophen for fever, saline nasal spray, and simple steam support may be possible options, but cough, cold, and decongestant medicines should be used only with doctor approval and should match your age and other conditions",
    "allergy": "cetirizine, loratadine, or another antihistamine may be possible options, but use them only if your doctor says they are safe for you and avoid the trigger that seems to start the reaction",
    "dermatology": "calamine, a plain emollient or moisturizer, or other soothing skin products may be possible options, but steroid or antibiotic creams should be used only with clinician approval",
    "gastro": "oral rehydration solution, an antacid or alginate product, or acid-reducing medicine already recommended for you may be possible options, but antibiotics or stronger stomach medicines should be used only with doctor approval",
    "mental_health": "do not self-start sedatives or sleeping tablets from chat alone and use such medicines only with doctor approval",
    "orthopedic": "paracetamol or acetaminophen, ibuprofen if it is safe for you, or a topical pain-relief gel such as ibuprofen or diclofenac may be possible options for strain-type pain, but use them only with orthopedic approval and avoid repeated painkiller use if you have stomach, kidney, heart, or bleeding problems",
}

ENT_DETAIL_MEDICINE_GUIDANCE = {
    "ear": "paracetamol or ibuprofen if it is safe for you may be possible options for ear pain, but use them only with doctor approval and avoid ear drops unless a clinician prescribed them",
    "nose_sinus": "saline nasal spray or wash, steam, and paracetamol or ibuprofen if safe may be possible options, but decongestant or steroid sprays should be used only with doctor guidance",
    "throat": "paracetamol or ibuprofen if safe, and simple medicated lozenges or sprays, may be possible options along with warm fluids and salt-water gargles, but use medicines only with doctor approval",
}

ENT_CLARIFICATION_PROMPT = (
    "Tell me whether this is mainly ear, nose or sinus, or throat or tonsil related."
)

ENT_DETAIL_KEYWORDS = {
    "ear": (
        "ear",
        "ears",
        "ear pain",
        "ear ache",
        "ear infection",
        "hearing",
        "hearing issue",
        "ear discharge",
        "ringing",
        "tinnitus",
    ),
    "nose_sinus": (
        "nose",
        "sinus",
        "sinusitis",
        "blocked nose",
        "runny nose",
        "nose block",
        "nasal",
        "facial pressure",
        "smell",
    ),
    "throat": (
        "throat",
        "tonsil",
        "tonsils",
        "sore throat",
        "swallow",
        "swallowing",
        "voice",
        "hoarse",
    ),
}

ENT_DETAIL_PROFILES = {
    "ear": {
        "focus_label": "Ear",
        "title": "Ear concern",
        "condition_name": "Ear-related concern",
        "symptoms_display": "ear symptoms",
        "overview": "This sounds more focused on the ear. Common possibilities include ear infection, wax buildup, pressure-related irritation, or middle-ear inflammation. This is not a confirmed diagnosis.",
        "watch_for": "ear pain, discharge, hearing change, ringing, dizziness, or fever",
        "care_tips": "keep the ear dry, avoid inserting buds or oil, and note if hearing changes or discharge starts",
        "red_flags": "severe ear pain, pus or blood discharge, facial weakness, high fever, or sudden hearing loss",
        "follow_up_hint": "whether there is discharge, hearing change, ringing, dizziness, or fever",
    },
    "nose_sinus": {
        "focus_label": "Nose / Sinus",
        "title": "Nose or sinus concern",
        "condition_name": "Nose or sinus concern",
        "symptoms_display": "nose or sinus symptoms",
        "overview": "This sounds more focused on the nose or sinuses. Common possibilities include allergy, cold-related congestion, sinus irritation, or sinus infection. This is not a confirmed diagnosis.",
        "watch_for": "blocked nose, runny nose, sinus pressure, facial pain, reduced smell, or fever",
        "care_tips": "rest, drink fluids, avoid smoke or dust, and note if facial pain or fever is getting worse",
        "red_flags": "eye swelling, severe facial pain, breathing trouble, or high persistent fever",
        "follow_up_hint": "whether there is blocked nose, thick discharge, facial pain, reduced smell, or fever",
    },
    "throat": {
        "focus_label": "Throat / Tonsil",
        "title": "Throat concern",
        "condition_name": "Throat or tonsil concern",
        "symptoms_display": "throat or tonsil symptoms",
        "overview": "This sounds more focused on the throat or tonsils. Common possibilities include throat infection, tonsil inflammation, irritation, or allergy-related throat symptoms. This is not a confirmed diagnosis.",
        "watch_for": "sore throat, tonsil swelling, painful swallowing, fever, voice change, or white patches",
        "care_tips": "drink warm fluids, rest your voice, avoid smoke, and note if swallowing becomes harder",
        "red_flags": "trouble breathing, drooling, severe swelling, inability to swallow fluids, or high fever",
        "follow_up_hint": "whether there is fever, painful swallowing, voice change, tonsil swelling, or white patches",
    },
}

CONDITION_PROFILES = {
    "neurology": {
        "name": "Neurology-related concern",
        "overview": "These symptoms can be linked with migraine, vertigo, nerve irritation, seizure disorders, or other brain and nerve conditions. This is not a confirmed diagnosis.",
        "watch_for": "headache, dizziness, numbness, tingling, balance problems, memory change, weakness, or vision change",
        "care_tips": "rest in a quiet room, drink fluids, avoid bright screens, and note when the symptom started and what made it worse",
        "red_flags": "sudden weakness, trouble speaking, severe headache, fainting, seizure, or confusion",
    },
    "cardiology": {
        "name": "Heart-related concern",
        "overview": "This pattern can be related to palpitations, blood-pressure changes, heart rhythm issues, or stress-related heart symptoms. It still needs doctor evaluation for confirmation.",
        "watch_for": "fast heartbeat, chest pressure, dizziness, shortness of breath, or swelling",
        "care_tips": "rest, avoid heavy exertion, reduce caffeine if it triggers symptoms, and note how long the episode lasts",
        "red_flags": "chest pain, fainting, severe breathlessness, or pain spreading to the arm or jaw",
    },
    "ent": {
        "name": "Ear, nose, and throat concern",
        "overview": "This may be related to sinus infection, ear infection, tonsil or throat inflammation, or allergy-related ENT symptoms.",
        "watch_for": "ear pain, blocked nose, throat pain, hearing change, sinus pressure, fever, or discharge",
        "care_tips": "drink warm fluids, rest, avoid smoke or dust, and keep track of fever or worsening pain",
        "red_flags": "trouble breathing, severe swelling, severe ear pain with discharge, or high persistent fever",
    },
    "gynecology": {
        "name": "Women's health concern",
        "overview": "These symptoms can be related to menstrual issues, hormonal imbalance, pelvic infection, pregnancy-related concerns, or other gynecologic conditions.",
        "watch_for": "pelvic pain, irregular bleeding, unusual discharge, worsening cramps, or pregnancy-related symptoms",
        "care_tips": "rest, stay hydrated, note the timing of the symptoms with your cycle, and avoid delaying an appointment if symptoms keep returning",
        "red_flags": "heavy bleeding, fainting, severe pelvic pain, or pregnancy with pain or bleeding",
    },
    "ophthalmology": {
        "name": "Eye-related concern",
        "overview": "This may be related to dryness, allergy, conjunctivitis, surface irritation, or another eye problem that may need an eye specialist review if it keeps returning or affects vision.",
        "watch_for": "redness, itching, watering, discharge, eye pain, blurred vision, or light sensitivity",
        "care_tips": "avoid rubbing the eye, wash your hands, remove contact lenses for now, and note whether there is pain, discharge, or vision change",
        "red_flags": "sudden vision loss, severe eye pain, marked light sensitivity, eye injury, or rapidly worsening swelling",
    },
    "general_fever": {
        "name": "Fever-related illness",
        "overview": "Fever can happen with viral infection, flu-like illness, throat infection, or other inflammatory conditions. It needs symptom follow-up rather than instant diagnosis.",
        "watch_for": "temperature changes, chills, weakness, cough, sore throat, vomiting, or rash",
        "care_tips": "rest, drink fluids, monitor temperature, and take only medicines already known to be safe for you",
        "red_flags": "very high fever, confusion, dehydration, breathing trouble, or fever lasting more than a few days",
    },
    "respiratory": {
        "name": "Respiratory concern",
        "overview": "This can be seen with cold, flu, throat infection, allergy, or other breathing-related conditions. A doctor should evaluate persistent or worsening symptoms.",
        "watch_for": "cough, sore throat, blocked nose, wheezing, fever, or shortness of breath",
        "care_tips": "rest, fluids, warm liquids, and avoiding smoke or dust can help while you wait for assessment",
        "red_flags": "trouble breathing, chest pain, blue lips, or worsening weakness",
    },
    "allergy": {
        "name": "Allergy-related concern",
        "overview": "This may be related to food, pollen, dust, or medicine allergy. A full diagnosis depends on the trigger and the severity of symptoms.",
        "watch_for": "itching, sneezing, rash, swelling, watery eyes, or wheezing",
        "care_tips": "avoid the suspected trigger, note what changed before symptoms started, and do not repeat a medicine that triggered a reaction",
        "red_flags": "swelling of the face, breathing trouble, severe rash, or faintness",
    },
    "dermatology": {
        "name": "Skin-related concern",
        "overview": "This can be related to allergy, dermatitis, fungal infection, heat rash, or medicine reaction depending on the pattern of the rash.",
        "watch_for": "itching, redness, spread of rash, discharge, pain, or swelling",
        "care_tips": "keep the area clean and dry, avoid new skin products, and note whether a medicine or food started before the rash",
        "red_flags": "rapid spread, facial swelling, breathing trouble, or rash with fever",
    },
    "gastro": {
        "name": "Digestive concern",
        "overview": "These symptoms can be seen with indigestion, gastritis, food poisoning, infection, or other stomach and bowel conditions.",
        "watch_for": "nausea, vomiting, loose motion, stomach cramps, bloating, or poor appetite",
        "care_tips": "drink fluids, avoid oily food for now, and monitor whether the pain gets worse after eating",
        "red_flags": "blood in vomit or stool, severe dehydration, unbearable pain, or persistent vomiting",
    },
    "mental_health": {
        "name": "Stress or anxiety-related concern",
        "overview": "These symptoms may be related to anxiety, stress overload, panic symptoms, or poor sleep, but a doctor can help rule out physical causes too.",
        "watch_for": "racing thoughts, poor sleep, chest tightness, restlessness, or panic-like symptoms",
        "care_tips": "slow breathing, water, short rest, reduced caffeine, and reaching out to someone you trust can help in the moment",
        "red_flags": "feeling unsafe, self-harm thoughts, or severe panic that does not settle",
    },
    "orthopedic": {
        "name": "Bone, joint, or muscle concern",
        "overview": "This can be related to strain, inflammation, overuse, posture issues, or joint problems that need orthopedic review if they keep returning.",
        "watch_for": "swelling, stiffness, movement pain, numbness, or weakness in the limb",
        "care_tips": "rest the area, avoid heavy load, and note whether the pain follows injury or repeated movement",
        "red_flags": "deformity, inability to walk, severe swelling, or loss of feeling",
    },
    "general": {
        "name": "General health concern",
        "overview": "Your message needs a bit more symptom detail before I can narrow the likely health area.",
        "watch_for": "the main symptom, when it started, how severe it is, and whether it is getting worse",
        "care_tips": "share the symptom, duration, triggers, and whether you already took any medicine",
        "red_flags": "sudden worsening, breathing trouble, fainting, or severe pain",
    },
}

EMERGENCY_PHRASES = (
    "chest pain",
    "cannot breathe",
    "can't breathe",
    "difficulty breathing",
    "severe bleeding",
    "passed out",
    "fainted",
    "heart attack",
    "stroke symptoms",
    "suicidal thoughts",
)
EMERGENCY_TOKENS = {
    "emergency",
    "unconscious",
    "collapse",
    "collapsed",
    "seizure",
    "bleeding",
    "overdose",
}

_lemmatizer = None

try:
    from nltk.stem import WordNetLemmatizer

    _lemmatizer = WordNetLemmatizer()
except Exception:
    _lemmatizer = None


def _normalize_text(text: str) -> str:
    return " ".join((text or "").strip().lower().split())


def _lemmatize(token: str) -> str:
    if not token or _lemmatizer is None:
        return token
    try:
        return _lemmatizer.lemmatize(token)
    except LookupError:
        return token


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9']+", _normalize_text(text))
    return [_lemmatize(token) for token in tokens]


def _keyword_matches(token_text: str, tokens: set[str], keyword: str) -> bool:
    keyword_tokens = tokenize(keyword)
    if not keyword_tokens:
        return False

    if len(keyword_tokens) == 1:
        return keyword_tokens[0] in tokens

    return " ".join(keyword_tokens) in token_text


def _format_human_list(items: list[str]) -> str:
    cleaned = [item.strip() for item in items if item and item.strip()]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return f"{', '.join(cleaned[:-1])}, and {cleaned[-1]}"


def _clean_sentence(text: str) -> str:
    cleaned = " ".join((text or "").strip().split())
    if not cleaned:
        return ""
    return cleaned if cleaned.endswith((".", "!", "?")) else f"{cleaned}."


@lru_cache(maxsize=1)
def load_intents() -> dict:
    if not INTENTS_PATH.exists():
        return {"intents": []}
    return json.loads(INTENTS_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _responses_by_tag() -> dict[str, list[str]]:
    intent_data = load_intents().get("intents", [])
    return {intent["tag"]: intent.get("responses", []) for intent in intent_data}


@lru_cache(maxsize=1)
def _load_model_bundle():
    model_path = next((path for path in MODEL_PATHS if path.exists()), None)
    if model_path is None or not WORDS_PATH.exists() or not CLASSES_PATH.exists():
        return None

    try:
        from tensorflow.keras.models import load_model

        with WORDS_PATH.open("rb") as words_handle:
            words = pickle.load(words_handle)
        with CLASSES_PATH.open("rb") as classes_handle:
            classes = pickle.load(classes_handle)
        model = load_model(model_path)
        return model, words, classes
    except Exception:
        return None


def bag_of_words(sentence: str, vocabulary: list[str]) -> np.ndarray:
    sentence_words = set(tokenize(sentence))
    return np.array([1 if word in sentence_words else 0 for word in vocabulary], dtype=np.float32)


def predict_intents(sentence: str, error_threshold: float = 0.4) -> list[dict]:
    bundle = _load_model_bundle()
    if bundle is None:
        return []

    model, words, classes = bundle
    probabilities = model.predict(np.array([bag_of_words(sentence, words)]), verbose=0)[0]
    matches = [
        {"intent": classes[index], "probability": float(score)}
        for index, score in enumerate(probabilities)
        if score >= error_threshold
    ]
    matches.sort(key=lambda item: item["probability"], reverse=True)
    return matches


def _pick_response(tag: str, default: str | None = None) -> str:
    responses = _responses_by_tag().get(tag) or []
    if responses:
        return random.choice(responses)
    return default or DEFAULT_FALLBACK_RESPONSE


def _condense_response(text: str, max_sentences: int = 2) -> str:
    cleaned = " ".join((text or "").strip().split())
    if not cleaned:
        return ""

    sentences = [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", cleaned) if segment.strip()]
    if len(sentences) <= max_sentences:
        return cleaned

    return " ".join(sentences[:max_sentences]).strip()


def _keyword_help_reply(message: str) -> str | None:
    normalized = _normalize_text(message)
    tokens = set(tokenize(message))

    if detect_emergency(message):
        return (
            "This sounds urgent. Please contact emergency services or go to the nearest "
            "hospital right away. Do not rely on chat alone for severe symptoms."
        )

    if tokens.intersection({"appointment", "appointments", "book", "booking", "schedule"}):
        return (
            "Use the Appointments section to manage visits. Tell me the symptom if you want help choosing the right doctor."
        )

    if tokens.intersection({"prescription", "prescriptions", "rx"}):
        return (
            "Open the Prescription section to review your medicines and instructions. Share a medicine name if you want quick guidance."
        )

    if tokens.intersection({"order", "orders", "invoice", "payment", "cart"}):
        return (
            "Check Orders, Payment, or Invoice pages for purchase status. If it is unpaid, finish payment first."
        )

    if tokens.intersection({"dose", "dosage", "tablet", "capsule", "missed"}):
        return (
            "Exact dosage depends on the medicine and prescription. Share the medicine name before taking more."
        )

    return None


def detect_emergency(text: str) -> bool:
    normalized = _normalize_text(text)
    tokens = set(tokenize(text))
    return any(phrase in normalized for phrase in EMERGENCY_PHRASES) or bool(tokens.intersection(EMERGENCY_TOKENS))


def classify_message(message: str) -> dict:
    predictions = predict_intents(message)
    if predictions:
        top_match = predictions[0]
        return {
            "intent": top_match["intent"],
            "confidence": float(top_match["probability"]),
            "predictions": predictions,
        }

    return {"intent": "noanswer", "confidence": 0.0, "predictions": []}


def extract_symptoms(text: str) -> list[str]:
    token_list = tokenize(text)
    tokens = set(token_list)
    token_text = " ".join(token_list)
    found = []
    for label, keywords in SYMPTOM_KEYWORDS.items():
        if any(_keyword_matches(token_text, tokens, keyword) for keyword in keywords):
            found.append(label)
    return found


def detect_specialty_topics(text: str) -> list[str]:
    token_list = tokenize(text)
    tokens = set(token_list)
    token_text = " ".join(token_list)
    matches = []

    for specialty, keywords in SPECIALTY_TOPIC_KEYWORDS.items():
        if any(_keyword_matches(token_text, tokens, keyword) for keyword in keywords):
            matches.append(specialty)

    if detect_ent_focus(text) and "ENT" not in matches:
        matches.append("ENT")

    return matches


def detect_ent_focus(text: str) -> str:
    token_list = tokenize(text)
    tokens = set(token_list)
    token_text = " ".join(token_list)
    best_focus = ""
    best_score = 0

    for focus_key, keywords in ENT_DETAIL_KEYWORDS.items():
        score = sum(1 for keyword in keywords if _keyword_matches(token_text, tokens, keyword))
        if score > best_score:
            best_focus = focus_key
            best_score = score

    return best_focus


def determine_urgency(text: str, symptoms: list[str] | None = None) -> str:
    symptoms = symptoms or extract_symptoms(text)
    tokens = set(tokenize(text))

    if detect_emergency(text):
        return "emergency"
    if "breathing trouble" in symptoms or "chest pain" in symptoms:
        return "high"
    if tokens.intersection(HIGH_PRIORITY_TOKENS):
        return "high"
    return "routine"


def extract_duration_text(text: str) -> str:
    normalized = _normalize_text(text)
    for pattern in DURATION_PATTERNS:
        match = re.search(pattern, normalized)
        if match:
            return match.group(0)
    return ""


def extract_severity_terms(text: str) -> list[str]:
    normalized = _normalize_text(text)
    detected = []

    for pattern, label in SEVERITY_PATTERNS:
        if pattern in normalized and label not in detected:
            detected.append(label)

    return detected


def suggest_specialty(symptoms: list[str], primary_intent: str = "", message_text: str = "") -> str:
    for symptom in symptoms:
        if symptom in SPECIALTY_BY_SYMPTOM:
            return SPECIALTY_BY_SYMPTOM[symptom]

    specialty_hints = detect_specialty_topics(message_text)
    if specialty_hints:
        return specialty_hints[0]

    if primary_intent in INTENT_SPECIALTY_HINTS:
        return INTENT_SPECIALTY_HINTS[primary_intent]

    return "General Physician"


def get_condition_profile(summary: dict) -> dict:
    symptoms = summary.get("symptoms") or []
    symptom_set = set(symptoms)

    for required_symptoms, profile_key in CONDITION_COMBINATION_RULES:
        if required_symptoms.issubset(symptom_set):
            profile = CONDITION_PROFILES[profile_key].copy()
            profile["key"] = profile_key
            return profile

    for symptom in symptoms:
        profile_key = CONDITION_PROFILE_BY_SYMPTOM.get(symptom)
        if profile_key:
            profile = CONDITION_PROFILES[profile_key].copy()
            profile["key"] = profile_key
            return profile

    for specialty in summary.get("specialty_hints") or []:
        profile_key = PROFILE_KEY_BY_SPECIALTY.get(specialty)
        if profile_key:
            profile = CONDITION_PROFILES[profile_key].copy()
            profile["key"] = profile_key
            return profile

    profile_key = PROFILE_KEY_BY_SPECIALTY.get(summary.get("recommended_specialty", ""))
    if profile_key:
        profile = CONDITION_PROFILES[profile_key].copy()
        profile["key"] = profile_key
        return profile

    default_profile = CONDITION_PROFILES["general"].copy()
    default_profile["key"] = "general"
    return default_profile


def build_follow_up_prompt(summary: dict) -> str:
    clarification_prompt = (summary.get("focus_clarification_prompt") or "").strip()
    if clarification_prompt:
        return clarification_prompt

    profile = get_condition_profile(summary)
    follow_up_hint = (
        summary.get("focus_follow_up_hint")
        or PROFILE_FOLLOW_UP_HINTS.get(profile.get("key", "general"), PROFILE_FOLLOW_UP_HINTS["general"])
    )
    missing_core_details = []

    if not summary.get("duration_text"):
        missing_core_details.append("when it started")
    if not summary.get("severity_terms"):
        missing_core_details.append("whether it is mild, severe, or getting worse")

    if missing_core_details:
        return (
            f"To narrow this down, tell me { _format_human_list(missing_core_details) }, "
            f"and {follow_up_hint}."
        )

    return f"To narrow this further, tell me {follow_up_hint}."


def build_medicine_guidance(summary: dict) -> str:
    focused_area_key = (summary.get("focused_area_key") or "").strip()
    if focused_area_key and focused_area_key in ENT_DETAIL_MEDICINE_GUIDANCE:
        return ENT_DETAIL_MEDICINE_GUIDANCE[focused_area_key]

    profile = get_condition_profile(summary)
    profile_key = profile.get("key", "general")
    return PROFILE_MEDICINE_GUIDANCE.get(profile_key, "")


def build_precaution_items(
    summary: dict,
    visual_analysis_summary: str = "",
    doctor_specialization: str = "",
    doctor_name: str = "",
) -> list[str]:
    items = []

    care_tips = _clean_sentence(summary.get("care_tips", ""))
    if care_tips:
        items.append(care_tips)

    normalized_specialization = " ".join((doctor_specialization or "").strip().lower().split())
    doctor_label = doctor_name or "the doctor"
    doctor_hint = DOCTOR_PRECAUTION_HINTS.get(normalized_specialization, "")
    if doctor_hint:
        items.append(_clean_sentence(doctor_hint.format(doctor=doctor_label)))

    watch_for = summary.get("watch_for", "")
    if watch_for:
        items.append(_clean_sentence(f"Keep watching for {watch_for}"))

    red_flags = summary.get("red_flags", "")
    if red_flags:
        prefix = "Get urgent medical help for" if summary.get("urgency_level") == "high" else "Seek urgent care if you notice"
        items.append(_clean_sentence(f"{prefix} {red_flags}"))

    follow_up_prompt = _clean_sentence(summary.get("follow_up_prompt", ""))
    if follow_up_prompt:
        items.append(follow_up_prompt)

    if visual_analysis_summary:
        items.append(_clean_sentence(f"Photo review note: {visual_analysis_summary}"))

    unique_items = []
    seen = set()
    for item in items:
        normalized = item.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        unique_items.append(item)
    return unique_items


def build_doctor_handoff_items(
    summary: dict,
    top_doctor_name: str = "",
    visual_analysis_label: str = "",
    visual_analysis_summary: str = "",
) -> list[dict]:
    items = [
        {"label": "Main concern", "value": summary.get("title") or summary.get("condition_name") or "Care chat"},
        {"label": "Likely health area", "value": summary.get("condition_name") or "General health concern"},
        {"label": "Detected symptoms", "value": summary.get("symptoms_display") or "No clear symptom markers yet"},
        {"label": "Urgency", "value": str(summary.get("urgency_level", "routine")).title()},
        {"label": "Suggested specialty", "value": summary.get("recommended_specialty") or "General Physician"},
        {"label": "Latest patient message", "value": summary.get("last_user_message") or "No patient message yet"},
        {"label": "Care summary", "value": summary.get("summary") or "No summary yet"},
        {"label": "What still needs clarification", "value": summary.get("follow_up_prompt") or "No additional follow-up prompt"},
    ]

    if summary.get("focused_area_label"):
        items.insert(3, {"label": "Specific area", "value": summary["focused_area_label"]})

    if summary.get("duration_text"):
        items.insert(4, {"label": "Reported duration", "value": summary["duration_text"]})

    if top_doctor_name:
        items.insert(6, {"label": "Best available doctor match", "value": top_doctor_name})

    if summary.get("medicine_guidance"):
        items.insert(7, {"label": "Suggested medicine support", "value": summary["medicine_guidance"]})

    if visual_analysis_summary:
        photo_value = visual_analysis_summary
        if visual_analysis_label:
            photo_value = f"{visual_analysis_label}: {visual_analysis_summary}"
        items.append({"label": "Photo review", "value": photo_value})

    return [item for item in items if item.get("value")]


def analyze_care_image(image_bytes: bytes, filename: str = "", summary: dict | None = None) -> dict:
    extension = Path(filename or "").suffix.lower()
    if extension and extension not in IMAGE_ANALYSIS_ALLOWED_EXTENSIONS:
        return {
            "label": "Unsupported image type",
            "summary": "Please upload a clear JPG, JPEG, PNG, BMP, or WEBP image.",
            "details": "This visual check only works on common image formats and only helps with visible external problems.",
        }

    if not image_bytes:
        return {
            "label": "No image uploaded",
            "summary": "Upload a clear photo if you want a surface-level image review.",
            "details": "This check only helps with visible external issues such as redness, bruising, swelling, rash, or wounds.",
        }

    try:
        import tensorflow as tf

        image = tf.io.decode_image(image_bytes, channels=3, expand_animations=False)
        image = tf.image.convert_image_dtype(image, tf.float32)
        if len(image.shape) != 3 or image.shape[-1] != 3:
            raise ValueError("Unexpected image shape")

        image = tf.image.resize(image, [192, 192])
        mean_rgb = tf.reduce_mean(image, axis=[0, 1])
        brightness = float(tf.reduce_mean(tf.image.rgb_to_grayscale(image)).numpy())
        hsv = tf.image.rgb_to_hsv(image)
        saturation = float(tf.reduce_mean(hsv[..., 1]).numpy())

        red_mask = tf.cast(
            (image[..., 0] > image[..., 1] * 1.10)
            & (image[..., 0] > image[..., 2] * 1.12)
            & (image[..., 0] > 0.34),
            tf.float32,
        )
        dark_mask = tf.cast(tf.reduce_mean(image, axis=-1) < 0.22, tf.float32)
        yellow_mask = tf.cast(
            (image[..., 0] > 0.45)
            & (image[..., 1] > 0.38)
            & (image[..., 2] < 0.32),
            tf.float32,
        )
        cool_dark_mask = tf.cast(
            (tf.reduce_mean(image, axis=-1) < 0.32)
            & (image[..., 2] >= image[..., 0] * 0.92),
            tf.float32,
        )

        red_ratio = float(tf.reduce_mean(red_mask).numpy())
        dark_ratio = float(tf.reduce_mean(dark_mask).numpy())
        yellow_ratio = float(tf.reduce_mean(yellow_mask).numpy())
        cool_dark_ratio = float(tf.reduce_mean(cool_dark_mask).numpy())

        sobel = tf.image.sobel_edges(tf.expand_dims(image, axis=0))
        edge_strength = float(
            tf.reduce_mean(tf.sqrt(tf.reduce_sum(tf.square(sobel), axis=-1))).numpy()
        )

        mean_red = float(mean_rgb[0].numpy())
        mean_green = float(mean_rgb[1].numpy())
        mean_blue = float(mean_rgb[2].numpy())
    except Exception:
        return {
            "label": "Image unclear",
            "summary": "I could not read that image clearly enough to give a visual note.",
            "details": "Try a brighter, closer image focused on the affected area. This visual check only supports visible surface concerns.",
        }

    label = "No clear surface pattern detected"
    summary_text = (
        "The photo does not show one strong visible surface pattern. If the issue is internal or not clearly visible on skin, the symptom chat is more useful than the image."
    )

    if brightness < 0.14:
        label = "Image too dark"
        summary_text = (
            "The image is too dark for a reliable visual note. Please use brighter light and keep the affected area centered."
        )
    elif red_ratio > 0.16 and saturation > 0.18:
        label = "Visible redness or irritation"
        summary_text = (
            "The photo shows a noticeable red or inflamed-looking surface area. This may fit visible irritation, rash, inflammation, or a superficial wound, but the cause cannot be confirmed from the image alone."
        )
    elif cool_dark_ratio > 0.24 or (dark_ratio > 0.32 and mean_blue >= mean_red * 0.85):
        label = "Possible bruising or dark discoloration"
        summary_text = (
            "The photo shows a darker discolored area that could fit bruising or another surface discoloration. A photo alone cannot confirm the reason."
        )
    elif yellow_ratio > 0.18 and saturation > 0.16:
        label = "Visible yellowish discoloration"
        summary_text = (
            "The photo shows a yellowish surface color change. This can happen for different reasons and still needs direct clinical review if it is new or spreading."
        )
    elif edge_strength > 0.24 and saturation > 0.14:
        label = "Possible surface rash or texture change"
        summary_text = (
            "The photo shows a visible surface pattern or texture change that may fit a rash, dry irritated area, or other external skin problem."
        )

    scope_parts = [
        "This visual check only helps with visible external issues such as rash, redness, bruising, swelling, or wounds.",
        "It cannot confirm infections, internal disease, or neurologic problems from an image alone.",
    ]
    if summary and summary.get("recommended_specialty") not in {"Dermatologist", "General Physician", "ENT"}:
        scope_parts.append(
            f"Your chat still points more toward {summary.get('condition_name', 'the reported symptom pattern')}, so the symptom description remains more important than the photo."
        )

    details = " ".join(scope_parts)
    if label == "No clear surface pattern detected" and brightness > 0.18 and edge_strength < 0.10:
        details += " The image looks visually even, so the problem may not be strongly visible on the surface."

    return {
        "label": label,
        "summary": summary_text,
        "details": details,
        "signals": {
            "brightness": round(brightness, 3),
            "saturation": round(saturation, 3),
            "red_ratio": round(red_ratio, 3),
            "dark_ratio": round(dark_ratio, 3),
            "edge_strength": round(edge_strength, 3),
            "mean_red": round(mean_red, 3),
            "mean_green": round(mean_green, 3),
            "mean_blue": round(mean_blue, 3),
        },
    }


def format_condition_guidance(summary: dict) -> str:
    profile = get_condition_profile(summary)

    segments = [
        f"Possible health area: {profile['name']}.",
        profile["overview"],
        f"Common things to watch: {profile['watch_for']}.",
        f"What may help for now: {profile['care_tips']}.",
    ]

    if summary.get("urgency_level") in {"high", "emergency"}:
        segments.append(f"Urgent warning signs: {profile['red_flags']}.")

    return " ".join(segment.strip() for segment in segments if segment).strip()


def _append_doctor_guidance(base_response: str, message: str, primary_intent: str = "") -> str:
    symptoms = extract_symptoms(message)
    urgency_level = determine_urgency(message, symptoms)
    if urgency_level == "emergency":
        return base_response

    if not symptoms and primary_intent not in INTENTS_WITH_DOCTOR_GUIDANCE:
        return base_response

    recommended_specialty = suggest_specialty(symptoms, primary_intent, message)
    specialty_text = recommended_specialty.lower()
    if specialty_text in base_response.lower():
        return base_response

    if recommended_specialty == "General Physician":
        doctor_hint = " A General Physician is a good first doctor."
    else:
        doctor_hint = f" A {recommended_specialty} is the right doctor."

    return f"{base_response}{doctor_hint}"


def _signal_display(symptoms: list[str], specialty_hints: list[str]) -> str:
    if symptoms:
        return ", ".join(SYMPTOM_DISPLAY_LABELS.get(symptom, symptom) for symptom in symptoms)

    labels = []
    for specialty in specialty_hints:
        label = SPECIALTY_SIGNAL_LABELS.get(specialty, specialty)
        if label not in labels:
            labels.append(label)

    return ", ".join(labels) if labels else "No clear symptom markers yet"


def _has_meaningful_health_signal(summary: dict) -> bool:
    if summary.get("symptoms"):
        return True
    if summary.get("specialty_hints"):
        return True
    return summary.get("condition_name") != CONDITION_PROFILES["general"]["name"]


def _guided_fallback_reply(summary: dict) -> str | None:
    if not _has_meaningful_health_signal(summary):
        return None

    condition_name = summary.get("condition_name", "a health concern").lower()
    recommended_specialty = summary.get("recommended_specialty", "doctor")
    symptom_display = summary.get("symptoms_display", "")
    parts = [f"This sounds more related to {condition_name}."]

    if summary.get("symptoms"):
        parts.append(f"The main pattern I noticed is {symptom_display}.")
    elif symptom_display and symptom_display != "No clear symptom markers yet":
        parts.append(f"The topic you mentioned points more toward {symptom_display}.")

    if recommended_specialty == "General Physician":
        parts.append("A General Physician would be a good first doctor to review this.")
    else:
        parts.append(f"A {recommended_specialty} would be the right doctor to review this.")

    if summary.get("focus_clarification_prompt"):
        return " ".join([parts[0], summary["focus_clarification_prompt"]]).strip()

    if not summary.get("symptoms"):
        parts.append(
            "Share the main symptom, when it started, and whether it is getting worse so I can narrow the guidance further."
        )

    return " ".join(parts).strip()


def _build_compact_handoff_summary(
    symptoms: list[str],
    specialty_hints: list[str],
    latest_message: str,
    duration_text: str,
    condition_name: str,
    urgency_level: str,
    signal_text: str = "",
    prefer_signal_text: bool = False,
    medicine_guidance: str = "",
) -> str:
    normalized_condition = (condition_name or "").strip()
    urgency_display = str(urgency_level or "routine").strip().title()
    cleaned_signal_text = (signal_text or "").strip()

    if prefer_signal_text and cleaned_signal_text and cleaned_signal_text != "No clear symptom markers yet":
        opening = f"Patient reports {cleaned_signal_text}"
        if duration_text:
            opening = f"{opening} {duration_text}"
        opening = f"{opening}."
    elif symptoms:
        symptom_labels = [SYMPTOM_DISPLAY_LABELS.get(symptom, symptom) for symptom in symptoms]
        opening = f"Patient reports {_format_human_list(symptom_labels)}"
        if duration_text:
            opening = f"{opening} {duration_text}"
        opening = f"{opening}."
    elif cleaned_signal_text and cleaned_signal_text != "No clear symptom markers yet":
        opening = f"Patient reports {cleaned_signal_text}"
        if duration_text:
            opening = f"{opening} {duration_text}"
        opening = f"{opening}."
    elif specialty_hints:
        concern_area = _format_human_list(specialty_hints)
        opening = f"Main concern points to {concern_area}."
    elif latest_message:
        trimmed_message = latest_message[:120].strip().rstrip(".")
        opening = f"Main concern shared: {trimmed_message}."
    else:
        return "No user details provided yet."

    closing = ""
    if normalized_condition and normalized_condition != "General health concern":
        closing = f"Likely {normalized_condition.lower()} with {urgency_display.lower()} urgency."
    elif urgency_display:
        closing = f"Current urgency: {urgency_display}."

    return " ".join(segment for segment in [opening, closing] if segment).strip()


def _ent_focus_context(
    combined_text: str,
    symptoms: list[str],
    specialty_hints: list[str],
    recommended_specialty: str,
) -> dict:
    has_ent_signal = (
        "ent concern" in (symptoms or [])
        or "ENT" in (specialty_hints or [])
        or recommended_specialty == "ENT"
    )
    if not has_ent_signal:
        return {}

    focus_key = detect_ent_focus(combined_text)
    if not focus_key:
        return {
            "focus_clarification_prompt": ENT_CLARIFICATION_PROMPT,
            "focus_follow_up_hint": "",
            "focused_area_key": "",
            "focused_area_label": "",
        }

    profile = ENT_DETAIL_PROFILES[focus_key]
    return {
        "focused_area_key": focus_key,
        "focused_area_label": profile["focus_label"],
        "focus_clarification_prompt": "",
        "focus_follow_up_hint": profile["follow_up_hint"],
        "title": profile["title"],
        "condition_name": profile["condition_name"],
        "condition_overview": profile["overview"],
        "watch_for": profile["watch_for"],
        "care_tips": profile["care_tips"],
        "red_flags": profile["red_flags"],
        "symptoms_display": profile["symptoms_display"],
    }


def build_care_summary(messages: list[str] | str) -> dict:
    if isinstance(messages, str):
        user_messages = [messages]
    else:
        user_messages = [str(message).strip() for message in messages if str(message).strip()]

    combined_text = " ".join(user_messages)
    latest_message = user_messages[-1] if user_messages else ""
    latest_classification = classify_message(latest_message) if latest_message else {"intent": "noanswer", "confidence": 0.0}
    symptoms = extract_symptoms(combined_text)
    specialty_hints = detect_specialty_topics(combined_text)
    duration_text = extract_duration_text(combined_text)
    severity_terms = extract_severity_terms(combined_text)
    urgency_level = determine_urgency(combined_text, symptoms)
    recommended_specialty = suggest_specialty(symptoms, latest_classification["intent"], combined_text)
    condition_profile = get_condition_profile(
        {
            "symptoms": symptoms,
            "specialty_hints": specialty_hints,
            "recommended_specialty": recommended_specialty,
        }
    )
    ent_focus = _ent_focus_context(combined_text, symptoms, specialty_hints, recommended_specialty)

    if ent_focus.get("title"):
        title = ent_focus["title"]
    elif symptoms:
        title = f"{symptoms[0].title()} concern"
    elif specialty_hints:
        title = f"{specialty_hints[0]} concern"
    elif latest_message:
        title = "General care question"
    else:
        title = "Care chat"

    symptoms_display = ent_focus.get("symptoms_display") or _signal_display(symptoms, specialty_hints)
    condition_name = ent_focus.get("condition_name") or condition_profile["name"]
    condition_overview = ent_focus.get("condition_overview") or condition_profile["overview"]
    care_tips = ent_focus.get("care_tips") or condition_profile["care_tips"]
    watch_for = ent_focus.get("watch_for") or condition_profile["watch_for"]
    red_flags = ent_focus.get("red_flags") or condition_profile["red_flags"]
    summary_seed = {
        "symptoms": symptoms,
        "specialty_hints": specialty_hints,
        "recommended_specialty": recommended_specialty,
        "focused_area_key": ent_focus.get("focused_area_key", ""),
    }
    medicine_guidance = build_medicine_guidance(summary_seed)

    summary = _build_compact_handoff_summary(
        symptoms,
        specialty_hints,
        latest_message,
        duration_text,
        condition_name,
        urgency_level,
        signal_text=symptoms_display,
        prefer_signal_text=bool(ent_focus.get("focused_area_key")),
        medicine_guidance=medicine_guidance,
    )

    summary_data = {
        "title": title,
        "summary": summary.strip(),
        "symptoms": symptoms,
        "specialty_hints": specialty_hints,
        "symptoms_display": symptoms_display,
        "primary_intent": latest_classification["intent"],
        "confidence": float(latest_classification["confidence"]),
        "recommended_specialty": recommended_specialty,
        "urgency_level": urgency_level,
        "last_user_message": latest_message,
        "duration_text": duration_text,
        "severity_terms": severity_terms,
        "severity_display": _format_human_list(severity_terms),
        "condition_name": condition_name,
        "condition_overview": condition_overview,
        "care_tips": care_tips,
        "watch_for": watch_for,
        "red_flags": red_flags,
        "medicine_guidance": medicine_guidance,
        "focused_area_key": ent_focus.get("focused_area_key", ""),
        "focused_area_label": ent_focus.get("focused_area_label", ""),
        "focus_clarification_prompt": ent_focus.get("focus_clarification_prompt", ""),
        "focus_follow_up_hint": ent_focus.get("focus_follow_up_hint", ""),
    }
    summary_data["follow_up_prompt"] = build_follow_up_prompt(summary_data)
    return summary_data


def generate_reply(message: str) -> str:
    message = (message or "").strip()
    if not message:
        return "Please type a question so I can help."

    keyword_reply = _keyword_help_reply(message)
    classification = classify_message(message)
    predictions = classification["predictions"]

    if predictions:
        top_match = predictions[0]
        top_probability = top_match["probability"]
        next_probability = predictions[1]["probability"] if len(predictions) > 1 else 0.0

        if top_match["intent"] == "emergency_situations":
            return _condense_response(_pick_response(top_match["intent"]))

        if top_probability >= 0.55 and (top_probability - next_probability) >= 0.08:
            return _condense_response(_append_doctor_guidance(
                _pick_response(top_match["intent"]),
                message,
                top_match["intent"],
            ), max_sentences=3)

        if keyword_reply:
            guided_summary = build_care_summary([message])
            guided_reply = _guided_fallback_reply(guided_summary)
            if guided_reply and guided_summary.get("recommended_specialty") != "General Physician":
                return _condense_response(guided_reply)
            return _condense_response(keyword_reply)

        if top_probability >= 0.45 and top_match["intent"] != "noanswer":
            return _condense_response(_append_doctor_guidance(
                _pick_response(top_match["intent"]),
                message,
                top_match["intent"],
            ), max_sentences=3)

    if keyword_reply:
        guided_summary = build_care_summary([message])
        guided_reply = _guided_fallback_reply(guided_summary)
        if guided_reply and guided_summary.get("recommended_specialty") != "General Physician":
            return _condense_response(guided_reply)
        return _condense_response(keyword_reply)

    guided_summary = build_care_summary([message])
    guided_reply = _guided_fallback_reply(guided_summary)
    if guided_reply:
        return _condense_response(guided_reply)

    return _condense_response(_pick_response("noanswer", DEFAULT_FALLBACK_RESPONSE))


def chatbot_response(message: str) -> str:
    return generate_reply(message)


def get_welcome_message() -> str:
    return DEFAULT_WELCOME_MESSAGE


def get_default_chat_history() -> list[dict[str, str]]:
    return [{"role": "assistant", "text": DEFAULT_WELCOME_MESSAGE}]


def get_quick_prompts() -> list[str]:
    return list(QUICK_PROMPTS)
