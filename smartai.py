import psutil
from utils import logger
from core.ghost_kill import ghost_kill

def check_sandbox_conditions():
    try:
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        net = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

        logger.log(f"SmartAI Kontrol ➜ CPU: {cpu}% | RAM: {mem}% | Net: {net} byte")

        if cpu > 85 and net < 1024:
            logger.log("[!] Sandbox ortamı şüphesi. GhostKill tetikleniyor.")
            ghost_kill()
    except Exception as e:
        logger.log(f"SmartAI kontrol hatası: {e}")
