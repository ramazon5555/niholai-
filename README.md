# 🌿 NiholAI — Aqlli O'simliklar Diagnostikasi va Fermerlik Platformasi

**NiholAI** — o'simlik turlarini aniqlash, barg fotosurati orqali kasalliklarga aniq tashxis qo'yish, agronomik davolash tavsiyalarini berish hamda O'zbekiston viloyatlari bo'yicha ekinlar hosildorligi va daromadini oldindan hisoblovchi aqlli sun'iy intellekt tizimi.

Loyiha **HCI (Inson-Kompyuter Muloqoti)** fani doirasida qulay va zamonaviy foydalanuvchi interfeysi hamda **Google Gemini Vision AI** va **Offline Agro-Ma'lumotlar Bazasi** bilan boyitilgan.

---

## 🚀 Asosiy Imkoniyatlar

1. **📱 Mobil Ilova (PWA & Telegram Mini App):**
   - Mobil qurilmalarga 100% moslashgan interfeys, pastki boshqaruv paneli (Bottom Navigation Bar), oflayn rejim va to'g'ridan-to'g'ri telefonga o'rnatish imkoniyati.
   - Telegram bot ichida to'liq ochiluvchi zamonaviy Telegram Mini App (TMA).

2. **📸 Jonli Kamera Skaneri (Real-time Viewfinder):**
   - Telefon kamerasidan to'g'ridan-to'g'ri barg va ko'chatlarni skanerlash, lazerli skaner animatsiyasi va tezkor suratga olish.

3. **💊 Dori Vositalari (Preparatlar) Tavsiyasi:**
   - Aniqlangan har bir kasallik uchun amaliy fungitsidlar, insektitsidlar, faol moddasi, 10 litr suvga dozasi, ishlatish muddati va taxminiy bozor narxlari.

4. **🏪 O'zbekiston Bo'yicha Agro-Aptekalar Bazasi:**
   - 14 ta hudud bo'yicha agro-aptekalar va o'simliklarni himoya qilish markazlari manzili, telefon raqamlari (bitta bosish bilan qo'ng'iroq) va xaritalardagi lokatsiyasi.

5. **🎙️ Ovozli Agronom (Audio Xulosa):**
   - Daladagi fermerlar uchun tashxis, sabab va davolash choralarini o'zbek tilida ovoz chiqarib o'qib berish.

6. **📜 Tahlillar Tarixi (Oflayn Xotira):**
   - O'tkazilgan barcha tekshiruvlar avtomatik saqlanib boradi va internet bo'lmaganda ham qayta ko'rish mumkin.

7. **🚜 Fermer Kalkulyatori:**
   - O'zbekiston viloyatlari iqlim koeffitsientlariga asoslangan holda ekinlar (Pomidor, Bodring, Kartoshka, Piyoz) bo'yicha hosil va daromad hisob-kitobi.

8. **⚡ Universal Jonli Gemini AI (Barcha foydalanuvchilar uchun):**
   - Ilovada Master API kaliti va gibrid bulut arxitekturasi o'rnatilgan. NiholAI ilovasini boshqa odamlar (do'stlaringiz, mijozlar, testerlar) o'z telefonlarida yoki kompyuterlarida ochganlarida ham sizning API kalitingiz orqali **100% online rejimda** (`🟢 Jonli AI`) ishlaydi.
   - Hech kim qo'shimcha server o'rnatishi yoki API kalit kiritishi shart emas — barchaga bir xil eng yuqori sifatli jonli tahlil taqdim etiladi.

---

## 📁 Loyiha Tuzilmasi

```text
NiholAI/
├── index.html          # Mobil PWA interfeysi (Bottom Nav, Kamera, Aptekalar, Audio)
├── server.py           # FastAPI serveri (PWA, API, Dori vositalari va Aptekalar)
├── detector.py         # AI diagnostika yadrosi (Gemini Vision + Offline Agro-Baza)
├── pharmacies.py       # O'zbekiston agro-aptekalari va dori vositalari bazasi
├── config.py           # Konfiguratsiya va sozlamalar
├── .env                # Muhit o'zgaruvchilari (API kalitlar)
├── bot.py              # Telegram Bot va Mini App integratsiyasi
├── cli.py              # Terminal orqali rasmni tekshirish vositasi
├── build_apk.sh        # Android APK yig'ish skripti (Capacitor)
├── capacitor.config.json # Capacitor sozlamalari
├── MOBILE_GUIDE.md     # Mobil ilova bo'yicha to'liq qo'llanma
├── requirements.txt    # Kerakli Python kutubxonalari
├── static/             # PWA aktivlari (manifest.json, sw.js, ikonkalar)
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
