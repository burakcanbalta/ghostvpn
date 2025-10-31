import subprocess
import time
import os

def connect_vpn(config_path):
    try:
        print(f"[+] Connecting to VPN using {config_path}...")
        if os.path.exists(config_path):
            subprocess.Popen(["openvpn", "--config", config_path])
            time.sleep(5)
            print("[+] VPN connection initiated.")
        else:
            print(f"[!] VPN config file not found: {config_path}")
    except Exception as e:
        print(f"[!] Failed to connect VPN: {str(e)}")

def disconnect_vpn():
    try:
        print("[+] Disconnecting VPN...")
        subprocess.run(["pkill", "openvpn"], check=False)
        print("[+] VPN disconnected.")
    except Exception as e:
        print(f"[!] Failed to disconnect VPN: {str(e)}")
