import os
import subprocess
import socket
import threading
import time
import random
import json
import platform
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {message}"
    print(line)
    try:
        with open("ghostvpn.log", "a") as f:
            f.write(line + "\n")
    except:
        pass

def clean_disconnect():
    try:
        print("[+] Cleaning system: Stopping VPN, Proxy, and Tor services...")
        subprocess.run(["pkill", "openvpn"], check=False)
        subprocess.run(["systemctl", "stop", "tor"], check=False)
        subprocess.run(["pkill", "-f", "proxy_server.py"], check=False)
        print("[+] Services stopped.")
        
        if platform.system().lower() == "linux":
            try:
                subprocess.run(["systemd-resolve", "--flush-caches"], check=False)
            except:
                subprocess.run(["resolvectl", "flush-caches"], check=False)
        elif platform.system().lower() == "windows":
            subprocess.run(["ipconfig", "/flushdns"], check=False, shell=True)
            
        print("[+] DNS cache flushed.")
    except Exception as e:
        print(f"[!] Error during cleanup: {str(e)}")

def handle_client(client_socket):
    try:
        client_socket.recv(262)
        client_socket.send(b"\x05\x00")
        req = client_socket.recv(4)
        mode = req[1]
        addrtype = req[3]

        if addrtype == 1:
            address = socket.inet_ntoa(client_socket.recv(4))
        elif addrtype == 3:
            domain_length = client_socket.recv(1)[0]
            address = client_socket.recv(domain_length).decode()
        port = int.from_bytes(client_socket.recv(2), 'big')

        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((address, port))
        client_socket.send(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + b"\x00\x00")

        threading.Thread(target=forward, args=(client_socket, remote)).start()
        threading.Thread(target=forward, args=(remote, client_socket)).start()

    except Exception as e:
        client_socket.close()

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.send(data)
    except:
        source.close()
        destination.close()

def start_socks5_server(listen_ip='127.0.0.1', listen_port=1080):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((listen_ip, listen_port))
        server.listen(5)
        print(f"[+] SOCKS5 proxy server started on {listen_ip}:{listen_port}")
        while True:
            client_socket, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except Exception as e:
        print(f"Proxy server error: {e}")

def start_tor_service():
    try:
        print("[+] Starting Tor service...")
        subprocess.run(["systemctl", "start", "tor"], check=False)
        time.sleep(5)
        print("[+] Tor service started.")
    except Exception as e:
        print(f"[!] Failed to start Tor service: {str(e)}")

def stop_tor_service():
    try:
        print("[+] Stopping Tor service...")
        subprocess.run(["systemctl", "stop", "tor"], check=False)
        print("[+] Tor service stopped.")
    except Exception as e:
        print(f"[!] Failed to stop Tor service: {str(e)}")

def connect_vpn(config_path):
    try:
        print(f"[+] Connecting to VPN using {config_path}...")
        if os.path.exists(config_path):
            subprocess.Popen(["openvpn", "--config", config_path])
            time.sleep(5)
            print("[+] VPN connection initiated.")
        else:
            print(f"[!] VPN config file not found: {config_path}")
    except Exception as e:
        print(f"[!] Failed to connect VPN: {str(e)}")

def disconnect_vpn():
    try:
        print("[+] Disconnecting VPN...")
        subprocess.run(["pkill", "openvpn"], check=False)
        print("[+] VPN disconnected.")
    except Exception as e:
        print(f"[!] Failed to disconnect VPN: {str(e)}")

class ConfigManager:
    def __init__(self):
        self.temp_dir = "/dev/shm/ghostvpn"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.key = hashlib.sha256(b'ghostvpn-master-key').digest()
        
    def encrypt_config(self, data, filename):
        try:
            cipher = AES.new(self.key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
            with open(filename, 'wb') as f:
                f.write(cipher.iv)
                f.write(ct_bytes)
            return True
        except Exception as e:
            print(f"Encryption error: {e}")
            return False
            
    def decrypt_config(self, filename):
        try:
            with open(filename, 'rb') as f:
                iv = f.read(16)
                ct = f.read()
            cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)
            return pt.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
    
    def secure_delete(self, path, passes=3):
        try:
            if not os.path.exists(path):
                return
            with open(path, 'rb+') as f:
                length = os.path.getsize(path)
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(length))
                    f.flush()
                    os.fsync(f.fileno())
            os.remove(path)
        except Exception as e:
            print(f"Secure delete error: {e}")
            try:
                os.remove(path)
            except:
                pass

class AntiFingerprint:
    def __init__(self):
        self.behavior_profiles = [
            {"name": "casual", "delay": (1, 3), "actions": 5},
            {"name": "researcher", "delay": (3, 7), "actions": 10},
            {"name": "developer", "delay": (0.5, 2), "actions": 15}
        ]
        self.current_profile = None
        
    def randomize_profile(self):
        self.current_profile = random.choice(self.behavior_profiles)
        
    def generate_noise(self):
        actions = [
            self.random_http_request,
            self.random_dns_query,
            self.random_delay,
            self.random_mouse_movement,
            self.random_key_press
        ]
        
        for _ in range(self.current_profile["actions"]):
            action = random.choice(actions)
            action()
            time.sleep(random.uniform(*self.current_profile["delay"]))
            
    def random_http_request(self):
        domains = ["example.com", "test.org", "dummy.net"]
        try:
            subprocess.run(["curl", "-s", f"http://{random.choice(domains)}"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except:
            pass
        
    def random_dns_query(self):
        domains = ["google.com", "yahoo.com", "bing.com"]
        try:
            if platform.system().lower() == "windows":
                subprocess.run(["nslookup", random.choice(domains)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False, shell=True)
            else:
                subprocess.run(["dig", "+short", random.choice(domains)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except:
            pass
    
    def random_delay(self):
        pass
        
    def random_mouse_movement(self):
        try:
            if platform.system().lower() == "windows":
                import pyautogui
                pyautogui.moveRel(random.randint(-10, 10), random.randint(-10, 10))
            else:
                subprocess.run(["xdotool", "mousemove_relative", "--", 
                               str(random.randint(-10, 10)), str(random.randint(-10, 10))],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except:
            pass
        
    def random_key_press(self):
        try:
            if platform.system().lower() == "windows":
                import pyautogui
                pyautogui.press('shift')
            else:
                subprocess.run(["xdotool", "key", "Shift_L"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except:
            pass

def ghost_kill():
    log("[!] GhostKill devreye girdi: sistem imha ediliyor...")
    try:
        subprocess.run(["pkill", "openvpn"], check=False)
        log("OpenVPN süreci durduruldu.")
        subprocess.run(["systemctl", "stop", "tor"], check=False)
        log("Tor servisi durduruldu.")
        subprocess.run(["swapoff", "-a"], check=False)
        log("Swap alanı devre dışı bırakıldı.")
        
        script_path = os.path.abspath(__file__)
        if os.path.exists(script_path):
            os.remove(script_path)
            log("GhostKill dosyası kendini sildi.")
    except Exception as e:
        log(f"GhostKill sırasında hata: {e}")
    finally:
        log("Sistem sonlandırılıyor.")
        os._exit(1)

def generate_fake_traffic():
    targets = ["1.1.1.1", "google.com", "yahoo.com"]
    try:
        while True:
            target = random.choice(targets)
            if platform.system().lower() == "windows":
                subprocess.run(["ping", "-n", "1", target], capture_output=True, check=False)
            else:
                subprocess.run(["ping", "-c", "1", target], capture_output=True, check=False)
            log(f"Fake trafik gönderildi: ping {target}")
            time.sleep(random.randint(5, 15))
    except Exception as e:
        log(f"Fake trafik üretimi hatası: {e}")

def run_cli():
    while True:
        print("""
===============================
      👻 GhostVPN Panel
===============================
[1] VPN Başlat
[2] Tor Başlat
[3] SOCKS Proxy Başlat
[4] AI Sahte Trafik
[5] İmha Et (GhostKill)
[0] Çıkış
===============================
""")
        try:
            choice = input("Seçim: ")
            if choice == "1":
                config_path = input("VPN config dosya yolu: ").strip()
                if config_path and os.path.exists(config_path):
                    connect_vpn(config_path)
                else:
                    print("Geçersiz config dosyası!")
            elif choice == "2":
                start_tor_service()
            elif choice == "3":
                threading.Thread(target=start_socks5_server, daemon=True).start()
                print("SOCKS5 proxy başlatıldı...")
            elif choice == "4":
                threading.Thread(target=generate_fake_traffic, daemon=True).start()
                print("AI sahte trafik başlatıldı...")
            elif choice == "5":
                confirm = input("Emin misiniz? (e/h): ").lower()
                if confirm == 'e':
                    ghost_kill()
            elif choice == "0":
                print("Çıkılıyor...")
                break
            else:
                print("Geçersiz seçim!")
        except KeyboardInterrupt:
            print("\nProgram kapatılıyor...")
            break
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    log("GhostVPN başlatıldı.")
    run_cli()
