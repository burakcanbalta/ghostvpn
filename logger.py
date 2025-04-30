# utils/logger.py

from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    formatted = f"{timestamp} {message}"
    print(formatted)
    try:
        with open("ghostvpn.log", "a") as f:
            f.write(formatted + "\n")
    except:
        pass