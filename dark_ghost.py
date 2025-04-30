import subprocess
from ram_system import RamSystem
from ghost_kill import GhostKill

class DarkGhost:
    def __init__(self):
        self.ram_system = RamSystem()
        self.ghost_kill = GhostKill()
        
    def activate(self):
        print("🔒 DarkGhost Mode Activating...")
        
        # 1. Tüm gereksiz servisleri kapat
        self.ghost_kill.kill_processes()
        
        # 2. RAM'e geç
        self.ram_system.move_to_ram("/etc/ghostvpn/config.ovpn")
        
        # 3. Swap ve cache temizle
        self.ram_system.disable_swap()
        self.ram_system.clear_ram()
        
        # 4. JavaScriptsiz tarayıcı başlat
        self.start_secure_browser()
        
        # 5. Tor + VPN zinciri
        self.start_tor_vpn_chain()
        
        print("🕶️ DarkGhost Mode Active - You are now invisible")
        
    def start_secure_browser(self):
        subprocess.Popen([
            'firefox', 
            '--private-window',
            '--disable-javascript',
            '--no-remote',
            'about:blank'
        ])
        
    def start_tor_vpn_chain(self):
        subprocess.Popen([
            'sudo', 'openvpn',
            '--config', '/dev/shm/ghostvpn/config.ovpn',
            '--route-nopull',
            '--route-up', 'torify'
        ])