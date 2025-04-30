
import subprocess

def clean_disconnect():
    try:
        print("[+] Cleaning system: Stopping VPN, Proxy, and Tor services...")
        subprocess.call(["sudo", "killall", "openvpn"])
        subprocess.call(["sudo", "systemctl", "stop", "tor"])
        subprocess.call(["sudo", "pkill", "-f", "proxy_server.py"])
        print("[+] Services stopped.")
        subprocess.call(["sudo", "systemd-resolve", "--flush-caches"])
        print("[+] DNS cache flushed.")
    except Exception as e:
        print(f"[!] Error during cleanup: {str(e)}")

if __name__ == "__main__":
    clean_disconnect()
