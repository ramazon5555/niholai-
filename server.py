#!/usr/bin/env python3
"""
Nihol AI - Asosiy FastAPI Web Serveri.
Foydalanuvchi interfeysi (index.html), AI tahlil API'lari,
Agro-aptekalar, Dori vositalari hamda PWA (mobil ilova) xizmatlarini taqdim etadi.
"""

import os
import shutil
import uuid
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Header, UploadFile, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import UPLOAD_DIR, GEMINI_API_KEY
from detector import PlantDiseaseDetector
from pharmacies import get_pharmacies, get_medicines_for_diagnosis, AGRO_PHARMACIES, AGRO_MEDICINES
from farmer_advisor import get_region_crop_recommendations, calculate_crop_plan
from auth_service import register_user, login_user, get_weather_info, ask_ai_agronomist

app = FastAPI(
    title="NiholAI — O'simliklar Diagnostikasi va Agro-Yordamchi",
    description="Jonli Gemini Vision AI, Offline Agro-Baza, Agro-Aptekalar va PWA Mobil Ilova Serveri",
    version="4.0.0",
)

# CORS ruxsatnomasi (barcha mijozlar va Telegram WebApp uchun)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Statik fayllarni ulash
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

detector = PlantDiseaseDetector()


@app.get("/", response_class=HTMLResponse)
async def home_page():
    index_file = BASE_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>NiholAI index.html topilmadi</h3>", status_code=404)


@app.get("/manifest.json")
async def get_manifest():
    manifest_file = STATIC_DIR / "manifest.json"
    if manifest_file.exists():
        return FileResponse(manifest_file, media_type="application/manifest+json")
    return JSONResponse(status_code=404, content={"error": "Manifest topilmadi"})


@app.get("/sw.js")
async def get_service_worker():
    sw_file = STATIC_DIR / "sw.js"
    if sw_file.exists():
        return FileResponse(sw_file, media_type="application/javascript")
    return JSONResponse(status_code=404, content={"error": "Service worker topilmadi"})


@app.get("/api/status")
async def get_system_status():
    env_key = bool(os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY.strip())
    return {
        "status": "online",
        "env_key_available": env_key,
        "mode": "live_gemini" if env_key else "offline_template",
        "app_name": "NiholAI Mobile",
        "version": "4.0.0",
    }


@app.post("/api/diagnose")
async def diagnose_leaf(
    file: UploadFile = File(...),
    x_gemini_key: str = Header(default="", alias="X-Gemini-Key"),
):
    """
    O'simlik bargining rasmini tahlil qilib, kasallik, sabab, davolash choralari,
    tavsiya etiladigan preparatlar (dori vositalari) va eng yaqin apteka tavsiyalarini aniqlaydi.
    """
    ext = Path(file.filename or "leaf.jpg").suffix or ".jpg"
    unique_filename = f"leaf_{uuid.uuid4().hex}{ext}"
    saved_path = UPLOAD_DIR / unique_filename

    try:
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = detector.analyze_image(saved_path, override_api_key=x_gemini_key)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.post("/api/identify")
async def identify_plant_species(
    file: UploadFile = File(...),
    x_gemini_key: str = Header(default="", alias="X-Gemini-Key"),
):
    """
    Fotosuratdagi o'simlik turini, oilasini va parvarishlash shartlarini aniqlaydi.
    """
    ext = Path(file.filename or "plant.jpg").suffix or ".jpg"
    unique_filename = f"plant_{uuid.uuid4().hex}{ext}"
    saved_path = UPLOAD_DIR / unique_filename

    try:
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = detector.identify_plant(saved_path, override_api_key=x_gemini_key)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.get("/api/pharmacies")
async def list_pharmacies(
    region: Optional[str] = Query(default=None, description="Viloyat nomi"),
    search: Optional[str] = Query(default=None, description="Qidiruv so'zi"),
):
    """
    O'zbekiston viloyatlari bo'yicha Agro-Aptekalar va o'simliklarni himoya qilish markazlarini qaytaradi.
    """
    pharmacies = get_pharmacies(region=region, search=search)
    return {
        "success": True,
        "count": len(pharmacies),
        "region": region or "Barchasi",
        "pharmacies": pharmacies,
    }


@app.get("/api/medicines")
async def list_medicines(
    disease: Optional[str] = Query(default="", description="Kasallik nomi"),
    plant: Optional[str] = Query(default="", description="O'simlik turi"),
    status: Optional[str] = Query(default="", description="Holati"),
):
    """
    Kasallik yoki holat bo'yicha tavsiya etiladigan rasmiy dori vositalarini qaytaradi.
    """
    medicines = get_medicines_for_diagnosis(disease_name=disease, plant_name=plant, status=status)
    return {
        "success": True,
        "count": len(medicines),
        "disease": disease,
        "medicines": medicines,
    }


@app.get("/api/farmer/recommendations")
async def get_farmer_recommendations(
    region: str = Query(default="Toshkent"),
    land_size: float = Query(default=10.0),
    unit: str = Query(default="sotix"),
):
    """
    Viloyat ob-havosi, tuproq sharoiti va yer hajmiga asoslangan holda ekin tavsiyalarini qaytaradi.
    """
    res = get_region_crop_recommendations(region=region, land_size=land_size, unit=unit)
    return JSONResponse(content=res)


@app.get("/api/farmer/calculate")
async def calculate_farmer_plan(
    region: str = Query(default="Toshkent"),
    crop: str = Query(default="Pomidor"),
    land_size: float = Query(default=10.0),
    unit: str = Query(default="sotix"),
    plants: Optional[int] = Query(default=None),
    price: Optional[float] = Query(default=None),
):
    """
    Tanlangan ekin, ko'chat/urug' sarfi, bitta tupdan va umumiy hosil hamda daromadni hisoblaydi.
    """
    res = calculate_crop_plan(
        region=region,
        crop_name=crop,
        land_size=land_size,
        unit=unit,
        custom_plants=plants,
        custom_price=price,
    )
    return JSONResponse(content=res)


@app.post("/api/auth/register")
async def api_register(request: Request):
    """
    Fermer yoki bog'bonni tizimda ro'yxatdan o'tkazish.
    """
    try:
        data = await request.json()
        res = register_user(
            name=data.get("name", ""),
            phone=data.get("phone", ""),
            region=data.get("region", "Toshkent"),
            role=data.get("role", "Fermer"),
            password=data.get("password", "")
        )
        return JSONResponse(content=res, status_code=200 if res.get("success") else 400)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.post("/api/auth/login")
async def api_login(request: Request):
    """
    Foydalanuvchi tizimga kirishi.
    """
    try:
        data = await request.json()
        res = login_user(
            phone=data.get("phone", ""),
            password=data.get("password", "")
        )
        return JSONResponse(content=res, status_code=200 if res.get("success") else 400)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@app.get("/api/weather")
async def api_weather(region: str = Query(default="Toshkent")):
    """
    Viloyat ob-havosi, namligi va dori purkash uchun qulaylik indeksi.
    """
    data = get_weather_info(region)
    return JSONResponse(content=data)


@app.post("/api/ai/ask")
async def api_ai_ask(
    request: Request,
    x_gemini_key: str = Header(default="", alias="X-Gemini-Key")
):
    """
    Fermer savollariga jonli AI agronom tomonidan amaliy javob berish.
    """
    try:
        data = await request.json()
        q = data.get("question", "")
        region = data.get("region", "Toshkent")
        res = ask_ai_agronomist(question=q, region=region, custom_key=x_gemini_key)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    uvicorn.run("server:app", host=API_HOST, port=API_PORT, reload=False)
