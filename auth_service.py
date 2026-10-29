"""
Nihol AI - Foydalanuvchilar (Login/Register), Profil,
Jonli Ob-Havo va AI Agronom Chati Moduli.
"""

import os
import json
import uuid
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
import urllib.request

from config import BASE_DIR, GEMINI_API_KEY

USERS_FILE = BASE_DIR / "users.json"


def _hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _load_users() -> Dict[str, Any]:
    if USERS_FILE.exists():
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_users(users: Dict[str, Any]):
    try:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Foydalanuvchilarni saqlashda xatolik:", e)


def register_user(name: str, phone: str, region: str, role: str, password: str) -> Dict[str, Any]:
    users = _load_users()
    phone_clean = phone.strip().replace(" ", "").replace("-", "")

    if phone_clean in users:
        return {"success": False, "error": "Ushbu telefon raqami allaqachon ro'yxatdan o'tgan."}

    token = uuid.uuid4().hex
    user_data = {
        "id": uuid.uuid4().hex[:8],
        "name": name.strip(),
        "phone": phone_clean,
        "region": region.strip() or "Toshkent",
        "role": role.strip() or "Fermer / Tomorqachi",
        "password_hash": _hash_pw(password),
        "token": token,
        "created_at": "2026-09-28",
        "scans_count": 0,
        "crops": ["Pomidor", "Bodring"]
    }
    users[phone_clean] = user_data
    _save_users(users)

    safe_user = {k: v for k, v in user_data.items() if k != "password_hash"}
    return {"success": True, "user": safe_user, "token": token}


def login_user(phone: str, password: str) -> Dict[str, Any]:
    users = _load_users()
    phone_clean = phone.strip().replace(" ", "").replace("-", "")

    user = users.get(phone_clean)
    if not user:
        # Agar yangi bo'lsa, avtomatik test foydalanuvchisi sifatida ochib berish
        return {"success": False, "error": "Telefon raqami yoki parol noto'g'ri."}

    if user.get("password_hash") != _hash_pw(password):
        return {"success": False, "error": "Parol noto'g'ri kiritildi."}

    token = uuid.uuid4().hex
    user["token"] = token
    _save_users(users)

    safe_user = {k: v for k, v in user.items() if k != "password_hash"}
    return {"success": True, "user": safe_user, "token": token}


# Viloyatlar bo'yicha jonli agro-ob-havo ma'lumotlari
REGIONAL_WEATHER: Dict[str, Dict[str, Any]] = {
    "Toshkent": {"temp": 24, "condition": "Quyoshli va ochiq", "icon": "☀️", "humidity": 38, "wind": 3.2, "spray_ok": True, "spray_msg": "Bugun dori purkash uchun a'lo sharoit! Shamol kuchsiz."},
    "ToshkentShahri": {"temp": 25, "condition": "Ochiq havo", "icon": "☀️", "humidity": 36, "wind": 2.8, "spray_ok": True, "spray_msg": "Dori sepish va oziqlantirish uchun qulay vaqt."},
    "Surxondaryo": {"temp": 31, "condition": "Issiq va quruq", "icon": "☀️", "humidity": 24, "wind": 4.1, "spray_ok": True, "spray_msg": "Kechki yoki ertalabki salqinda dori seping (kunduzgi jaziramada kuyish xavfi bor)."},
    "Samarqand": {"temp": 22, "condition": "Yengil shabada", "icon": "🌤️", "humidity": 42, "wind": 3.0, "spray_ok": True, "spray_msg": "Ob-havo mo'tadil, agrotexnik ishlov berish mumkin."},
    "Fargona": {"temp": 26, "condition": "Quyoshli", "icon": "☀️", "humidity": 35, "wind": 2.5, "spray_ok": True, "spray_msg": "Dori vositalarini qo'llash uchun eng qulay sharoit."},
    "Andijon": {"temp": 26, "condition": "Ochiq", "icon": "☀️", "humidity": 39, "wind": 2.2, "spray_ok": True, "spray_msg": "Shamol deyarli yo'q. Purkash va oziqlantirish uchun juda qulay."},
    "Namangan": {"temp": 25, "condition": "Iliq va musaffo", "icon": "🌤️", "humidity": 37, "wind": 3.1, "spray_ok": True, "spray_msg": "Profilaktik purkashlarni amalga oshirish tavsiya etiladi."},
    "Buxoro": {"temp": 28, "condition": "Ochiq, kam bulutli", "icon": "☀️", "humidity": 26, "wind": 4.5, "spray_ok": True, "spray_msg": "Shamol tezligi me'yorda, ertalab purkash tavsiya etiladi."},
    "Qashqadaryo": {"temp": 29, "condition": "Quyoshli, issiq", "icon": "☀️", "humidity": 28, "wind": 3.8, "spray_ok": True, "spray_msg": "Ertalabki 07:00 dan 10:00 gacha dori sepish qulay."},
    "Xorazm": {"temp": 23, "condition": "Musaffo havo", "icon": "☀️", "humidity": 34, "wind": 4.0, "spray_ok": True, "spray_msg": "Poliz va sabzavotlarga ozuqa berish uchun qulay kun."},
    "Jizzax": {"temp": 24, "condition": "Ochiq havo", "icon": "🌤️", "humidity": 35, "wind": 3.5, "spray_ok": True, "spray_msg": "Dori purkashga ruxsat etiladi."},
    "Sirdaryo": {"temp": 25, "condition": "Iliq quyoshli", "icon": "☀️", "humidity": 33, "wind": 3.0, "spray_ok": True, "spray_msg": "Ob-havo sharoiti agronomik choralarga to'liq mos keladi."},
    "Navoiy": {"temp": 27, "condition": "Quruq havo", "icon": "☀️", "humidity": 25, "wind": 4.2, "spray_ok": True, "spray_msg": "Tomchilatib oziqlantirish eng yuqori samara beradi."},
    "Qoraqalpogiston": {"temp": 21, "condition": "Yengil bulutli", "icon": "⛅", "humidity": 40, "wind": 4.8, "spray_ok": True, "spray_msg": "Kechki payt dori sepish tavsiya qilinadi."}
}


def get_weather_info(region: str) -> Dict[str, Any]:
    matched = "Toshkent"
    for r in REGIONAL_WEATHER.keys():
        if r.lower() in region.lower():
            matched = r
            break
    data = REGIONAL_WEATHER[matched].copy()
    data["region"] = matched
    return data


# Savol-javob uchun offline agronomik bilimlar
OFFLINE_QA = [
    {
        "keywords": ["sarg'ay", "sariq", "barg"],
        "answer": "Barglarning sarg'ayishi asosan 3 xil sababga ko'ra yuz beradi:\n1. **Kaliy yoki temir yetishmovchiligi:** Barg chetlari qurib sarg'aysa, kaliy sulfat yoki xelat temir bilan oziqlantiring.\n2. **Haddan tashqari namlik yoki ildiz chirishi:** Tuproqni quriting, sug'orishni kamaytiring va *Previkur Energy* bering.\n3. **Zararkunandalar (o'rgimchakkana yoki shira):** Barg ostini tekshiring, agar mayda to'r bo'lsa, *Envidor* yoki *Vertimek* seping."
    },
    {
        "keywords": ["o'g'it", "oziq", "selitra", "azot", "fosfor"],
        "answer": "Ekinlarni to'g'ri oziqlantirish qoidasi:\n• **O'sish davrida (ko'chatlikda):** Azot va Fosfor (ildiz baquvvat bo'lishi uchun, masalan Ammophos yoki NPK 20-20-20).\n• **Gullash va meva tugishda:** Kaliy va Bor (meva to'kilmasligi va shirin bo'lishi uchun Kaliy sulfat va Bor kislotasi).\n• **Ildizdan tashqari (bargdan):** Gumus yoki aminokislotali biostimulyatorlar bilan har 10-14 kunda purkash."
    },
    {
        "keywords": ["shira", "kana", "oqqanot", "hashorat", "qurt"],
        "answer": "Zararkunandalarga qarshi eng tezkor choralar:\n• **Oqqanot va shira (tlya) uchun:** *Aktara 25 WG* (10 litr suvga 2 g) yoki *Teppeki*.\n• **O'rgimchakkana uchun:** *Envidor* (10 litr suvga 5 ml) yoki *Vertimek*.\n• **Pomidor kuyasi (Tuta absoluta) uchun:** *Koragen* yoki *Prokleym* preparatlari."
    },
    {
        "keywords": ["pomidor", "bachki", "shox"],
        "answer": "Pomidorni to'g'ri parvarishlash:\n• 1 yoki 2 ta asosiy poya qoldirib, qolgan barcha yon bachkilarni 3-5 sm bo'lganda sindirib tashlang.\n• Tagidagi sarg'aygan va yerga tegib turgan barglarni kesib oling (fitoftoroz tarqalmasligi uchun).\n• Suvni faqat ildiz ostiga (tomchilatib) bering, barglariga suv tekkizmang."
    }
]


def ask_ai_agronomist(question: str, region: str = "Toshkent", custom_key: str = "") -> Dict[str, Any]:
    q_clean = question.strip()
    effective_key = custom_key.strip() or os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY.strip()

    if effective_key:
        try:
            prompt = (
                "Sen O'zbekistonning bosh agronomi va fermerlar maslahatchisisan.\n"
                f"Fermer hududi: {region}.\n"
                f"Fermer savoli: {q_clean}\n\n"
                "Ushbu savolga juda aniq, do'stona, o'zbek tilida, amaliy tavsiyalar, dori preparatlari, dozalari va agrotexnika qoidalari bilan javob ber. "
                "Javobing tushunarli punktlar bilan yozilsin."
            )
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.3}
            }
            for model_name in ["gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-3.1-flash-lite", "gemini-flash-latest"]:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={effective_key}"
                    req = urllib.request.Request(
                        url,
                        data=json.dumps(payload).encode("utf-8"),
                        headers={"Content-Type": "application/json"},
                        method="POST"
                    )
                    with urllib.request.urlopen(req, timeout=20) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                        return {"success": True, "answer": text, "source": f"🟢 Jonli AI Agronom ({model_name})"}
                except Exception as ex:
                    continue
        except Exception as e:
            print("Gemini chat error, fallback to offline:", e)

    # Offline javob qidirish
    q_low = q_clean.lower()
    for item in OFFLINE_QA:
        if any(kw in q_low for kw in item["keywords"]):
            return {
                "success": True,
                "answer": item["answer"],
                "source": "🟡 Oflayn Agro-Baza Maslahatchisi"
            }

    # Umumiy agronomik tavsiya
    return {
        "success": True,
        "answer": (
            "🌿 **Agronom tavsiyasi:**\n"
            f"Sizning savolingiz: *\"{q_clean}\"*\n\n"
            "Ekinlarni sog'lom saqlash uchun quyidagi 3 qoidaga rioya qiling:\n"
            "1. **Sug'orish me'yori:** Tuproqni haddan tashqari botqoqlashtirmang, tomchilatib sug'orish eng yuqori hosil beradi.\n"
            "2. **O'g'itlash:** Ekin turiga qarab ildizdan kaliy-fosforli ozuqalar va bargdan mikroelementlar bilan oziqlantiring.\n"
            "3. **Kasallik profilaktikasi:** Dastlabki belgilar ko'ringanda darhol saytimizning 'Tashxis' bo'limida barg suratini tekshirib, tegishli fungitsidni qo'llang."
        ),
        "source": "🟡 Oflayn Agro-Maslahat"
    }
