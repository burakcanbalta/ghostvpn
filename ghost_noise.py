import random
import subprocess
import time
import platform
from utils import logger

def generate_fake_traffic():
    targets = ["1.1.1.1", "google.com", "yahoo.com"]
    try:
        while True:
            target = random.choice(targets)
            if platform.system().lower() == "windows":
                subprocess.run(["ping", "-n", "1", target], capture_output=True)
            else:
                subprocess.run(["ping", "-c", "1", target], capture_output=True)
            logger.log(f"Fake trafik gönderildi: ping {target}")
            time.sleep(random.randint(5, 15))
    except Exception as e:
        logger.log(f"Fake trafik üretimi hatası: {e}")
