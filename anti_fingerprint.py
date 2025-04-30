import random
import time
import subprocess

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
        subprocess.run(["curl", "-s", f"http://{random.choice(domains)}"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    def random_dns_query(self):
        domains = ["google.com", "yahoo.com", "bing.com"]
        subprocess.run(["dig", "+short", random.choice(domains)], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)