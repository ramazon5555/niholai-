#!/usr/bin/env python3
"""
Nihol AI - Buyruqlar satri (CLI) orqali rasmni tekshirish vositasi.
Ishlatish:
    python3 cli.py /yo'l/rasm.jpg
    python3 cli.py /yo'l/rasm.jpg --key "AIzaSy..."
"""

import argparse
import os
import sys
from pathlib import Path
from detector import PlantDiseaseDetector

# ANSI ranglar
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_banner():
    banner = f"""
{GREEN}{BOLD}==================================================================
       🌿 NIHOL AI — O'simlik Kasalliklari Diagnostikasi v2.0
=================================================================={RESET}"""
    print(banner)


def main():
    parser = argparse.ArgumentParser(description="Nihol AI - O'simlik fotosurati diagnostikasi")
    parser.add_argument("image", help="Tahlil qilinadigan rasm faylining yo'li (masalan: leaf.jpg)")
    parser.add_argument("--key", default="", help="Ixtiyoriy Google Gemini API kaliti")
    args = parser.parse_args()

    img_path = Path(args.image)
    if not img_path.exists():
        print(f"{RED}[-] Xatolik: '{img_path}' fayli topilmadi!{RESET}")
        sys.exit(1)

    print_banner()

    api_key = args.key or os.getenv("GEMINI_API_KEY", "")
    if api_key:
        print(f"{CYAN}📡 Rejim: {BOLD}🟢 Jonli Gemini Vision AI (Ekspert agronomik tahlil){RESET}")
    else:
        print(f"{YELLOW}📡 Rejim: {BOLD}🟡 Offline Agro-Andoza Bazasi (API kalitsiz){RESET}")
        print(f"{YELLOW}💡 Maslahat: Jonli AI uchun: export GEMINI_API_KEY='kalit'{RESET}")

    print(f"\n{CYAN}[+] '{img_path.name}' rasmi tahlil qilinmoqda...{RESET}\n")

    detector = PlantDiseaseDetector()
    result = detector.analyze_image(img_path, override_api_key=api_key)

    is_healthy = "sog'lom" in (result.get("status") or "").lower()
    status_color = GREEN if is_healthy else RED
    status_icon = "🟢" if is_healthy else "🔴"

    print(f"{BOLD}🌱 O'simlik turi:{RESET}      {result.get('plant_name', 'Nomaʼlum')}")
    print(f"{BOLD}{status_icon} Holati:{RESET}             {status_color}{BOLD}{result.get('status', 'Nomaʼlum')}{RESET}")
    print(f"{BOLD}🦠 Kasallik / Muammo:{RESET} {YELLOW}{BOLD}{result.get('disease_name', 'Mavjud emas')}{RESET}")
    print(f"{BOLD}📊 Ishonchlilik:{RESET}      {result.get('confidence', 0)}%")
    print(f"{BOLD}⚠️  Xavflilik darajasi:{RESET}{result.get('severity', 'Aniqlanmadi')}")
    print(f"{BOLD}🏷  Tahlil manbasi:{RESET}    {result.get('source', '')}")

    print(f"\n{BOLD}{CYAN}🔍 Alomatlar va Tahlil:{RESET}")
    print(f"   {result.get('symptoms', 'Mavjud emas')}")

    treatments = result.get("treatment", [])
    if treatments:
        print(f"\n{BOLD}{GREEN}💊 Tavsiya etiladigan Davolash Choralari:{RESET}")
        for t in treatments:
            print(f"   {GREEN}✔{RESET} {t}")

    preventions = result.get("prevention", [])
    if preventions:
        print(f"\n{BOLD}{CYAN}🛡  Profilaktika (Oldini Olish):{RESET}")
        for p in preventions:
            print(f"   {CYAN}★{RESET} {p}")

    print(f"\n{GREEN}=================================================================={RESET}\n")


if __name__ == "__main__":
    main()
