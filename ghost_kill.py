# core/ghost_kill.py

import os
import subprocess
from utils import logger

def ghost_kill():
    logger.log("[!] GhostKill devreye girdi: sistem imha ediliyor...")
    try:
        subprocess.call(["pkill", "openvpn"])
        logger.log("OpenVPN süreci durduruldu.")
        subprocess.call(["systemctl", "stop", "tor"])
        logger.log("Tor servisi durduruldu.")
        subprocess.call(["swapoff", "-a"])
        logger.log("Swap alanı devre dışı bırakıldı.")
        script_path = os.path.abspath(__file__)
        if os.path.exists(script_path):
            os.remove(script_path)
            logger.log("GhostKill dosyası kendini sildi.")
    except Exception as e:
        logger.log(f"GhostKill sırasında hata: {e}")
    finally:
        logger.log("Sistem sonlandırılıyor.")
        os._exit(1)