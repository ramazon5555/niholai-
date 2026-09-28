#!/usr/bin/env python3
"""
Nihol AI - Telegram Bot integratsiyasi.
Fermerlar va foydalanuvchilar o'simlik bargining rasmini yuborganlarida,
AI uni tahlil qilib, o'zbek tilida to'liq hisobot va davolash tavsiyalarini qaytaradi.
"""

import asyncio
import os
import sys
from pathlib import Path

try:
    from aiogram import Bot, Dispatcher, types, F
    from aiogram.filters import Command
    from aiogram.enums import ParseMode
except ImportError:
    print("[!] 'aiogram' kutubxonasi topilmadi. O'rnatish uchun:")
    print("    pip install aiogram")
    sys.exit(1)

from config import TELEGRAM_BOT_TOKEN, UPLOAD_DIR
from detector import PlantDiseaseDetector

if not TELEGRAM_BOT_TOKEN:
    print("[!] DIQQAT: TELEGRAM_BOT_TOKEN o'rnatilmagan.")
    print("    Eksport qiling: export TELEGRAM_BOT_TOKEN='bot_tokeningiz'")

bot = Bot(token=TELEGRAM_BOT_TOKEN or "DUMMY_TOKEN")
dp = Dispatcher()
detector = PlantDiseaseDetector()

# Har bir foydalanuvchining shaxsiy API kalitini saqlash xotirasi
user_keys: dict[int, str] = {}


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    is_live = bool(user_keys.get(message.from_user.id) or os.getenv("GEMINI_API_KEY"))
    mode_text = "🟢 Jonli Gemini AI Faol" if is_live else "🟡 Offline Agro-Andoza Rejimi"

    await message.answer(
        "🌿 **Assalomu alaykum! Men Nihol AI agro-yordamchisiman.**\n\n"
        f"📡 **Joriy holat:** `{mode_text}`\n\n"
        "Men o'simlik va ko'chatlar (nihollar) holatini fotosurat orqali tahlil qilaman:\n"
        "• Kasallik va zararkunandalarni aniqlash\n"
        "• O'simlikning sog'lomlik darajasi\n"
        "• Agronomik davolash choralari va profilaktika\n\n"
        "💡 *Maslahat:*\n"
        "• Jonli Gemini AI kalitini kiritish uchun: `/key AIzaSy...`\n"
        "• Kalitsiz holatda ham offline andoza bazasi to'liq ishlaydi.\n\n"
        "📸 **Tahlil qilish uchun barg yoki nihol fotosuratini yuboring!**",
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message(Command("key"))
async def key_handler(message: types.Message):
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        await message.answer(
            "🔑 **Gemini API Kalitini sozlash:**\n"
            "Format: `/key AIzaSy...`\n\n"
            "Kalitni o'chirish uchun: `/key clear`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    new_key = parts[1].strip()
    if new_key.lower() == "clear":
        user_keys.pop(message.from_user.id, None)
        await message.answer("🟡 Shaxsiy API kalit o'chirildi. Tizim offline andoza rejimiga o'tdi.")
    else:
        user_keys[message.from_user.id] = new_key
        await message.answer("🟢 **Muvaffaqiyatli saqlandi!** Endi sizning tahlillaringiz 100% Jonli Gemini Vision AI orqali amalga oshiriladi.")


@dp.message(F.photo)
async def photo_handler(message: types.Message):
    wait_msg = await message.answer("⏳ *Rasm qabul qilindi. Nihol AI tahlil o'tkazmoqda...*", parse_mode=ParseMode.MARKDOWN)

    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    save_path = UPLOAD_DIR / f"tg_{photo.file_id}.jpg"

    await bot.download_file(file_info.file_path, save_path)

    # Foydalanuvchi kaliti bormi tekshirish
    custom_key = user_keys.get(message.from_user.id, "")
    res = detector.analyze_image(save_path, override_api_key=custom_key)

    status_icon = "🟢" if "sog'lom" in (res.get("status") or "").lower() else "🔴"
    treatments_text = "\n".join([f"• {t}" for t in res.get("treatment", [])])
    prevention_text = "\n".join([f"• {p}" for p in res.get("prevention", [])])

    response_text = (
        f"🌱 **O'simlik turi:** {res.get('plant_name', 'Aniqlanmadi')}\n"
        f"{status_icon} **Holati:** {res.get('status', 'Nomaʼlum')}\n"
        f"🦠 **Kasallik/Muammo:** {res.get('disease_name', 'Mavjud emas')}\n"
        f"📊 **Ishonchlilik:** {res.get('confidence', 0)}%\n"
        f"⚠️ **Xavflilik:** {res.get('severity', 'Oʻrtacha')}\n"
        f"🏷 **Manba:** {res.get('source', '')}\n\n"
        f"🔍 **Alomatlar:**\n{res.get('symptoms', 'Keltirilmadi')}\n\n"
        f"💊 **Davolash choralari:**\n{treatments_text}\n\n"
        f"🛡 **Profilaktika:**\n{prevention_text}"
    )

    await wait_msg.delete()
    await message.answer(response_text, parse_mode=ParseMode.MARKDOWN)


async def main():
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "DUMMY_TOKEN":
        print("[-] Xatolik: TELEGRAM_BOT_TOKEN ko'rsatilmagan. Bot ishga tushmadi.")
        return
    print("[+] Nihol AI Telegram boti ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
