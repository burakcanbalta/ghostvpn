import os
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib

class ConfigManager:
    def __init__(self):
        self.temp_dir = "/dev/shm/ghostvpn"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.key = hashlib.sha256(b'ghostvpn-master-key').digest()
        
    def encrypt_config(self, data, filename):
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        with open(filename, 'wb') as f:
            f.write(cipher.iv)
            f.write(ct_bytes)
            
    def decrypt_config(self, filename):
        with open(filename, 'rb') as f:
            iv = f.read(16)
            ct = f.read()
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    
    def secure_delete(self, path, passes=3):
        with open(path, 'ba+') as f:
            length = f.tell()
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(path)
