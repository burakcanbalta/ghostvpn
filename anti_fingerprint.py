import random
import time
import subprocess
import platform

class AntiFingerprint:
    def __init__(self):
        self.behavior_profiles = [
            {"name": "casual", "delay": (1, 3), "actions": 5},
            {"name": "researcher", "delay": (3, 7), "actions": 10},
            {"name": "developer", "delay": (0.5, 2), "actions": 15}
        ]
        self.current_profile = None
        
    def randomize_profile(self):
        self.current_profile = random.choice(self.behavior_profiles)
        
    def generate_noise(self):
        actions = [
            self.random_http_request,
            self.random_dns_query,
            self.random_delay,
            self.random_mouse_movement,
            self.random_key_press
        ]
        
        for _ in range(self.current_profile["actions"]):
            action = random.choice(actions)
            action()
            time.sleep(random.uniform(*self.current_profile["delay"]))
            
    def random_http_request(self):
        domains = ["example.com", "test.org", "dummy.net"]
        try:
            if platform.system() == "Windows":
                subprocess.run(["curl", "-s", f"http://{random.choice(domains)}"], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            else:
                subprocess.run(["curl", "-s", f"http://{random.choice(domains)}"], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        
    def random_dns_query(self):
        domains = ["google.com", "yahoo.com", "bing.com"]
        try:
            if platform.system() == "Windows":
                subprocess.run(["nslookup", random.choice(domains)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            else:
                subprocess.run(["dig", "+short", random.choice(domains)], 
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        
    def random_delay(self):
        pass
        
    def random_mouse_movement(self):
        try:
            if platform.system() == "Windows":
                import pyautogui
                pyautogui.moveRel(random.randint(-10, 10), random.randint(-10, 10))
            else:
                subprocess.run(["xdotool", "mousemove_relative", "--", 
                               str(random.randint(-10, 10)), str(random.randint(-10, 10))],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
        
    def random_key_press(self):
        try:
            if platform.system() == "Windows":
                import pyautogui
                pyautogui.press('shift')
            else:
                subprocess.run(["xdotool", "key", "Shift_L"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

if __name__ == "__main__":
    afp = AntiFingerprint()
    afp.randomize_profile()
    print(f"Seçilen profil: {afp.current_profile['name']}")
    afp.generate_noise()
