# 🌿 NiholAI — Aqlli O'simliklar Diagnostikasi va Fermerlik Platformasi

**NiholAI** — o'simlik turlarini aniqlash, barg fotosurati orqali kasalliklarga aniq tashxis qo'yish, agronomik davolash tavsiyalarini berish hamda O'zbekiston viloyatlari bo'yicha ekinlar hosildorligi va daromadini oldindan hisoblovchi aqlli sun'iy intellekt tizimi.

Loyiha **HCI (Inson-Kompyuter Muloqoti)** fani doirasida qulay va zamonaviy foydalanuvchi interfeysi hamda **Google Gemini Vision AI** va **Offline Agro-Ma'lumotlar Bazasi** bilan boyitilgan.

---

## 🚀 Asosiy Imkoniyatlar

1. **📷 O'simliklarni Aniqlash (Botanik AI):**
   - O'simlik yoki xona guli fotosurati yuklanganda, uning turi, botanik oilasi, sug'orish tartibi, yorug'lik va harorat talablarini bir zumda aniqlaydi.

2. **🩺 Sog'liqni Tekshirish (Kasalliklar Diagnostikasi):**
   - Zararlangan barg yoki ko'chat suratini chuqur tahlil qilib:
     - Sog'lomlik darajasi (Sog'lom / Kasallangan)
     - Kasallik yoki zararkunanda aniq nomi
     - Vizual alomatlar va yuzaga kelish sabablari
     - Amaliy agrotexnik, biologik va kimyoviy davolash choralari (preparatlar va dozalari)
     - Kelgusida ushbu kasallikning oldini olish (profilaktika) choralarini taqdim etadi.

3. **🚜 Fermer Rejimi (Hosil va Daromad Kalkulyatori):**
   - O'zbekistonning barcha 14 ta hududi (viloyatlar, Toshkent shahri va Qoraqalpog'iston Respublikasi) iqlim koeffitsientlariga asoslangan holda ekinlar (Pomidor, Bodring, Kartoshka, Piyoz) bo'yicha past, o'rtacha va yuqori hosil hamda daromadni hisoblaydi.

4. **⚡ Ikki Bosqichli AI Arxitekturasi:**
   - **🟢 Jonli AI Rejimi (Google Gemini Vision):** Har qanday fotosurat bo'yicha 100% real vaqtli chuqur agronomik tahlil.
   - **🟡 Offline Agro-Baza:** Internet yoki API kalit bo'lmagan sharoitda ham O'zbekistonda eng ko'p uchraydigan ekin kasalliklari bo'yicha mustaqil ishlay oladi.

5. **🤖 Telegram Bot va Terminal (CLI):**
   - Dala sharoitida fermerlar to'g'ridan-to'g'ri Telegram orqali barg rasmini yuborib javob olishlari uchun `bot.py` moduli.
   - Dasturchilar va server ma'murlari uchun rangli `cli.py` vositasi.

---

## 📁 Loyiha Tuzilmasi

```text
NiholAI/
├── index.html          # Zamonaviy veb interfeys (Bosh sahifa, Aniqlash, Sog'liq, Fermer)
├── server.py           # FastAPI asosiy veb-serveri (API va HTML yetkazib berish)
├── detector.py         # AI diagnostika yadrosi (Gemini Vision + Offline Agro-Baza)
├── config.py           # Konfiguratsiya va sozlamalar
├── .env                # Muhit o'zgaruvchilari (API kalitlar)
├── bot.py              # Fermerlar uchun Telegram bot integratsiyasi
├── cli.py              # Terminal orqali rasmni tekshirish vositasi
├── requirements.txt    # Kerakli Python kutubxonalari
└── uploads/            # Tahlil qilingan fotosuratlar saqlanadigan papka
```

---

## 🛠 O'rnatish va Ishga Tushirish

### 1. Bog'liqliklarni o'rnatish
```bash
git clone https://github.com/ozodbekqodirovlenova2025-netizen/NiholAI.git
cd NiholAI
pip install -r requirements.txt
```

### 2. Veb-Platformani ishga tushirish
```bash
python3 server.py
# Yoki uvicorn orqali:
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```
Brauzerda oching: **`http://localhost:8000`**

### 3. Terminal orqali sinash
```bash
python3 cli.py leaf_photo.jpg
```

### 4. Telegram botni yoqish
```bash
export TELEGRAM_BOT_TOKEN="sizning_bot_tokeningiz"
python3 bot.py
```

---

## 🔑 Sozlamalar (Gemini API)
Loyiha ichidagi `.env` faylida API kalitingiz avtomatik saqlanadi:
```env
GEMINI_API_KEY="AIzaSy..."
```
Shuningdek, veb-saytning yuqori o'ng burchagidagi **"⚙️ Sozlamalar"** tugmasi orqali brauzerdan turib ham kalitni o'zgartirish mumkin.

---

## 👨‍💻 Muallif
- **Ozodbek Qodirov** ([GitHub](https://github.com/ozodbekqodirovlenova2025-netizen))
