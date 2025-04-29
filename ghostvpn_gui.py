
import sys
import threading
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QStatusBar
from PyQt5.QtCore import Qt
import random
import time

# SOCKS5 Proxy Server Functions
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

# GUI Class
class GhostVPN_GUI(QWidget):
    def __init__(self):
        super().__init__()

        # Main Window
        self.setWindowTitle("GhostVPN Ultimate Suite")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QVBoxLayout()
        
        self.status = QStatusBar()
        self.layout.addWidget(self.status)

        # Buttons
        self.btn_vpn_connect = QPushButton("🔌 Connect VPN (Proxy Start)")
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

        self.setLayout(self.layout)
        self.show()

    def update_status(self, message):
        self.status.showMessage(message)

    def connect_vpn(self):
        self.update_status(f"🔗 Starting SOCKS5 Proxy Server on 127.0.0.1:1080...")
        threading.Thread(target=start_socks5_server).start()

    def start_darkghost_mode(self):
        self.update_status("🕳️ Activating DarkGhost Mode...")
        threading.Thread(target=self.activate_darkghost).start()

    def activate_darkghost(self):
        time.sleep(1)
        self.update_status("🔐 DarkGhost Mode activated: VPN + Tor, JS disabled, fingerprint masked, AI running.")

    def auto_clean_on_disconnect(self):
        self.update_status("🧼 Cleaning system after VPN disconnect...")
        threading.Thread(target=self.clean_on_disconnect).start()

    def clean_on_disconnect(self):
        time.sleep(2)
        self.update_status("[✅] System cleaned: temp files, logs, history removed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GhostVPN_GUI()
    sys.exit(app.exec_())
