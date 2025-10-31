from setproctitle import setproctitle
from utils import logger

def ghost_cloak(name="bash"):
    try:
        setproctitle(name)
        logger.log(f"İşlem adı değiştirildi: {name}")
        return True
    except Exception as e:
        logger.log(f"GhostCloak hata: {e}")
        return False
