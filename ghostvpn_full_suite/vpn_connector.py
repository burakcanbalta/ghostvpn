
import subprocess
import time

def connect_vpn(config_path):
    try:
        print(f"[+] Connecting to VPN using {config_path}...")
        subprocess.Popen(["sudo", "openvpn", "--config", config_path])
        time.sleep(5)
        print("[+] VPN connection initiated.")
    except Exception as e:
        print(f"[!] Failed to connect VPN: {str(e)}")

def disconnect_vpn():
    try:
        print("[+] Disconnecting VPN...")
        subprocess.call(["sudo", "killall", "openvpn"])
        print("[+] VPN disconnected.")
    except Exception as e:
        print(f"[!] Failed to disconnect VPN: {str(e)}")
