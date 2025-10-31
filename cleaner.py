import subprocess
import platform
import os

def clean_disconnect():
    try:
        print("[+] Cleaning system: Stopping VPN, Proxy, and Tor services...")
        
        system_platform = platform.system().lower()
        is_linux = system_platform == "linux"
        is_windows = system_platform == "windows"
        
        if is_linux:
            subprocess.run(["pkill", "openvpn"], capture_output=True)
            subprocess.run(["systemctl", "stop", "tor"], capture_output=True)
            subprocess.run(["pkill", "-f", "proxy_server.py"], capture_output=True)
            
            try:
                subprocess.run(["systemd-resolve", "--flush-caches"], capture_output=True)
            except:
                subprocess.run(["resolvectl", "flush-caches"], capture_output=True)
                
        elif is_windows:
            subprocess.run(["taskkill", "/F", "/IM", "openvpn.exe"], capture_output=True, shell=True)
            subprocess.run(["taskkill", "/F", "/IM", "tor.exe"], capture_output=True, shell=True)
            subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True, shell=True)
            
            subprocess.run(["ipconfig", "/flushdns"], capture_output=True, shell=True)
        
        print("[+] Services stopped and DNS cache flushed.")
        
    except Exception as e:
        print(f"[!] Error during cleanup: {str(e)}")

if __name__ == "__main__":
    if os.name != 'nt' and os.geteuid() != 0:
        print("[!] Warning: Script should be run with sudo for full functionality")
    
    clean_disconnect()
