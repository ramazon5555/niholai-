# 📱 NiholAI — Mobil Ilova Bo'yicha To'liq Qo'llanma

**NiholAI** to'liq mobil ilova darajasiga ko'tarildi! Ushbu hujjat orqali platformani telefoningizda qanday o'rnatish, Telegram bot orqali tarqatish va mustaqil Android `.apk` fayliga aylantirishni o'rganasiz.

---

## 🌟 Mobil Ilovadagi Yangi Imkoniyatlar

1. **📱 Native-Feel Mobil Interfeys:**
   - Ekranning pastki qismida qulay navigatsiya paneli (**Bottom Navigation Bar**):
     - 🏠 **Asosiy:** Dashboard, tezkor harakatlar va mavsumiy agronom maslahatlari.
     - 🩺 **Tashxis:** Kasalliklarni tahlil qilish va dori vositalarini topish.
     - 🏪 **Aptekalar:** O'zbekiston viloyatlari bo'yicha agro-aptekalar va o'simliklarni himoya qilish markazlari.
     - 🔍 **Botanik:** Suratdan o'simlik turini aniqlash.
     - 🚜 **Fermer:** 14 ta hudud bo'yicha hosildorlik va daromad kalkulyatori.
     - 📜 **Tarix:** Oflayn xotirada saqlanadigan tahlillar arxivi.

2. **📸 Jonli Kamera Skaneri (Live Viewfinder):**
   - HTML5 Kamera API orqali to'g'ridan-to'g'ri telefon kamerasini bargga qaratib, skanerlash ramkasi va yashil lazer nuri orqali bitta tugmada suratga olish.
   - Old/orqa kamerani almashtirish (🔄) yoki galereyadan yuklash imkoniyati.

3. **💊 Dori Vositalari (Preparatlar) Tavsiyasi:**
   - Har bir aniqlangan kasallik uchun rasmiy fungitsidlar, insektitsidlar yoki biopreparatlar:
     - Preparat nomi (masalan: *Ridomil Gold MZ*, *Topaz*, *Quadris*, *Previkur Energy*, *Skor*, *Aktara*).
     - Dozasi (10 litr suvga qancha qo'shish kerakligi).
     - Qo'llash vaqti va yo'riqnomasi.
     - O'rtacha bozor narxi va xavfsizlik qoidalari (kutilish muddati).

4. **🏪 O'zbekiston Viloyatlari Bo'yicha Agro-Aptekalar:**
   - 14 ta hudud (Toshkent, Samarqand, Farg'ona, Andijon, Namangan, Buxoro, Qashqadaryo, Surxondaryo, Xorazm, Jizzax, Sirdaryo, Navoiy, Qoraqalpog'iston).
   - Aniq manzil va mo'ljal.
   - **Bir marta bosish bilan qo'ng'iroq qilish** (`📞 Qo'ng'iroq qilish`).
   - **Yandex / Google Xaritada lokatsiyani ochish** (`🗺️ Xaritada ko'rish`).

5. **🎙️ Ovozli Agronom (Audio Xulosa):**
   - Dala sharoitida fermer qo'llari band bo'lganda natijani o'qib beruvchi audio sintezator.
   - Bitta tugma orqali tashxis, xavf darajasi va birinchi chorani ovozli eshitish.

6. **📜 Oflayn Xotira va Tarix (Offline History):**
   - Barcha tahlillar avtomatik ravishda qurilmaning `localStorage` xotirasida saqlanadi.
   - Internet yo'q bo'lganda ham o'tgan haftadagi yoki eski tekshiruvlarni ochib ko'rish mumkin.

---

## 🚀 1-BOSQICH: PWA Sifatida Telefonga O'rnatish

NiholAI zamonaviy **Progressive Web App (PWA)** standartida qurilgan. Google Play yoki App Store siz ham har qanday telefonga ilova qilib o'rnatiladi:

### Android (Chrome orqali):
1. Serverni ishga tushiring:
   ```bash
   python3 server.py
   ```
2. Telefoningiz brauzerida saytni oching (masalan, mahalliy tarmoqda: `http://192.168.1.X:8000` yoki internetdagi domeningiz).
3. Ekranning yuqori qismida paydo bo'ladigan **"📲 NiholAI ilovasini o'rnating"** tugmasini bosing yoki Chrome menyusidan (**⋮**) **"Ilovani o'rnatish" (Install app / Добавить на главный экран)** ni tanlang.
4. Telefoningiz ish stolida NiholAI logotipi paydo bo'ladi va u to'liq mustaqil mobil ilova kabi ishlaydi.

### iOS / iPhone (Safari orqali):
1. Safari orqali saytga kiring.
2. Pastki paneldagi **"Ulashish" (Share - kvadrat ichida yuqoriga strelka)** belgisini bosing.
3. Ro'yxatdan **"Bosh ekranga qo'shish" (Add to Home Screen)** bandini tanlang.

---

## 🤖 2-BOSQICH: Telegram Mini App (TMA) Integratsiyasi

O'zbekistondagi fermerlarning 99% Telegram dan foydalanishini hisobga olsak, bu eng ommabop tarqatish yo'lidir.

1. Serveringizga tashqi havola bering (masalan, `ngrok http 8000` yoki o'z VPS domeningiz: `https://niholai.uz`).
2. `.env` faylida o'zgaruvchini belgilang:
   ```env
   WEBAPP_URL="https://sizning-domen.uz"
   TELEGRAM_BOT_TOKEN="sizning_bot_tokeningiz"
   ```
3. [@BotFather](https://t.me/botfather) orqali Menyuga Mini App qo'shish:
   - `/mybots` &rarr; Botingizni tanlang.
   - **Bot Settings** &rarr; **Menu Button** &rarr; **Configure menu button**.
   - Tugma matnini kiriting: `🌱 NiholAI Mobil Ilovasi`.
   - Havolani kiriting: `https://sizning-domen.uz`.
4. Endi foydalanuvchilar botga kirganda chap pastki burchakdagi tugmani bosishlari bilan Telegram ichida to'liq mobil ilova ochiladi!

---

## 📦 3-BOSQICH: Android APK Paketini Yig'ish (Capacitor)

Agar siz loyihani mustaqil `.apk` fayliga aylantirmoqchi bo'lsangiz:

1. Avval loyihaning `www` katalogini tayyorlang:
   ```bash
   ./build_apk.sh
   ```
2. Node.js va npm mavjud bo'lganda:
   ```bash
   npm install @capacitor/core @capacitor/cli @capacitor/android --save-dev
   npx cap add android
   npx cap sync android
   ```
3. Android Studio da ochish yoki Gradle orqali yig'ish:
   ```bash
   cd android
   ./gradlew assembleDebug
   ```
   Tayyor APK fayl manzili:
   `android/app/build/outputs/apk/debug/app-debug.apk`

---

## 🧪 4-BOSQICH: Tezkor Sinash

Loyiha serverini yoqish:
```bash
python3 server.py
```
Brauzerda oching:
`http://localhost:8000`
