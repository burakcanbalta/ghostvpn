# core/ram_system.py

import os
import subprocess
from utils import logger

def activate_ram_only_mode():
    logger.log("RAM-only mod başlatılıyor...")
    try:
        subprocess.call(["swapoff", "-a"])
        temp_dirs = ["/tmp", "/var/tmp", "/dev/shm"]
        for temp in temp_dirs:
            if os.path.exists(temp):
                for item in os.listdir(temp):
                    full_path = os.path.join(temp, item)
                    try:
                        if os.path.isfile(full_path):
                            os.remove(full_path)
                        elif os.path.isdir(full_path):
                            subprocess.call(["rm", "-rf", full_path])
                    except Exception as e:
                        logger.log(f"{full_path} temizlenemedi: {e}")
        logger.log("Geçici dizinler temizlendi.")
    except Exception as e:
        logger.log(f"RAM-only mod hatası: {e}")