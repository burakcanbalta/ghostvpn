# cli_menu.py

from utils import logger
from core import mac_changer, ghost_kill, ghost_noise, ghost_trap, smartai
import threading
import time

def run_cli():
    while True:
        print("""
===============================
      👻 GhostVPN Panel
===============================
[1] MAC Adresi Değiştir
[2] Fake Trafik Başlat
[3] Honeypot Başlat
[4] Şüpheli Süreçleri Tara
[5] SmartAI Analiz
[6] Kendini İmha Et (GhostKill)
[0] Çıkış
===============================
""")
        choice = input("Seçim yapınız: ")
        if choice == "1":
            mac_changer.change_mac("eth0", use_realistic=True)
        elif choice == "2":
            threading.Thread(target=ghost_noise.generate_fake_traffic, daemon=True).start()
        elif choice == "3":
            ghost_trap.start_honeypot()
        elif choice == "4":
            ghost_trap.monitor_for_attackers()
        elif choice == "5":
            smartai.check_sandbox_conditions()
        elif choice == "6":
            ghost_kill.ghost_kill()
        elif choice == "0":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")
        time.sleep(1)