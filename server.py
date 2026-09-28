#!/usr/bin/env python3
"""
Nihol AI - Asosiy FastAPI Web Serveri.
Foydalanuvchi interfeysi (index.html) va AI tahlil API'larini taqdim etadi.
"""

import os
import shutil
import uuid
from pathlib import Path
from fastapi import FastAPI, File, Header, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import UPLOAD_DIR, GEMINI_API_KEY
from detector import PlantDiseaseDetector

app = FastAPI(
    title="NiholAI - O'simliklar va Ekinlar Diagnostika Platformasi",
    description="HCI Talaba Loyihasi + Jonli Gemini Vision AI Backend",
    version="3.0.0",
)

# CORS ruxsatnomasi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = PlantDiseaseDetector()
BASE_DIR = Path(__file__).resolve().parent


@app.get("/", response_class=HTMLResponse)
async def home_page():
    index_file = BASE_DIR / "index.html"
    if index_file.exists():
        with open(index_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h3>NiholAI index.html topilmadi</h3>", status_code=404)


@app.get("/api/status")
async def get_system_status():
    env_key = bool(os.getenv("GEMINI_API_KEY", "").strip() or GEMINI_API_KEY.strip())
    return {
        "status": "online",
        "env_key_available": env_key,
        "mode": "live_gemini" if env_key else "offline_template",
    }


@app.post("/api/diagnose")
async def diagnose_leaf(
    file: UploadFile = File(...),
    x_gemini_key: str = Header(default="", alias="X-Gemini-Key"),
):
    """
    O'simlik bargining rasmini tahlil qilib, kasallik, sabab va davolash choralarini aniqlaydi.
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
