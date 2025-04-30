# core/mac_changer.py

import random
import subprocess
from utils import logger

def generate_realistic_mac():
    vendors = ["00:16:3E", "00:1C:42", "00:0C:29"]
    suffix = ":".join("%02x" % random.randint(0, 255) for _ in range(3))
    mac = random.choice(vendors) + ":" + suffix
    logger.log(f"Yeni gerçekçi MAC üretildi: {mac}")
    return mac

def change_mac(interface, use_realistic=True):
    new_mac = generate_realistic_mac()
    try:
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])
        logger.log(f"{interface} için MAC adresi değiştirildi: {new_mac}")
        return new_mac
    except Exception as e:
        logger.log(f"MAC değiştirme hatası: {e}")
        return None