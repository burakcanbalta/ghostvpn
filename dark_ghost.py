import subprocess
import os
from ram_system import RamSystem
from ghost_kill import GhostKill

class DarkGhost:
    def __init__(self):
        self.ram_system = RamSystem()
        self.ghost_kill = GhostKill()
        
    def activate(self):
        print("🔒 DarkGhost Mode Activating...")
        
        self.ghost_kill.kill_processes()
        
        config_path = "/etc/ghostvpn/config.ovpn"
        if os.path.exists(config_path):
            self.ram_system.move_to_ram(config_path)
        
        self.ram_system.disable_swap()
        self.ram_system.clear_ram()
        
        self.start_secure_browser()
        
        self.start_tor_vpn_chain()
        
        print("🕶️ DarkGhost Mode Active - You are now invisible")
        
    def start_secure_browser(self):
        try:
            subprocess.Popen([
                'firefox', 
                '--private-window',
                '--no-remote',
                'about:blank'
            ])
        except Exception as e:
            print(f"Browser error: {e}")
        
    def start_tor_vpn_chain(self):
        try:
            config_file = '/dev/shm/ghostvpn/config.ovpn'
            if os.path.exists(config_file):
                subprocess.Popen([
                    'openvpn',
                    '--config', config_file,
                    '--route-nopull'
                ])
        except Exception as e:
            print(f"VPN error: {e}")
