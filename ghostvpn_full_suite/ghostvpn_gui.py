import sys
import threading
import random
import subprocess
import time
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStatusBar
from PyQt5.QtCore import Qt

# İçerideki modüller
import os

# MAC changer fonksiyonları
from proxy_server import start_socks5_server, get_current_mac, generate_random_mac, change_mac, restore_mac
from proxy_server import connect_vpn, disconnect_vpn, start_tor_service, stop_tor_service, clean_disconnect

class GhostVPN_GUI(QWidget):
    def __init__(self):
        super().__init__()

        # Ana Pencere
        self.setWindowTitle("GhostVPN Ultimate Suite")
        self.setGeometry(200, 200, 600, 400)
        
        self.layout = QVBoxLayout()
        
        self.status = QStatusBar()
        self.layout.addWidget(self.status)

        # Butonlar
        self.btn_start = QPushButton("🚀 Start GhostVPN")
        self.btn_start.clicked.connect(self.start_ghostvpn)
        self.layout.addWidget(self.btn_start)

        self.btn_clean = QPushButton("🧹 Clean Disconnect")
        self.btn_clean.clicked.connect(self.clean_disconnect)
        self.layout.addWidget(self.btn_clean)

        self.btn_exit = QPushButton("❌ Exit")
        self.btn_exit.clicked.connect(self.close)
        self.layout.addWidget(self.btn_exit)

        # IP ve MAC bilgisi
        self.label_ip = QLabel("Current IP: Unknown")
        self.layout.addWidget(self.label_ip)

        self.label_mac = QLabel("Current MAC: Unknown")
        self.layout.addWidget(self.label_mac)

        self.setLayout(self.layout)
        self.show()

        # Varsayılan bilgiler
        self.interface = "eth0"  # veya "wlan0"
        self.original_mac = None

    def update_status(self, message):
        self.status.showMessage(message)

    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Unknown"

    def update_labels(self):
        ip = self.get_ip()
        mac = get_current_mac(self.interface)
        self.label_ip.setText(f"Current IP: {ip}")
        self.label_mac.setText(f"Current MAC: {mac}")

    def start_ghostvpn(self):
        self.update_status("🚀 Starting GhostVPN...")
        threading.Thread(target=self.start_all_services).start()

    def start_all_services(self):
        try:
            # 1. MAC değiştir
            self.original_mac = get_current_mac(self.interface)
            new_mac = generate_random_mac()
            change_mac(self.interface, new_mac)
            time.sleep(1)

            # 2. Proxy Server başlat
            threading.Thread(target=start_socks5_server, daemon=True).start()
            time.sleep(2)

            # 3. Tor başlat
            start_tor_service()

            # 4. VPN başlat (burada configs klasöründen rastgele seçebilirsin)
            # Örnek olarak hardcoded bir config kullandım:
            vpn_config = "/etc/openvpn/client.ovpn"  # Değiştirmek istersen
            threading.Thread(target=connect_vpn, args=(vpn_config,), daemon=True).start()

            time.sleep(5)

            self.update_labels()
            self.update_status("[🟢] GhostVPN Started Successfully!")

        except Exception as e:
            self.update_status(f"[❗] Error starting GhostVPN: {str(e)}")

    def clean_disconnect(self):
        self.update_status("🧹 Cleaning and Disconnecting...")
        threading.Thread(target=self.clean_all_services).start()

    def clean_all_services(self):
        try:
            # VPN + Tor + Proxy + Temizlik
            clean_disconnect()
            # MAC geri yükle
            if self.original_mac:
                restore_mac(self.interface, self.original_mac)
            time.sleep(3)

            self.update_labels()
            self.update_status("[✅] Cleaned and Disconnected.")
        except Exception as e:
            self.update_status(f"[❗] Error cleaning: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GhostVPN_GUI()
    sys.exit(app.exec_())
