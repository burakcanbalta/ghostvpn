import os
import subprocess
import sys
from utils import logger

def ghost_kill():
    logger.log("[!] GhostKill devreye girdi: sistem imha ediliyor...")
    try:
        subprocess.run(["pkill", "openvpn"], check=False)
        logger.log("OpenVPN süreci durduruldu.")
        subprocess.run(["systemctl", "stop", "tor"], check=False)
        logger.log("Tor servisi durduruldu.")
        subprocess.run(["swapoff", "-a"], check=False)
        logger.log("Swap alanı devre dışı bırakıldı.")
        
        script_path = os.path.abspath(__file__)
        if os.path.exists(script_path):
            os.remove(script_path)
            logger.log("GhostKill dosyası kendini sildi.")
    except Exception as e:
        logger.log(f"GhostKill sırasında hata: {e}")
    finally:
        logger.log("Sistem sonlandırılıyor.")
        sys.exit(1)
