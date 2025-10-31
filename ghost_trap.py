import subprocess
import threading
import socket
import time
from utils import logger
from core.ghost_kill import ghost_kill

def monitor_for_attackers():
    try:
        suspicious_processes = ["nmap", "wireshark", "tcpdump"]
        output = subprocess.check_output(["ps", "aux"]).decode()
        for proc in suspicious_processes:
            if proc in output:
                logger.log(f"[!] Şüpheli süreç tespit edildi: {proc}")
                ghost_kill()
    except Exception as e:
        logger.log(f"Trap kontrol hatası: {e}")

def start_honeypot():
    def run_ssh_trap():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("0.0.0.0", 2222))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                logger.log(f"[!] Honeypot bağlantısı: {addr}")
                conn.send(b"Unauthorized access. Connection logged.\n")
                conn.close()
        except Exception as e:
            logger.log(f"Honeypot hatası: {e}")

    thread = threading.Thread(target=run_ssh_trap, daemon=True)
    thread.start()
    logger.log("SSH honeypot port 2222 başlatıldı.")
