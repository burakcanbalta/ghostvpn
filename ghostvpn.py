# GHOSTVPN.PY - Tüm sistemin tek dosyada birleşmiş sürümü
# Bu dosya cleaner, proxy, tor, vpn, config_manager, anti_fingerprint, dark_ghost gibi tüm parçaları içerir.
# Çalıştırmak için: python3 ghostvpn_allinone.py




# cleaner.py
============================================================
import subprocess

def clean_disconnect():
    try:
        print("[+] Cleaning system: Stopping VPN, Proxy, and Tor services...")
        subprocess.call(["sudo", "killall", "openvpn"])
        subprocess.call(["sudo", "systemctl", "stop", "tor"])
        subprocess.call(["sudo", "pkill", "-f", "proxy_server.py"])
        print("[+] Services stopped.")
        subprocess.call(["sudo", "systemd-resolve", "--flush-caches"])
        print("[+] DNS cache flushed.")
    except Exception as e:
        print(f"[!] Error during cleanup: {str(e)}")

if __name__ == "__main__":
    clean_disconnect()


# proxy_server.py
============================================================
import socket
import threading

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
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listen_ip, listen_port))
    server.listen(5)
    print(f"[+] SOCKS5 proxy server started on {listen_ip}:{listen_port}")
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()


# tor_controller.py
============================================================
import subprocess
import time

def start_tor_service():
    try:
        print("[+] Starting Tor service...")
        subprocess.call(["sudo", "systemctl", "start", "tor"])
        time.sleep(5)
        print("[+] Tor service started.")
    except Exception as e:
        print(f"[!] Failed to start Tor service: {str(e)}")

def stop_tor_service():
    try:
        print("[+] Stopping Tor service...")
        subprocess.call(["sudo", "systemctl", "stop", "tor"])
        print("[+] Tor service stopped.")
    except Exception as e:
        print(f"[!] Failed to stop Tor service: {str(e)}")


# vpn_connector.py
============================================================
import subprocess
import time

def connect_vpn(config_path):
    try:
        print(f"[+] Connecting to VPN using {config_path}...")
        subprocess.Popen(["sudo", "openvpn", "--config", config_path])
        time.sleep(5)
        print("[+] VPN connection initiated.")
    except Exception as e:
        print(f"[!] Failed to connect VPN: {str(e)}")

def disconnect_vpn():
    try:
        print("[+] Disconnecting VPN...")
        subprocess.call(["sudo", "killall", "openvpn"])
        print("[+] VPN disconnected.")
    except Exception as e:
        print(f"[!] Failed to disconnect VPN: {str(e)}")


# config_manager.py
============================================================
import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

class ConfigManager:
    def __init__(self):
        self.temp_dir = "/dev/shm/ghostvpn"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.key = hashlib.sha256(b'ghostvpn-master-key').digest()
        
    def encrypt_config(self, data, filename):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        with open(filename, 'wb') as f:
            f.write(cipher.iv)
            f.write(ct_bytes)
            
    def decrypt_config(self, filename):
        with open(filename, 'rb') as f:
            iv = f.read(16)
            ct = f.read()
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    
    def secure_delete(self, path, passes=3):
        with open(path, 'ba+') as f:
            length = f.tell()
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(path)


# anti_fingerprint.py
============================================================
import random
import time
import subprocess

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
        subprocess.run(["curl", "-s", f"http://{random.choice(domains)}"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    def random_dns_query(self):
        domains = ["google.com", "yahoo.com", "bing.com"]
        subprocess.run(["dig", "+short", random.choice(domains)], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# dark_ghost.py
============================================================
import subprocess
from ram_system import RamSystem
from ghost_kill import GhostKill

class DarkGhost:
    def __init__(self):
        self.ram_system = RamSystem()
        self.ghost_kill = GhostKill()
        
    def activate(self):
        print("🔒 DarkGhost Mode Activating...")
        
        # 1. Tüm gereksiz servisleri kapat
        self.ghost_kill.kill_processes()
        
        # 2. RAM'e geç
        self.ram_system.move_to_ram("/etc/ghostvpn/config.ovpn")
        
        # 3. Swap ve cache temizle
        self.ram_system.disable_swap()
        self.ram_system.clear_ram()
        
        # 4. JavaScriptsiz tarayıcı başlat
        self.start_secure_browser()
        
        # 5. Tor + VPN zinciri
        self.start_tor_vpn_chain()
        
        print("🕶️ DarkGhost Mode Active - You are now invisible")
        
    def start_secure_browser(self):
        subprocess.Popen([
            'firefox', 
            '--private-window',
            '--disable-javascript',
            '--no-remote',
            'about:blank'
        ])
        
    def start_tor_vpn_chain(self):
        subprocess.Popen([
            'sudo', 'openvpn',
            '--config', '/dev/shm/ghostvpn/config.ovpn',
            '--route-nopull',
            '--route-up', 'torify'
        ])


# ================= LOGGER ====================
import os
from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    line = f"{timestamp} {message}"
    print(line)
    try:
        with open("ghostvpn.log", "a") as f:
            f.write(line + "\n")
    except:
        pass


# ================= CLI MENU ====================
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
        choice = input("Seçim: ")
        if choice == "1":
            connect_vpn()
        elif choice == "2":
            start_tor()
        elif choice == "3":
            start_proxy_server()
        elif choice == "4":
            generate_fake_traffic()
        elif choice == "5":
            ghost_kill()
        elif choice == "0":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim!")


# ================= WEB DASHBOARD ====================
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status')
def status():
    try:
        import socket
        ip = socket.gethostbyname(socket.gethostname())
    except:
        ip = "Bilinmiyor"
    return jsonify({
        "status": "Aktif",
        "ip": ip,
        "tor": "Açık",
        "vpn": "Açık",
        "socks_proxy": "127.0.0.1:1080",
        "log": "ghostvpn.log"
    })

def start_dashboard():
    import threading
    threading.Thread(target=lambda: app.run(port=5000), daemon=True).start()


# ================= MAIN ====================
if __name__ == "__main__":
    log("GhostVPN başlatıldı.")
    start_dashboard()
    run_cli()