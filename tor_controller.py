import subprocess
import time

def start_tor_service():
    try:
        print("[+] Starting Tor service...")
        subprocess.run(["systemctl", "start", "tor"], check=False)
        time.sleep(5)
        print("[+] Tor service started.")
    except Exception as e:
        print(f"[!] Failed to start Tor service: {str(e)}")

def stop_tor_service():
    try:
        print("[+] Stopping Tor service...")
        subprocess.run(["systemctl", "stop", "tor"], check=False)
        print("[+] Tor service stopped.")
    except Exception as e:
        print(f"[!] Failed to stop Tor service: {str(e)}")
