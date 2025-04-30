# core/ghostcloak.py

from setproctitle import setproctitle
from utils import logger

def ghost_cloak(name="bash"):
    try:
        setproctitle(name)
        logger.log(f"İşlem adı değiştirildi: {name}")
    except Exception as e:
        logger.log(f"GhostCloak hata: {e}")