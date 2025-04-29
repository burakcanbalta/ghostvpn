
import subprocess
import random
import re

def get_current_mac(interface):
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result.stdout)
    if mac_address_search:
        return mac_address_search.group(0)
    else:
        return None

def generate_random_mac():
    mac = [0x00, 0x16, 0x3e,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def change_mac(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    print(f"[+] MAC address for {interface} changed to {new_mac}")

def restore_mac(interface, original_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", original_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    print(f"[+] MAC address for {interface} restored to {original_mac}")
