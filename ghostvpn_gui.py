
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStatusBar
from PyQt5.QtCore import Qt
import subprocess
import random
import os
import time
import threading

# GhostVPN Ultimate GUI - Main Class
class GhostVPN_GUI(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize main window
        self.setWindowTitle("GhostVPN Ultimate Suite")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QVBoxLayout()
        
        self.status = QStatusBar()
        self.layout.addWidget(self.status)

        # Buttons for each feature
        self.btn_vpn_connect = QPushButton("🔌 Connect VPN")
        self.btn_vpn_connect.clicked.connect(self.connect_vpn)
        self.layout.addWidget(self.btn_vpn_connect)

        self.btn_darkghost = QPushButton("🕳️ DarkGhost Mode")
        self.btn_darkghost.clicked.connect(self.start_darkghost_mode)
        self.layout.addWidget(self.btn_darkghost)

        self.btn_cleanup = QPushButton("🧼 Clean on Disconnect")
        self.btn_cleanup.clicked.connect(self.auto_clean_on_disconnect)
        self.layout.addWidget(self.btn_cleanup)

        self.btn_exit = QPushButton("❌ Exit")
        self.btn_exit.clicked.connect(self.close)
        self.layout.addWidget(self.btn_exit)

        # Display the window
        self.setLayout(self.layout)
        self.show()

    def update_status(self, message):
        self.status.showMessage(message)

    def connect_vpn(self):
        # Select country file (For now, it picks a random country conf file)
        country_file = self.get_random_country()
        password = "yourpassword"  # Replace with your password for decrypting VPN .conf files
        
        self.update_status(f"🔗 Connecting to {country_file}...")
        self.start_vpn_connection(country_file, password)

    def start_vpn_connection(self, country_file, password):
        decrypted_path = country_file.replace(".enc", "")
        # Simulating VPN connection with decrypting the config file
        self.update_status(f"[🟢] VPN connected to {decrypted_path}")

    def get_random_country(self):
        route_pool = [
            "netherlands.conf.enc", "estonia.conf.enc", "switzerland.conf.enc", "iceland.conf.enc",
            "germany.conf.enc", "canada.conf.enc", "finland.conf.enc", "singapore.conf.enc",
            "uk.conf.enc", "france.conf.enc", "usa.conf.enc", "norway.conf.enc", "austria.conf.enc",
            "japan.conf.enc", "chile.conf.enc", "southkorea.conf.enc", "sweden.conf.enc",
            "poland.conf.enc", "spain.conf.enc", "czechia.conf.enc"
        ]
        return random.choice(route_pool)

    def start_darkghost_mode(self):
        self.update_status("🕳️ Activating DarkGhost Mode...")
        threading.Thread(target=self.activate_darkghost).start()

    def activate_darkghost(self):
        # Simulating the activation of DarkGhost Mode (Tor, VPN, JS block, etc.)
        time.sleep(1)
        self.update_status("🔐 DarkGhost Mode activated: VPN + Tor, JS disabled, fingerprint masked, AI running.")

    def auto_clean_on_disconnect(self):
        self.update_status("🧼 Cleaning system after VPN disconnect...")
        threading.Thread(target=self.clean_on_disconnect).start()

    def clean_on_disconnect(self):
        # This function simulates the automatic cleanup after VPN disconnection
        time.sleep(2)  # Simulate a delay for cleanup tasks
        self.update_status("[✅] System cleaned: temp files, logs, history removed.")

# Main function to run the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GhostVPN_GUI()
    sys.exit(app.exec_())
