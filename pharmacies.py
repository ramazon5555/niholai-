"""
Nihol AI - O'zbekiston bo'yicha Agro-Aptekalar va Dori vositalari ma'lumotlar bazasi.
Fermerlar va dehqonlar uchun ekin kasalliklariga qarshi preparatlar va eng yaqin agro-do'konlar manzillari.
"""

from typing import List, Dict, Any, Optional

# O'zbekiston bo'yicha agro-aptekalar va o'simliklarni himoya qilish markazlari
AGRO_PHARMACIES: List[Dict[str, Any]] = [
    # Toshkent shahri & viloyati
    {
        "id": "tash_01",
        "name": "Agro Kimyo Savdo Markazi",
        "region": "Toshkent shahri",
        "district": "Chilonzor tumani",
        "address": "Kichik halqa yo'li ko'chasi, 42-uy",
        "landmark": "Chilonzor buyum bozori yaqinida",
        "phone": "+998 71 200 45 45",
        "working_hours": "08:00 - 18:00 (Har kuni)",
        "categories": ["Fungitsidlar", "Insektitsidlar", "Biostimulyatorlar", "Urug'lar"],
        "lat": 41.2758,
        "lon": 69.1985,
        "map_url": "https://yandex.uz/maps/?text=41.2758,69.1985",
        "verified": True
    },
    {
        "id": "tash_02",
        "name": "Green Agro Toshkent",
        "region": "Toshkent shahri",
        "district": "Yunusobod tumani",
        "address": "Amir Temur shoh ko'chasi, 114",
        "landmark": "Uchqahramon bozori ro'parasida",
        "phone": "+998 90 912 34 56",
        "working_hours": "08:30 - 19:00",
        "categories": ["Fungitsidlar", "Insektitsidlar", "Tomchilatib sug'orish", "Organik o'g'itlar"],
        "lat": 41.3654,
        "lon": 69.2891,
        "map_url": "https://yandex.uz/maps/?text=41.3654,69.2891",
        "verified": True
    },
    {
        "id": "tash_vil_01",
        "name": "Yangiyo'l Agro Apteka & Urug'chilik",
        "region": "Toshkent viloyati",
        "district": "Yangiyo'l tumani",
        "address": "Toshkent-Samarqand trassasi, 28-km",
        "landmark": "Dehqon bozori markaziy darvozasi yonida",
        "phone": "+998 97 740 11 22",
        "working_hours": "07:30 - 18:30",
        "categories": ["Issiqxona dori vositalari", "Fungitsidlar", "Gumus", "Fitosporin"],
        "lat": 41.1167,
        "lon": 69.0500,
        "map_url": "https://yandex.uz/maps/?text=41.1167,69.0500",
        "verified": True
    },
    {
        "id": "tash_vil_02",
        "name": "Chirchiq Agro Kimyo Servis",
        "region": "Toshkent viloyati",
        "district": "Qibray tumani",
        "address": "Bog'dorchilik ilmiy instituti yo'li, 15",
        "landmark": "Shreder nomidagi bog'dorchilik instituti yaqinida",
        "phone": "+998 93 514 88 99",
        "working_hours": "08:00 - 17:30",
        "categories": ["Meva va uzum dorilari", "Skor", "Xorus", "Tiovit Jet"],
        "lat": 41.3833,
        "lon": 69.4667,
        "map_url": "https://yandex.uz/maps/?text=41.3833,69.4667",
        "verified": True
    },

    # Samarqand viloyati
    {
        "id": "sam_01",
        "name": "Samarqand Markaziy Agro Apteka",
        "region": "Samarqand viloyati",
        "district": "Samarqand shahri",
        "address": "Shohi Zinda ko'chasi, Siab bozori hududi",
        "landmark": "Siab dehqon bozori 4-qator",
        "phone": "+998 66 235 60 70",
        "working_hours": "07:00 - 18:00 (Dushanba dam olish)",
        "categories": ["Fungitsidlar", "Ridomil Gold", "Previkur", "Insektitsidlar"],
        "lat": 39.6633,
        "lon": 66.9786,
        "map_url": "https://yandex.uz/maps/?text=39.6633,66.9786",
        "verified": True
    },
    {
        "id": "sam_02",
        "name": "Jomboy Bog'bon & Dehqon Do'koni",
        "region": "Samarqand viloyati",
        "district": "Jomboy tumani",
        "address": "Mustaqillik shoh ko'chasi, 24",
        "landmark": "Tuman hokimiyati va avtoshohxona oralig'ida",
        "phone": "+998 91 550 44 33",
        "working_hours": "08:00 - 18:00",
        "categories": ["Meva zararkunandalari dori-darmonlari", "Fungitsidlar", "Biopreparatlar"],
        "lat": 39.6983,
        "lon": 67.0944,
        "map_url": "https://yandex.uz/maps/?text=39.6983,67.0944",
        "verified": True
    },

    # Farg'ona vodiysi (Farg'ona, Andijon, Namangan)
    {
        "id": "fer_01",
        "name": "Farg'ona Agro Himoya Markazi",
        "region": "Farg'ona viloyati",
        "district": "Farg'ona shahri",
        "address": "Al-Farg'oniy ko'chasi, 65-bino",
        "landmark": "Markaziy stadion orqa tomoni",
        "phone": "+998 73 224 15 15",
        "working_hours": "08:00 - 18:00",
        "categories": ["Barcha turdagi fungitsidlar", "Gerbitsidlar", "Topaz", "Quadris"],
        "lat": 40.3864,
        "lon": 71.7864,
        "map_url": "https://yandex.uz/maps/?text=40.3864,71.7864",
        "verified": True
    },
    {
        "id": "fer_02",
        "name": "Quva Anor va Ko'chat Dorixonasi",
        "region": "Farg'ona viloyati",
        "district": "Quva tumani",
        "address": "Bog'bonlar ko'chasi, 12",
        "landmark": "Quva markaziy chorrahasi",
        "phone": "+998 90 580 99 00",
        "working_hours": "07:30 - 18:00",
        "categories": ["Ko'chat kasalliklari dori vositalari", "Ildiz stimulyatorlari", "Oltingugurt"],
        "lat": 40.5286,
        "lon": 72.0125,
        "map_url": "https://yandex.uz/maps/?text=40.5286,72.0125",
        "verified": True
    },
    {
        "id": "and_01",
        "name": "Andijon Agro Doktor Servis",
        "region": "Andijon viloyati",
        "district": "Andijon shahri",
        "address": "Bobur shoh ko'chasi, Yangi bozor hududi",
        "landmark": "Yangi bozor qishloq xo'jaligi mollari rastasi",
        "phone": "+998 74 223 88 77",
        "working_hours": "07:00 - 18:30",
        "categories": ["Issiqxona preparatlari", "Pomidor/Bodring dorilari", "Aktara", "Ridomil"],
        "lat": 40.7821,
        "lon": 72.3442,
        "map_url": "https://yandex.uz/maps/?text=40.7821,72.3442",
        "verified": True
    },
    {
        "id": "and_02",
        "name": "Asaka Agro Kimyo Savdo",
        "region": "Andijon viloyati",
        "district": "Asaka tumani",
        "address": "Dehqonobod ko'chasi, 8",
        "landmark": "Asaka markaziy bozori yonida",
        "phone": "+998 93 440 22 11",
        "working_hours": "08:00 - 18:00",
        "categories": ["Fungitsidlar", "Biologik vositalar", "Fitosporin-M"],
        "lat": 40.6417,
        "lon": 72.2389,
        "map_url": "https://yandex.uz/maps/?text=40.6417,72.2389",
        "verified": True
    },
    {
        "id": "nam_01",
        "name": "Namangan Agro Ta'minot Markazi",
        "region": "Namangan viloyati",
        "district": "Namangan shahri",
        "address": "Nodira ko'chasi, Chorsu bozori yonida",
        "landmark": "Chorsu agro mahsulotlar pavilyoni",
        "phone": "+998 69 227 40 50",
        "working_hours": "07:30 - 18:00",
        "categories": ["Gullash va meva turg'unligi", "Fungitsidlar", "Zararkunandalarga qarshi"],
        "lat": 40.9983,
        "lon": 71.6726,
        "map_url": "https://yandex.uz/maps/?text=40.9983,71.6726",
        "verified": True
    },
    {
        "id": "nam_02",
        "name": "Chust Dehqon Madadkor",
        "region": "Namangan viloyati",
        "district": "Chust tumani",
        "address": "Mustaqillik ko'chasi, 77",
        "landmark": "Tuman kasalxonasi ro'parasida",
        "phone": "+998 91 360 12 34",
        "working_hours": "08:00 - 17:30",
        "categories": ["Meva zararkunandalari", "Oltingugurt preparatlari", "Mis kuporosi"],
        "lat": 41.0078,
        "lon": 71.2294,
        "map_url": "https://yandex.uz/maps/?text=41.0078,71.2294",
        "verified": True
    },

    # Buxoro & Navoiy
    {
        "id": "bux_01",
        "name": "Buxoro Agro Zamin Aptekasi",
        "region": "Buxoro viloyati",
        "district": "Buxoro shahri",
        "address": "Ibrohim Mo'minov ko'chasi, Karvon bozori",
        "landmark": "Karvon bozori qishloq xo'jaligi sektori",
        "phone": "+998 65 221 80 90",
        "working_hours": "08:00 - 18:00",
        "categories": ["Sho'rlanishga chidamli ekinlar dori vositalari", "Fungitsidlar", "Gumus"],
        "lat": 39.7747,
        "lon": 64.4286,
        "map_url": "https://yandex.uz/maps/?text=39.7747,64.4286",
        "verified": True
    },
    {
        "id": "nav_01",
        "name": "Navoiy Agro Kimyo Servis",
        "region": "Navoiy viloyati",
        "district": "Navoiy shahri",
        "address": "G'alaba shoh ko'chasi, 31",
        "landmark": "Markaziy vokzal yaqinida",
        "phone": "+998 79 223 11 44",
        "working_hours": "08:30 - 18:00",
        "categories": ["Fungitsidlar", "Biostimulyatorlar", "Tomchilatib oziqlantirish"],
        "lat": 40.0844,
        "lon": 65.3792,
        "map_url": "https://yandex.uz/maps/?text=40.0844,65.3792",
        "verified": True
    },

    # Qashqadaryo & Surxondaryo
    {
        "id": "qash_01",
        "name": "Qarshi Agro Himoya Do'koni",
        "region": "Qashqadaryo viloyati",
        "district": "Qarshi shahri",
        "address": "Islom Karimov ko'chasi, Yerqo'rg'on bozori",
        "landmark": "Yerqo'rg'on ulgurji bozori 2-darvoza",
        "phone": "+998 75 221 05 60",
        "working_hours": "06:30 - 18:00",
        "categories": ["Paxta va g'alla dorilari", "Fungitsidlar", "Insektitsidlar", "Envidor"],
        "lat": 38.8606,
        "lon": 65.7891,
        "map_url": "https://yandex.uz/maps/?text=38.8606,65.7891",
        "verified": True
    },
    {
        "id": "sur_01",
        "name": "Termiz Agro Nur Dorixonasi",
        "region": "Surxondaryo viloyati",
        "district": "Termiz shahri",
        "address": "At-Termiziy ko'chasi, Markaziy bozor",
        "landmark": "Termiz markaziy dehqon bozori",
        "phone": "+998 76 222 34 88",
        "working_hours": "07:00 - 18:30",
        "categories": ["Erta hosil himoyasi", "Fungitsidlar", "Oqqanotga qarshi vositalar"],
        "lat": 37.2242,
        "lon": 67.2783,
        "map_url": "https://yandex.uz/maps/?text=37.2242,67.2783",
        "verified": True
    },
    {
        "id": "sur_02",
        "name": "Denov Agro Servis Markazi",
        "region": "Surxondaryo viloyati",
        "district": "Denov tumani",
        "address": "Sharaf Rashidov ko'chasi, 45",
        "landmark": "Denov katta bozori yonida",
        "phone": "+998 91 585 70 00",
        "working_hours": "07:30 - 18:00",
        "categories": ["Pomidor, karam, piyoz himoyasi", "Fungitsidlar", "Quadris"],
        "lat": 38.2758,
        "lon": 67.8986,
        "map_url": "https://yandex.uz/maps/?text=38.2758,67.8986",
        "verified": True
    },

    # Jizzax & Sirdaryo
    {
        "id": "jiz_01",
        "name": "Jizzax Dehqon Najotkori",
        "region": "Jizzax viloyati",
        "district": "Jizzax shahri",
        "address": "Sharof Rashidov shoh ko'chasi, Ko'k bozor",
        "landmark": "Ko'k bozor sharqiy kirish darvozasi",
        "phone": "+998 72 226 50 10",
        "working_hours": "08:00 - 18:00",
        "categories": ["Fungitsidlar", "Galla dorilari", "Previkur", "Fitosporin"],
        "lat": 40.1158,
        "lon": 67.8422,
        "map_url": "https://yandex.uz/maps/?text=40.1158,67.8422",
        "verified": True
    },
    {
        "id": "sir_01",
        "name": "Guliston Agro Himoya",
        "region": "Sirdaryo viloyati",
        "district": "Guliston shahri",
        "address": "Sayhun ko'chasi, Dehqon bozori hududi",
        "landmark": "Guliston markaziy dehqon bozori",
        "phone": "+998 67 225 12 90",
        "working_hours": "07:30 - 18:00",
        "categories": ["Qovun pashshasiga qarshi", "Fungitsidlar", "Poliz dorilari"],
        "lat": 40.4897,
        "lon": 68.7842,
        "map_url": "https://yandex.uz/maps/?text=40.4897,68.7842",
        "verified": True
    },

    # Xorazm & Qoraqalpog'iston
    {
        "id": "xor_01",
        "name": "Urganch Agro Servis Aptekasi",
        "region": "Xorazm viloyati",
        "district": "Urganch shahri",
        "address": "Al-Xorazmiy ko'chasi, Yangi bozor",
        "landmark": "Yangi bozor qishloq xo'jalik mahsulotlari rastasi",
        "phone": "+998 62 228 45 60",
        "working_hours": "08:00 - 18:00",
        "categories": ["Fungitsidlar", "Sho'r yerlar uchun biostimulyatorlar", "Skor"],
        "lat": 41.5500,
        "lon": 60.6333,
        "map_url": "https://yandex.uz/maps/?text=41.5500,60.6333",
        "verified": True
    },
    {
        "id": "qr_01",
        "name": "Nukus Agro Himoya Markazi",
        "region": "Qoraqalpog'iston Respublikasi",
        "district": "Nukus shahri",
        "address": "A. Dosnazarov ko'chasi, Markaziy bozor",
        "landmark": "Nukus markaziy dehqon bozori",
        "phone": "+998 61 222 71 80",
        "working_hours": "08:00 - 17:30",
        "categories": ["Barcha agro-preparatlar", "Fungitsidlar", "Biogumus"],
        "lat": 42.4602,
        "lon": 59.6166,
        "map_url": "https://yandex.uz/maps/?text=42.4602,59.6166",
        "verified": True
    },
]

# O'simlik kasalliklari va zararkunandalariga qarshi tavsiya etiladigan rasmiy dori vositalari
AGRO_MEDICINES: Dict[str, List[Dict[str, Any]]] = {
    "fitoftoroz": [
        {
            "name": "Ridomil Gold MZ 68 WG",
            "type": "Tizimli va kontakt fungitsid",
            "active_ingredient": "Mankotseb (640 g/kg) + Mefenoksam (40 g/kg)",
            "dosage": "10 litr suvga 25-30 g",
            "instruction": "Ekin barglariga dastlabki kasallik belgilari ko'ringanda yoki profilaktika uchun bir tekisda purkaladi. 10-14 kundan so'ng qayta ishlov beriladi.",
            "price_range": "35,000 - 45,000 so'm (100g)",
            "safety": "Kutilish muddati: 14 kun. Ishlov berishda respirator va qo'lqopdan foydalaning.",
            "urgency": "Zudlik bilan qo'llash tavsiya etiladi"
        },
        {
            "name": "Quadris (Kvadris 250 SC)",
            "type": "Tizimli fungitsid",
            "active_ingredient": "Azoksistrobin (250 g/l)",
            "dosage": "10 litr suvga 6-8 ml",
            "instruction": "Zamburug' sporalarini yo'q qiladi, fotosintezni oshiradi. Ertalab yoki kechki salqinda seping.",
            "price_range": "28,000 - 38,000 so'm (100ml)",
            "safety": "Kutilish muddati: 5 kun. Asalarilar uchun xavfi past.",
            "urgency": "O'rtacha"
        },
        {
            "name": "XOM (Mis xloroksidi)",
            "type": "Himoya kontakt fungitsidi",
            "active_ingredient": "Mis xloroksidi (861 g/kg)",
            "dosage": "10 litr suvga 40 g",
            "instruction": "Barg yuzasida himoya qatlami hosil qilib kasallik kirishiga to'sqinlik qiladi.",
            "price_range": "18,000 - 25,000 so'm (100g)",
            "safety": "Kutilish muddati: 20 kun. Gullash davrida sepilmaydi.",
            "urgency": "Profilaktik"
        }
    ],
    "peronosporoz": [
        {
            "name": "Previkur Enerji (Previcur Energy)",
            "type": "Tizimli fungitsid va o'sish stimulyatori",
            "active_ingredient": "Propamokarb (530 g/l) + Fosetil (310 g/l)",
            "dosage": "10 litr suvga 15-20 ml",
            "instruction": "Ildiz chirishi va soxta un-shudringga qarshi ildiz ostiga quyiladi yoki bargdan purkaladi.",
            "price_range": "45,000 - 60,000 so'm (100ml)",
            "safety": "Kutilish muddati: 3 kun. Ildiz tizimini tez tiklaydi.",
            "urgency": "Yuqori zaruriyat"
        },
        {
            "name": "Infinito 687.5 SC",
            "type": "Ikki komponentli fungitsid",
            "active_ingredient": "Fluopikolid (62.5 g/l) + Propamokarb gidroxlorid (625 g/l)",
            "dosage": "10 litr suvga 12-16 ml",
            "instruction": "Eng kuchli zamburug' shtammlarini ham 24 soat ichida bartaraf etadi.",
            "price_range": "50,000 - 65,000 so'm (100ml)",
            "safety": "Kutilish muddati: 10 kun.",
            "urgency": "Zudlik bilan"
        },
        {
            "name": "Fitosporin-M (Biologik)",
            "type": "Biologik fungitsid",
            "active_ingredient": "Bacillus subtilis shtammi 26D",
            "dosage": "10 litr suvga 2-3 choy qoshiq (pasta ko'rinishida)",
            "instruction": "Ekologik toza davolash. Hosil yig'ish kuni ham qo'llash mumkin.",
            "price_range": "15,000 - 22,000 so'm (200g)",
            "safety": "Inson va tabiat uchun mutlaqo zararsiz.",
            "urgency": "Yengil va profilaktik"
        }
    ],
    "oidium": [
        {
            "name": "Topaz 100 EC",
            "type": "Tizimli maxsus fungitsid",
            "active_ingredient": "Penkonazol (100 g/l)",
            "dosage": "10 litr suvga 2-3 ml",
            "instruction": "Un-shudringning barcha turlariga qarshi eng samarali vosita. 2 soatda o'simlik to'qimalariga so'riladi.",
            "price_range": "20,000 - 30,000 so'm (10ml)",
            "safety": "Kutilish muddati: 20 kun. Yomg'ir yuvib ketmaydi.",
            "urgency": "Zudlik bilan"
        },
        {
            "name": "Tiovit Jet (Oltingugurt)",
            "type": "Kontakt fungitsid va akaritsid",
            "active_ingredient": "Oltingugurt (800 g/kg)",
            "dosage": "10 litr suvga 40-50 g",
            "instruction": "Haqiqiy un-shudring va barg kanalari (o'rgimchakkana)ni bir vaqtda yo'q qiladi.",
            "price_range": "15,000 - 20,000 so'm (100g)",
            "safety": "Harorat 28°C dan yuqori bo'lganda sepmang (kuyish xavfi bor).",
            "urgency": "O'rtacha"
        },
        {
            "name": "Skor 250 EC",
            "type": "Tizimli fungitsid",
            "active_ingredient": "Difenokonazol (250 g/l)",
            "dosage": "10 litr suvga 2 ml",
            "instruction": "Bargdagi oq g'uborni to'xtatadi va mevalarni chirishdan asraydi.",
            "price_range": "25,000 - 35,000 so'm (10ml)",
            "safety": "Kutilish muddati: 15-20 kun.",
            "urgency": "Yuqori"
        }
    ],
    "qotir": [
        {
            "name": "Xorus 75 WG (Chorus)",
            "type": "Tizimli davolovchi fungitsid",
            "active_ingredient": "Siprodinil (750 g/kg)",
            "dosage": "10 litr suvga 3-3.5 g",
            "instruction": "Past haroratlarda (+3°C dan boshlab) ham yuqori samara beruvchi noyob preparat. Kurtak yozilishida va guldan so'ng qo'llanadi.",
            "price_range": "30,000 - 42,000 so'm (10g)",
            "safety": "Kutilish muddati: 21 kun. Asalarilar uchun xavfsiz.",
            "urgency": "Yuqori zaruriyat"
        },
        {
            "name": "Skor 250 EC",
            "type": "Tizimli fungitsid",
            "active_ingredient": "Difenokonazol (250 g/l)",
            "dosage": "10 litr suvga 2 ml",
            "instruction": "Qo'tir va moniliozga qarshi eng ishonchli vositalardan biri.",
            "price_range": "25,000 - 35,000 so'm (10ml)",
            "safety": "Kutilish muddati: 20 kun.",
            "urgency": "O'rtacha"
        },
        {
            "name": "Bordo suyuqligi (1%)",
            "type": "Klassik kontakt preparat",
            "active_ingredient": "Mis kuporosi + so'ndirilgan ohak",
            "dosage": "100 g mis kuporosi + 100 g ohak / 10 litr suv",
            "instruction": "Bahorda va kuzda daraxt shoxlariga purkaladi.",
            "price_range": "12,000 - 18,000 so'm (komplekt)",
            "safety": "Qo'shimcha kimyoviy preparatlar bilan aralashtirilmaydi.",
            "urgency": "Mavsumiy"
        }
    ],
    "zararkunanda": [
        {
            "name": "Aktara 25 WG",
            "type": "Tizimli kuchli insektitsid",
            "active_ingredient": "Tiametoksam (250 g/kg)",
            "dosage": "10 litr suvga 1.5 - 2 g",
            "instruction": "Shira (tlya), oqqanot, trips va kolorado qo'ng'iziga qarshi bir zumda ta'sir qiladi.",
            "price_range": "15,000 - 22,000 so'm (4g)",
            "safety": "Kutilish muddati: 14 kun. Asalarilar uchish vaqtida qo'llash taqiqlanadi.",
            "urgency": "Zudlik bilan"
        },
        {
            "name": "Envidor 240 SC",
            "type": "Akaritsid (Kanalarga qarshi)",
            "active_ingredient": "Spirodiklofen (240 g/l)",
            "dosage": "10 litr suvga 5-6 ml",
            "instruction": "Barcha turdagi o'rgimchakkana va ularning tuxumlariga qarshi 40 kungacha himoya ta'minlaydi.",
            "price_range": "40,000 - 55,000 so'm (50ml)",
            "safety": "Kutilish muddati: 20 kun.",
            "urgency": "Yuqori"
        },
        {
            "name": "Vertimek (Biologik kelib chiqishli)",
            "type": "Insektoakaritsid",
            "active_ingredient": "Abamektin (18 g/l)",
            "dosage": "10 litr suvga 8-10 ml",
            "instruction": "Tuproq bakteriyalaridan olingan tabiiy vosita. Sabzavot va mevalarda 3 kunda parchalanadi.",
            "price_range": "35,000 - 48,000 so'm (50ml)",
            "safety": "Kutilish muddati: 3-5 kun.",
            "urgency": "O'rtacha"
        }
    ],
    "soglom": [
        {
            "name": "Gumus / Biostimulyator",
            "type": "Organik o'g'it va ildiz rivojlantiruvchi",
            "active_ingredient": "Gumin va fulvo kislotalar",
            "dosage": "10 litr suvga 30-40 ml",
            "instruction": "Ko'chatning baquvvat o'sishi va hosildorlikni 25-30% oshirish uchun har 10-15 kunda sug'orish.",
            "price_range": "15,000 - 25,000 so'm (1 litr)",
            "safety": "Zararsiz tabiiy mahsulot.",
            "urgency": "Profilaktik oziqlantirish"
        },
        {
            "name": "NPK 20-20-20 (Mikroelementlar bilan)",
            "type": "Kompleks mineral o'g'it",
            "active_ingredient": "Azot (20%), Fosfor (20%), Kaliy (20%) + Me",
            "dosage": "10 litr suvga 20 g",
            "instruction": "Bargdan yoki tomchilatib beriladi, o'simlikning immunitetini oshiradi.",
            "price_range": "25,000 - 35,000 so'm (1 kg)",
            "safety": "Ko'rsatilgan dozadan oshirmang.",
            "urgency": "Rejali parvarish"
        }
    ]
}


def get_medicines_for_diagnosis(disease_name: str, plant_name: str = "", status: str = "") -> List[Dict[str, Any]]:
    """
    Kasallik nomi, o'simlik va holatiga qarab eng mos agro-dori vositalarini topadi.
    """
    d_lower = (disease_name or "").lower()
    s_lower = (status or "").lower()

    if "sog'lom" in s_lower or "sog'lom" in d_lower or "healthy" in d_lower:
        return AGRO_MEDICINES["soglom"]

    if any(k in d_lower for k in ["fitoftor", "late blight", "qora dog'", "chirish", "qo'ng'ir"]):
        return AGRO_MEDICINES["fitoftoroz"]

    if any(k in d_lower for k in ["peronospor", "soxta un", "downy"]):
        return AGRO_MEDICINES["peronosporoz"]

    if any(k in d_lower for k in ["oidium", "un-shudring", "powdery", "oq g'ubor"]):
        return AGRO_MEDICINES["oidium"]

    if any(k in d_lower for k in ["qo'tir", "scab", "parcha", "parchis"]):
        return AGRO_MEDICINES["qotir"]

    if any(k in d_lower for k in ["zararkunanda", "shira", "kana", "oqqanot", "pest", "aphid", "mite"]):
        return AGRO_MEDICINES["zararkunanda"]

    # Standart holda fitoftoroz va un-shudring kombinatsiyasidagi eng ko'p ishlatiladigan dori vositalari
    return AGRO_MEDICINES["fitoftoroz"][:2] + AGRO_MEDICINES["zararkunanda"][:1]


def get_pharmacies(region: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Viloyat yoki qidiruv so'zi bo'yicha agro-aptekalarni saralab beradi.
    """
    results = AGRO_PHARMACIES

    if region and region.strip() and region.strip().lower() != "barchasi":
        r_norm = region.strip().lower().replace("viloyati", "").replace("shahri", "").replace("respublikasi", "").strip()
        results = [
            p for p in results
            if r_norm in p["region"].lower() or r_norm in p["district"].lower()
        ]

    if search and search.strip():
        q = search.strip().lower()
        results = [
            p for p in results
            if q in p["name"].lower()
            or q in p["region"].lower()
            or q in p["district"].lower()
            or q in p["address"].lower()
            or any(q in c.lower() for c in p["categories"])
        ]

    return results
