# core/ghost_noise.py

import random
import subprocess
import time
from utils import logger

def generate_fake_traffic():
    targets = ["1.1.1.1", "google.com", "yahoo.com"]
    try:
        while True:
            target = random.choice(targets)
            subprocess.call(["ping", "-c", "1", target])
            logger.log(f"Fake trafik gönderildi: ping {target}")
            time.sleep(random.randint(5, 15))
    except Exception as e:
        logger.log(f"Fake trafik üretimi hatası: {e}")