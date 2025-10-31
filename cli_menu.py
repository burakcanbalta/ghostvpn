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
        try:
            choice = input("Seçim yapınız: ")
            
            if choice == "1":
                interface = input("Ağ arayüzü giriniz (örn: eth0, wlan0): ").strip()
                if interface:
                    mac_changer.change_mac(interface, use_realistic=True)
                else:
                    print("Geçersiz ağ arayüzü!")
                    
            elif choice == "2":
                thread = threading.Thread(target=ghost_noise.generate_fake_traffic, daemon=True)
                thread.start()
                print("Fake trafik başlatıldı...")
                
            elif choice == "3":
                thread = threading.Thread(target=ghost_trap.start_honeypot, daemon=True)
                thread.start()
                print("Honeypot başlatıldı...")
                
            elif choice == "4":
                ghost_trap.monitor_for_attackers()
                
            elif choice == "5":
                smartai.check_sandbox_conditions()
                
            elif choice == "6":
                confirm = input("Emin misiniz? (e/h): ").lower()
                if confirm == 'e':
                    ghost_kill.ghost_kill()
                    break
                    
            elif choice == "0":
                print("Çıkılıyor...")
                break
                
            else:
                print("Geçersiz seçim!")
                
        except KeyboardInterrupt:
            print("\nProgram kapatılıyor...")
            break
        except Exception as e:
            print(f"Hata oluştu: {e}")
            
        time.sleep(1)
