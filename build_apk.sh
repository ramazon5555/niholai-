#!/usr/bin/env bash
# ==============================================================================
# NiholAI — Android APK Yig'ish Skripti (Capacitor orqali)
# ==============================================================================

set -e

echo "🌿 NiholAI Mobil APK yig'ish jarayoni boshlanmoqda..."

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# 1. www katalogini tayyorlash
echo "[1/4] 'www' katalogini yaratish va web aktivlarini nusxalash..."
rm -rf www
mkdir -p www/static

cp index.html www/
cp -r static/* www/static/
cp static/manifest.json www/manifest.json
cp static/sw.js www/sw.js

echo "✅ 'www' katalogi muvaffaqiyatli tayyorlandi."

# 2. Node va npm tekshiruvi
echo "[2/4] Capacitor muhitini tekshirish..."
if ! command -v npm &> /dev/null; then
    echo "⚠️  DIQQAT: Tizimingizda 'npm' topilmadi."
    echo "   npm o'rnatish uchun: sudo apt update && sudo apt install -y nodejs npm"
    echo "   So'ngra quyidagi buyruqlarni bajaring:"
    echo "   1. npm install @capacitor/core @capacitor/cli @capacitor/android"
    echo "   2. npx cap init NiholAI uz.niholai.app --web-dir www"
    echo "   3. npx cap add android"
    echo "   4. npx cap sync android"
    echo "   5. cd android && ./gradlew assembleDebug"
    echo ""
    echo "👉 Natijada 'android/app/build/outputs/apk/debug/app-debug.apk' tayyor bo'ladi!"
    exit 0
fi

# 3. Agar npm mavjud bo'lsa
echo "[3/4] Bog'liqliklarni o'rnatish..."
npm install @capacitor/core @capacitor/cli @capacitor/android --save-dev

# 4. Android platformasini sinxronlash
echo "[4/4] Android platformasini yaratish/yangilash..."
if [ ! -d "android" ]; then
    npx cap add android
fi

npx cap sync android

echo "🎉 Android loyihasi tayyor!"
echo "APK qurish uchun:"
echo "   cd android && ./gradlew assembleDebug"
echo "Yoki Android Studio da ochish uchun:"
echo "   npx cap open android"
