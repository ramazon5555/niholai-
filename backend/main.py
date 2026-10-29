import os
import json
import base64
import sqlite3
import hashlib
from datetime import datetime, timedelta
import requests
import jwt
from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
SECRET_KEY = "niholai_super_secret_jwt_key_2026"
ALGORITHM = "HS256"

os.makedirs("static/icons", exist_ok=True)

app = FastAPI(title="NiholAI Smart Diagnostic API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

DB_PATH = "backend/niholai.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            region TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plant_name TEXT,
            disease_name TEXT,
            status TEXT,
            severity TEXT,
            result_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password: str) -> str:
    salt = "niholai_salt_secure"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password

# === AUTH ===
class UserRegister(BaseModel):
    name: str
    phone: str
    region: str = "Toshkent"
    role: str = "Fermer"
    password: str

class UserLogin(BaseModel):
    phone: str
    password: str

@app.post("/api/auth/register")
def register(user: UserRegister):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE phone = ?", (user.phone,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Ushbu telefon raqami allaqachon mavjud")
    
    pwd_h = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (name, phone, region, role, password_hash) VALUES (?, ?, ?, ?, ?)",
        (user.name, user.phone, user.region, user.role, pwd_h)
    )
    conn.commit()
    uid = cursor.lastrowid
    conn.close()
    
    token = jwt.encode(
        {"user_id": uid, "phone": user.phone, "name": user.name, "exp": datetime.utcnow() + timedelta(days=30)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"success": True, "token": token, "user": {"id": uid, "name": user.name, "phone": user.phone, "region": user.region, "role": user.role}}

@app.post("/api/auth/login")
def login(user: UserLogin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, region, role, password_hash FROM users WHERE phone = ?", (user.phone,))
    row = cursor.fetchone()
    conn.close()
    
    if not row or not verify_password(user.password, row[5]):
        raise HTTPException(status_code=400, detail="Telefon raqam yoki parol noto'g'ri")
    
    uid, name, phone, region, role, _ = row
    token = jwt.encode(
        {"user_id": uid, "phone": phone, "name": name, "exp": datetime.utcnow() + timedelta(days=30)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"success": True, "token": token, "user": {"id": uid, "name": name, "phone": phone, "region": region, "role": role}}

# === STATIK & PWA ===
@app.get("/")
def serve_home():
    return FileResponse("index.html")

@app.get("/manifest.json")
def get_manifest():
    if os.path.exists("manifest.json"):
        return FileResponse("manifest.json")
    return {"name": "NiholAI", "short_name": "NiholAI", "start_url": "/"}

@app.get("/sw.js")
def get_sw():
    if os.path.exists("sw.js"):
        return FileResponse("sw.js", media_type="application/javascript")
    return Response(content="// sw", media_type="application/javascript")

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "gemini_active": bool(GEMINI_KEY),
        "database": "sqlite_connected"
    }

# === OB-HAVO ===
@app.get("/api/weather")
def get_weather(region: str = "Toshkent"):
    temp, hum, wind = 21.3, 33, 10
    daily_min, daily_max = 12.0, 23.0
    COORDS = {
        "Toshkent": (41.2995, 69.2401), "Samarqand": (39.6542, 66.9597),
        "Farg'ona": (40.3842, 71.7843), "Andijon": (40.7821, 72.3442),
        "Namangan": (40.9983, 71.6726), "Buxoro": (39.7747, 64.4286),
        "Xorazm": (41.5562, 60.6315), "Qashqadaryo": (38.8606, 65.7891),
        "Surxondaryo": (37.2242, 67.2783), "Jizzax": (40.1158, 67.8422),
        "Sirdaryo": (40.8436, 68.6617), "Navoiy": (40.0844, 65.3792),
        "Qoraqalpog'iston": (42.4619, 59.6166)
    }
    lat, lon = COORDS.get(region, (41.2995, 69.2401))
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        res = requests.get(url, timeout=2.0).json()
        curr = res.get("current", {})
        daily = res.get("daily", {})
        temp = float(curr.get("temperature_2m", temp))
        hum = int(curr.get("relative_humidity_2m", hum))
        wind = float(curr.get("wind_speed_10m", wind))
        if daily.get("temperature_2m_min"):
            daily_min = float(daily["temperature_2m_min"][0])
            daily_max = float(daily["temperature_2m_max"][0])
    except Exception:
        pass

    msg = "Kuz fasli: fosfor-kaliyli o'g'itlar berish, xazonrezgilik oldi parvarishi va zamburug' profilaktikasi davri."

    return {
        "success": True,
        "region": region,
        "temp": temp,
        "temperature": temp,
        "humidity": hum,
        "wind": wind,
        "tip": msg,
        "advice": msg,
        "agro_tip": msg,
        "recommendation": msg,
        "text": msg,
        "desc": "Kuzgi havo",
        "forecast": [
            {"day": "Ertaga", "temp": f"{daily_max}°C", "desc": "Kuzgi ochiq havo"},
            {"day": "Tungi", "temp": f"{daily_min}°C", "desc": "Salqin"}
        ]
    }

# === APTEKALAR ===
@app.get("/api/pharmacies")
def get_pharmacies(region: str = "Barchasi"):
    return {
        "success": True,
        "pharmacies": [
            {"id": 1, "name": "AgroKimyo Markaz", "region": "Toshkent", "phone": "+998 71 200-11-22", "address": "Chilonzor tumani", "rating": 4.9},
            {"id": 2, "name": "Baraka Hosil Savdo", "region": "Samarqand", "phone": "+998 66 233-44-55", "address": "Samarqand sh.", "rating": 4.8}
        ]
    }

# === TARIX ===
@app.get("/api/history")
def get_diagnoses_history():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, plant_name, disease_name, status, severity, created_at, result_json FROM diagnoses ORDER BY id DESC LIMIT 30")
    rows = cur.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "id": r[0],
            "plant_name": r[1],
            "disease_name": r[2],
            "status": r[3],
            "severity": r[4],
            "created_at": r[5],
            "details": json.loads(r[6]) if r[6] else {}
        })
    return {"success": True, "history": history}

# === DIAGNOSTIKA ===
@app.post("/api/diagnose")
async def diagnose_leaf(file: UploadFile = File(...), authorization: str = Header(None)):
    contents = await file.read()
    b64_image = base64.b64encode(contents).decode("utf-8")
    mime_type = file.content_type or "image/jpeg"

    prompt = """Sen tajribali agronom va o'simliklar patologisan.
Ushbu fotosuratni diqqat bilan o'rganib chiq.
O'simlik turini aniqla va unda kasallik bor-yo'qligini aniq ko'rsat.
Faqat JSON formatda javob ber:
{
  "is_plant": true,
  "plant_name": "O'simlik nomi",
  "status": "Kasallangan yoki Sog'lom",
  "disease_name": "Kasallik nomi yoki Sog'lom o'simlik",
  "confidence": 95,
  "severity": "Past yoki O'rtacha yoki Yuqori",
  "symptoms": "Alomatlar tavsifi",
  "causes": "Kasallik sababi",
  "treatment": ["1. Davolash chorasi", "2. Tavsiya etiladigan preparat"],
  "prevention": ["Oldini olish chorasi"]
}"""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": mime_type, "data": b64_image}}
            ]
        }],
        "generationConfig": {
            "temperature": 0.1,
            "response_mime_type": "application/json"
        }
    }

    result = None
    models = ["gemini-flash-latest", "gemini-3.5-flash", "gemini-pro-latest"]
    for m in models:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_KEY}"
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                result = json.loads(text.strip())
                result["success"] = True
                result["source"] = f"🟢 Jonli Gemini AI ({m})"
                break
        except Exception:
            continue

    if not result:
        try:
            from backend.ml_model import predict_leaf_disease
            result = predict_leaf_disease(contents)
        except Exception:
            result = {
                "success": True,
                "is_plant": True,
                "plant_name": "O'simlik bargi",
                "status": "Tekshiruv talab qilinadi",
                "disease_name": "Profilaktik ko'rik",
                "confidence": 80,
                "severity": "Past",
                "symptoms": "Barg yuzasida mayda o'zgarishlar bor.",
                "causes": "Mavsumiy omillar.",
                "treatment": ["Bargni toza tuting."],
                "prevention": ["Profilaktika qiling."],
                "source": "🧠 Lokal Zaxira Modeli"
            }

    # Foydalanuvchi ID sini aniqlash
    current_uid = 1
    if authorization and authorization.startswith("Bearer "):
        try:
            token = authorization.split(" ")[1]
            payload_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            current_uid = payload_data.get("user_id", 1)
        except Exception:
            current_uid = 1

    # Natijani SQLite bazasiga saqlash
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO diagnoses (user_id, plant_name, disease_name, status, severity, result_json) VALUES (?, ?, ?, ?, ?, ?)",
            (
                current_uid,
                result.get("plant_name", "Noma'lum"),
                result.get("disease_name", "Noma'lum"),
                result.get("status", "Tahlil qilindi"),
                result.get("severity", "Past"),
                json.dumps(result, ensure_ascii=False)
            )
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

    return result
