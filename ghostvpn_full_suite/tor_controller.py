
import subprocess
import time

def start_tor_service():
    try:
        print("[+] Starting Tor service...")
        subprocess.call(["sudo", "systemctl", "start", "tor"])
        time.sleep(5)
        print("[+] Tor service started.")
    except Exception as e:
        print(f"[!] Failed to start Tor service: {str(e)}")

def stop_tor_service():
    try:
        print("[+] Stopping Tor service...")
        subprocess.call(["sudo", "systemctl", "stop", "tor"])
        print("[+] Tor service stopped.")
    except Exception as e:
        print(f"[!] Failed to stop Tor service: {str(e)}")
