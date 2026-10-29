"""
Nihol AI - Aqlli Fermerlik va Hosil Prognozi Moduli.
Hudud ob-havosi, tuproq sharoiti va yer hajmiga asoslangan holda ekin tavsiyasi,
urug'/ko'chat me'yori, bitta tup va umumiy hosil hamda daromad kalkulyatori.
"""

from typing import Dict, Any, List, Optional
import os
import json
import urllib.request

from config import GEMINI_API_KEY


# O'zbekiston viloyatlari agro-iqlimiy ma'lumotlari
REGIONAL_CLIMATE_PROFILES: Dict[str, Dict[str, Any]] = {
    "Surxondaryo": {
        "title": "Surxondaryo viloyati",
        "climate_type": "Quruq subtropik, erta bahor, uzoq issiq yoz",
        "avg_temp": "Bahor: 18-24°C, Yoz: 35-42°C",
        "favorable_crops": ["Pomidor", "Bodring", "Qalampir", "Qovun/Tarvuz", "Piyoz"],
        "yield_factor": 1.15,
        "soil": "Och tusli bo'z tuproq, qumloq, unumdor",
        "summary": "O'zbekistonda eng erta hosil pishadigan hudud. Plyonka ostiga va ochiq dalaga erta bahorgi issiqsevar ekinlar (pomidor, bodring, poliz) juda yuqori hosil beradi."
    },
    "Qashqadaryo": {
        "title": "Qashqadaryo viloyati",
        "climate_type": "Keskin kontinental, issiq va quruq yoz",
        "avg_temp": "Bahor: 16-22°C, Yoz: 34-40°C",
        "favorable_crops": ["Qovun/Tarvuz", "Pomidor", "Kartoshka", "Piyoz"],
        "yield_factor": 1.05,
        "soil": "Bo'z tuproq, cho'l-qumloq yerlar",
        "summary": "Quyoshli kunlar ko'p, poliz ekinlari (qovun, tarvuz) va erta-kechki pomidor uchun juda qulay."
    },
    "Toshkent": {
        "title": "Toshkent viloyati",
        "climate_type": "Mo'tadil kontinental, yaxshi yog'ingarchilik va suv ta'minoti",
        "avg_temp": "Bahor: 14-20°C, Yoz: 30-36°C",
        "favorable_crops": ["Pomidor", "Bodring", "Kartoshka", "Karam", "Sabzi", "Qalampir"],
        "yield_factor": 1.15,
        "soil": "Tipik bo'z va o'tloqi unumdor tuproq",
        "summary": "Serhosil va suvli hudud. Issiqxona va ochiq dalada pomidor, bodring, karam va mevali ko'chatlar eng yuqori hosil beradi."
    },
    "ToshkentShahri": {
        "title": "Toshkent shahri",
        "climate_type": "Mo'tadil, issiqxona va shahar atrofida dehqonchilik",
        "avg_temp": "Bahor: 15-21°C, Yoz: 32-38°C",
        "favorable_crops": ["Bodring", "Pomidor", "Ko'katlar", "Qalampir"],
        "yield_factor": 1.10,
        "soil": "Madaniylashgan unumdor tuproq",
        "summary": "Shahar atrofidagi issiqxonalar va tomorqalar uchun erta pishar pomidor, bodring va ko'katlar eng serdaromad hisoblanadi."
    },
    "Samarqand": {
        "title": "Samarqand viloyati",
        "climate_type": "Tog'oldi mo'tadil iqlim, qulay namlik",
        "avg_temp": "Bahor: 14-19°C, Yoz: 29-35°C",
        "favorable_crops": ["Kartoshka", "Pomidor", "Piyoz", "Sabzi", "Bodring"],
        "yield_factor": 1.10,
        "soil": "Qoramtir-bo'z va qumoq unumdor tuproq",
        "summary": "O'zbekistonning kartoshkachilik va sabzavotchilik markazi. Kartoshka va sabzi yetishtirish uchun eng maqbul iqlim va tuproqqa ega."
    },
    "Fargona": {
        "title": "Farg'ona viloyati",
        "climate_type": "Vodiy iqlimi, yumshoq bahor, quyoshli yoz",
        "avg_temp": "Bahor: 15-21°C, Yoz: 31-37°C",
        "favorable_crops": ["Bodring", "Pomidor", "Qalampir", "Karam", "Sabzi"],
        "yield_factor": 1.12,
        "soil": "Sug'oriladigan o'tloqi-bo'z tuproq",
        "summary": "Farg'ona vodiysining unumdor yerlari har tup ko'chatdan maksimal hosil olish imkonini beradi. Issiqxona va ochiq maydonlar juda serhosil."
    },
    "Andijon": {
        "title": "Andijon viloyati",
        "climate_type": "Iliq vodiy iqlimi, yer unumdorligi juda yuqori",
        "avg_temp": "Bahor: 15-21°C, Yoz: 30-36°C",
        "favorable_crops": ["Pomidor", "Bodring", "Qalampir", "Karam", "Kartoshka"],
        "yield_factor": 1.15,
        "soil": "Yuqori unumdor o'tloqi tuproq",
        "summary": "Aholi zich va yer juda qadrli. Tomorqa va fermer xo'jaliklarida pomidor, bodring va qalampir yetishtirish eng katta foyda keltiradi."
    },
    "Namangan": {
        "title": "Namangan viloyati",
        "climate_type": "Tog' etagi va tekislik, quyoshli, qulay sharoit",
        "avg_temp": "Bahor: 14-20°C, Yoz: 31-36°C",
        "favorable_crops": ["Pomidor", "Bodring", "Qalampir", "Piyoz", "Sabzi"],
        "yield_factor": 1.10,
        "soil": "Bo'z va qumoq tuproq",
        "summary": "Sabzavot va meva yetishtirishda yetakchi. Ko'chatlar tez ildiz otadi va erta hosil beradi."
    },
    "Buxoro": {
        "title": "Buxoro viloyati",
        "climate_type": "Cho'l-kontinental, quruq issiq, sho'rlanishga moyil",
        "avg_temp": "Bahor: 16-22°C, Yoz: 35-41°C",
        "favorable_crops": ["Qovun/Tarvuz", "Piyoz", "Pomidor", "Sabzi"],
        "yield_factor": 0.95,
        "soil": "Allyuvial va o'tloqi sho'rxok tuproq",
        "summary": "Quyoshli issiq iqlim qovun, tarvuz va piyoz uchun nihoyatda qulay. Shiradorlik darajasi eng yuqori bo'ladi."
    },
    "Xorazm": {
        "title": "Xorazm viloyati",
        "climate_type": "Keskin kontinental, o'ziga xos toza quyosh nuri",
        "avg_temp": "Bahor: 13-19°C, Yoz: 32-38°C",
        "favorable_crops": ["Qovun/Tarvuz", "Piyoz", "Bodring", "Sabzi"],
        "yield_factor": 1.00,
        "soil": "Amudaryo allyuvial unumdor tuproqlari",
        "summary": "Mashhur Xorazm qovunlari va shirin sabzi yurti. Poliz va piyoz ekish eng yaxshi iqtisodiy natija beradi."
    },
    "Jizzax": {
        "title": "Jizzax viloyati",
        "climate_type": "Tog' etagi va dasht, havo ochiq",
        "avg_temp": "Bahor: 14-20°C, Yoz: 32-38°C",
        "favorable_crops": ["Qovun/Tarvuz", "Pomidor", "Piyoz", "Kartoshka"],
        "yield_factor": 0.98,
        "soil": "Och va tipik bo'z tuproq",
        "summary": "Dasht va tog'oldi sharoitida qovun (Jizzax qovunlari), pomidor va piyoz yaxshi hosil beradi."
    },
    "Sirdaryo": {
        "title": "Sirdaryo viloyati",
        "climate_type": "Cho'l-dasht, grunt suvlari yaqin",
        "avg_temp": "Bahor: 15-21°C, Yoz: 33-39°C",
        "favorable_crops": ["Qovun/Tarvuz", "Pomidor", "Piyoz", "Bodring"],
        "yield_factor": 0.95,
        "soil": "O'tloqi-bo'z va sho'rtob tuproq",
        "summary": "Polizchilik (qovun va tarvuz) va erta pomidor ekish tavsiya qilinadi."
    },
    "Navoiy": {
        "title": "Navoiy viloyati",
        "climate_type": "Cho'l zonasi, issiq va kam yog'inli",
        "avg_temp": "Bahor: 15-21°C, Yoz: 35-42°C",
        "favorable_crops": ["Qovun/Tarvuz", "Piyoz", "Pomidor"],
        "yield_factor": 0.88,
        "soil": "Cho'l va qumloq yerlar",
        "summary": "Tomchilatib sug'orish orqali poliz ekinlari va piyozdan yaxshi daromad olish mumkin."
    },
    "Qoraqalpogiston": {
        "title": "Qoraqalpog'iston Respublikasi",
        "climate_type": "Keskin kontinental, qisqa issiq yoz",
        "avg_temp": "Bahor: 12-18°C, Yoz: 33-39°C",
        "favorable_crops": ["Qovun/Tarvuz", "Piyoz", "Sabzi", "Pomidor"],
        "yield_factor": 0.85,
        "soil": "Sho'rxok va qumloq allyuvial tuproq",
        "summary": "Sho'rga chidamli poliz ekinlari, piyoz va sabzi yetishtirish eng xavfsiz va samarali yo'l hisoblanadi."
    }
}


# Ekinlar agrotexnik parametrlari
CROP_SPECS: Dict[str, Dict[str, Any]] = {
    "Pomidor": {
        "name": "Pomidor (Nihol / Ko'chat)",
        "icon": "🍅",
        "plants_per_sotix": 330,  # 1 sotix = 100 kv.m -> 70x30 sm da ~330 tup
        "seed_per_sotix_grams": 4, # urug'dan o'stirilganda
        "unit_type": "kochat",
        "spacing": "70 x 30 sm",
        "yield_per_plant_min": 2.5,
        "yield_per_plant_max": 4.5,
        "default_price": 4000,
        "description": "Eng yuqori talabga ega sabzavot. Bozor narxi erta bahor va kech kuzda juda yuqori bo'ladi.",
        "tips": "Tomchilatib sug'orishni qo'llang, ortiqcha bachkilarni har haftada olib tashlang."
    },
    "Bodring": {
        "name": "Bodring (Tez hosilli)",
        "icon": "🥒",
        "plants_per_sotix": 380,
        "seed_per_sotix_grams": 80,
        "unit_type": "kochat",
        "spacing": "70 x 25 sm",
        "yield_per_plant_min": 2.0,
        "yield_per_plant_max": 3.8,
        "default_price": 5000,
        "description": "45-50 kunda hosilga kiradi. Har 2-3 kunda terib olinadi va muntazam daromad keltiradi.",
        "tips": "Iliq suv bilan sug'oring, harorat 15°C dan tushib ketmasligini ta'minlang."
    },
    "Qalampir": {
        "name": "Shirin / Achchiq Qalampir",
        "icon": "🫑",
        "plants_per_sotix": 380,
        "seed_per_sotix_grams": 5,
        "unit_type": "kochat",
        "spacing": "70 x 25 sm",
        "yield_per_plant_min": 1.2,
        "yield_per_plant_max": 2.2,
        "default_price": 6500,
        "description": "Bozor narxi juda barqaror va yuqori. Eksportbop mahsulot.",
        "tips": "Ildiz tizimi nozik, chuqur chopmasdan faqat ustki qatlam yumshatiladi."
    },
    "Kartoshka": {
        "name": "Kartoshka (Urug'lik tugunak)",
        "icon": "🥔",
        "plants_per_sotix": 450,
        "seed_per_sotix_kg": 28,  # 1 sotixga ~28 kg urug'lik kartoshka
        "unit_type": "urug",
        "spacing": "70 x 25 sm",
        "yield_per_plant_min": 0.5,
        "yield_per_plant_max": 0.9,
        "default_price": 3500,
        "description": "Ikkinchi non. O'zbekiston ichki bozorida doimiy xaridorgir va kafolatlangan hosil.",
        "tips": "Gullash davrida mo'l sug'oring va tagini 2 marta baland qilib ko'ming."
    },
    "Piyoz": {
        "name": "Piyoz (Erta va O'rta)",
        "icon": "🧅",
        "plants_per_sotix": 8000,
        "seed_per_sotix_kg": 1.8, # mayda sevok piyozbosh
        "unit_type": "urug",
        "spacing": "20 x 8 sm",
        "yield_per_plant_min": 0.12,
        "yield_per_plant_max": 0.22,
        "default_price": 2500,
        "description": "Kam xarajatli va uzoq saqlanuvchi ekin. Mayda boshli sevok orqali tez hosil beradi.",
        "tips": "Hosil yig'ishdan 2 hafta oldin sug'orishni butunlay to'xtatish kerak."
    },
    "Qovun/Tarvuz": {
        "name": "Qovun va Tarvuz (Poliz)",
        "icon": "🍉",
        "plants_per_sotix": 70,
        "seed_per_sotix_grams": 40,
        "unit_type": "kochat",
        "spacing": "200 x 70 sm",
        "yield_per_plant_min": 6.0,
        "yield_per_plant_max": 14.0,
        "default_price": 3000,
        "description": "Katta maydonlarda eng kam mehnat talab qiluvchi va yuqori massa beruvchi poliz ekini.",
        "tips": "Quyoshli ochiq maydonda shakar to'plash davrida suvni me'yorida bering."
    },
    "Sabzi": {
        "name": "Qizil / Sariq Sabzi",
        "icon": "🥕",
        "plants_per_sotix": 12000,
        "seed_per_sotix_grams": 50,
        "unit_type": "urug",
        "spacing": "15 x 5 sm",
        "yield_per_plant_min": 0.08,
        "yield_per_plant_max": 0.15,
        "default_price": 3000,
        "description": "Kuz-qish mavsumida talab juda yuqori bo'lgan sabzavot.",
        "tips": "Yerni chuqur haydab yumshating, shunda sabzi to'g'ri va uzun o'sadi."
    },
    "Karam": {
        "name": "Oqbosh Karam",
        "icon": "🥬",
        "plants_per_sotix": 400,
        "seed_per_sotix_grams": 5,
        "unit_type": "kochat",
        "spacing": "70 x 35 sm",
        "yield_per_plant_min": 1.5,
        "yield_per_plant_max": 3.2,
        "default_price": 2500,
        "description": "Salqin havoni yaxshi ko'radi, 1 sotixdan 1 tonnagacha massa beradi.",
        "tips": "Tuproq doimo nam bo'lishi kerak, zararkunandalardan muntazam himoya qiling."
    }
}


def get_region_crop_recommendations(region: str, land_size: float, unit: str = "sotix") -> Dict[str, Any]:
    """
    Berilgan viloyat va yer hajmiga qarab AI tavsiyalarini tayyorlaydi.
    """
    region_key = region.strip()
    # Normalize region key
    matched_key = "Toshkent"
    for r in REGIONAL_CLIMATE_PROFILES.keys():
        if r.lower() in region_key.lower():
            matched_key = r
            break

    profile = REGIONAL_CLIMATE_PROFILES[matched_key]
    sotix_size = land_size * 100 if unit == "gektar" else land_size

    # Tavsiya etiladigan ekinlar ro'yxati
    recommended_crops = []
    for crop_name in profile["favorable_crops"]:
        spec = CROP_SPECS.get(crop_name)
        if not spec:
            continue

        # Hisob-kitoblar
        total_plants = int(spec["plants_per_sotix"] * sotix_size)
        seed_info = ""
        if spec.get("seed_per_sotix_kg"):
            total_seed_kg = round(spec["seed_per_sotix_kg"] * sotix_size, 1)
            seed_info = f"~{total_seed_kg:g} kg urug'lik"
        elif spec.get("seed_per_sotix_grams"):
            total_seed_g = round(spec["seed_per_sotix_grams"] * sotix_size, 1)
            if total_seed_g >= 1000:
                seed_info = f"~{total_seed_g/1000:.1f} kg urug'"
            else:
                seed_info = f"~{total_seed_g:g} g urug'"

        yield_factor = profile["yield_factor"]
        per_plant_avg = (spec["yield_per_plant_min"] + spec["yield_per_plant_max"]) / 2 * yield_factor
        total_yield_kg = round(total_plants * per_plant_avg, 1)
        est_revenue = round(total_yield_kg * spec["default_price"])

        recommended_crops.append({
            "name": crop_name,
            "display_name": spec["name"],
            "icon": spec["icon"],
            "plants_count": total_plants,
            "seed_info": seed_info,
            "spacing": spec["spacing"],
            "yield_per_plant": f"{spec['yield_per_plant_min']*yield_factor:.1f} - {spec['yield_per_plant_max']*yield_factor:.1f} kg",
            "total_yield_avg_kg": total_yield_kg,
            "default_price": spec["default_price"],
            "estimated_revenue": est_revenue,
            "tips": spec["tips"],
            "description": spec["description"]
        })

    return {
        "success": True,
        "region": profile["title"],
        "climate_type": profile["climate_type"],
        "avg_temp": profile["avg_temp"],
        "soil": profile["soil"],
        "summary": profile["summary"],
        "land_size": land_size,
        "unit": unit,
        "sotix_size": sotix_size,
        "recommended_crops": recommended_crops
    }


def calculate_crop_plan(
    region: str,
    crop_name: str,
    land_size: float,
    unit: str = "sotix",
    custom_plants: Optional[int] = None,
    custom_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Tanlangan ekin, yer hajmi va narx bo'yicha to'liq 3 bosqichli agronomik hosil va foyda hisobi.
    """
    matched_key = "Toshkent"
    for r in REGIONAL_CLIMATE_PROFILES.keys():
        if r.lower() in region.lower():
            matched_key = r
            break

    profile = REGIONAL_CLIMATE_PROFILES[matched_key]
    spec = CROP_SPECS.get(crop_name) or CROP_SPECS["Pomidor"]

    sotix_size = land_size * 100 if unit == "gektar" else land_size
    plants_count = custom_plants if (custom_plants and custom_plants > 0) else int(spec["plants_per_sotix"] * sotix_size)
    price_per_kg = custom_price if (custom_price and custom_price > 0) else spec["default_price"]

    yield_factor = profile["yield_factor"]

    # Bitta tupdan hosil (kg)
    bitta_min = round(spec["yield_per_plant_min"] * yield_factor, 2)
    bitta_max = round(spec["yield_per_plant_max"] * yield_factor, 2)
    bitta_avg = round((bitta_min + bitta_max) / 2, 2)

    # Butun maydondan umumiy hosil (kg)
    umumiy_min_kg = round(plants_count * bitta_min, 1)
    umumiy_max_kg = round(plants_count * bitta_max, 1)
    umumiy_avg_kg = round(plants_count * bitta_avg, 1)

    # Daromad (so'm)
    daromad_min = int(umumiy_min_kg * price_per_kg)
    daromad_avg = int(umumiy_avg_kg * price_per_kg)
    daromad_max = int(umumiy_max_kg * price_per_kg)

    # Urug' / ko'chat normasi tavsifi
    norma_text = f"{plants_count:,} tup ko'chat".replace(",", " ")
    if spec.get("seed_per_sotix_kg"):
        norma_text += f" (yoki ~{round(spec['seed_per_sotix_kg'] * sotix_size, 1)} kg urug'lik)"
    elif spec.get("seed_per_sotix_grams"):
        norma_text += f" (yoki ~{round(spec['seed_per_sotix_grams'] * sotix_size, 1)} g urug')"

    return {
        "success": True,
        "region": profile["title"],
        "crop_name": crop_name,
        "crop_display": spec["name"],
        "icon": spec["icon"],
        "land_size": land_size,
        "unit": unit,
        "sotix_size": sotix_size,
        "plants_count": plants_count,
        "norma_text": norma_text,
        "spacing": spec["spacing"],
        "price_per_kg": int(price_per_kg),
        "per_plant": {
            "min_kg": bitta_min,
            "avg_kg": bitta_avg,
            "max_kg": bitta_max,
        },
        "total_yield": {
            "min_kg": umumiy_min_kg,
            "avg_kg": umumiy_avg_kg,
            "max_kg": umumiy_max_kg,
            "avg_ton": round(umumiy_avg_kg / 1000, 2) if umumiy_avg_kg >= 1000 else None
        },
        "revenue": {
            "min_som": daromad_min,
            "avg_som": daromad_avg,
            "max_som": daromad_max
        },
        "tips": spec["tips"],
        "climate_note": f"{profile['title']} iqlim koeffitsienti: {yield_factor}x. {profile['summary']}"
    }
