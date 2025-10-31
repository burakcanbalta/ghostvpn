import os
import subprocess
from utils import logger

def clean_ghostvpn_files():
    files = ["ghostvpn.log", "status.json"]
    for file in files:
        if os.path.exists(file):
            try:
                subprocess.run(["shred", "-u", file], check=False)
                logger.log(f"İz temizlendi: {file}")
            except Exception as e:
                logger.log(f"{file} silinemedi: {e}")
