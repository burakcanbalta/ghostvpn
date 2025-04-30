# 👻 GhostVPN Ultra — Stealth Red Team VPN Toolkit

GhostVPN Ultra is a fully integrated Python-based privacy and stealth framework that operates as a **single executable file**.  
Built for penetration testers, researchers, and red team simulations, it combines VPN, Tor, SOCKS5 Proxy, RAM-only execution, traffic obfuscation, AI-based idle simulation, sandbox detection, and self-destruct mechanisms.

---

## 🚀 Features

| Category | Feature |
|---------|---------|
| 🔁 Networking | VPN (.ovpn) and Tor fallback connection |
| 🎭 Identity Spoofing | MAC changer with realistic vendor prefixes |
| 🧠 Behavior Simulation | Human-like fake terminal activity |
| 🧅 Proxy Mode | Built-in SOCKS5 server (127.0.0.1:1080) |
| 🔥 GhostKill | Self-destruction on threat detection |
| 💣 Honeypot | Fake SSH listener + process scanner |
| 🧹 RAM-only Execution | Disables swap, wipes tmp files |
| 📊 Web Dashboard | Flask-based status panel (localhost:5000) |
| 🧬 Sandbox Detection | High CPU/low net = likely VM = exit |
| 📦 All-in-One | Single-file agent with CLI menu |

---

## 🖥️ CLI Menu Options

```text
[1] VPN Başlat
[2] Tor Başlat
[3] SOCKS Proxy Başlat
[4] AI Sahte Trafik
[5] Kendini İmha Et (GhostKill)
[0] Çıkış
```

---

## 🌐 Web Dashboard

GhostVPN runs a built-in Flask server on [http://localhost:5000/status](http://localhost:5000/status)

Example Output:
```json
{
  "status": "Aktif",
  "ip": "192.168.x.x",
  "tor": "Açık",
  "vpn": "Açık",
  "socks_proxy": "127.0.0.1:1080",
  "log": "ghostvpn.log"
}
```

---

## 🔐 How It Works

1. Loads config settings and decrypts if needed
2. Spoofs MAC address with realistic OUI
3. Attempts VPN connection; falls back to Tor if failed
4. Starts local SOCKS proxy for anonymized routing
5. Activates RAM-only cleanup (swap off, tmp clear)
6. Begins AI idle simulation loop (optional)
7. Starts web dashboard for local visibility
8. CLI menu allows real-time control
9. Detects suspicious processes or sandbox signs
10. If compromised → GhostKill erases all traces and exits

---

## ⚙️ Requirements

- Python 3.8+
- Linux (tested on Kali, Parrot)
- Installed: `openvpn`, `tor`, `psutil`, `flask`, `setproctitle`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚦 Usage

```bash
sudo python3 ghostvpn_ultra.py
```

- Choose functions via CLI menu
- Access dashboard at `localhost:5000/status`
- Logs are saved in `ghostvpn.log` unless disabled

---

## ⚠️ Legal Notice

> This tool is provided for **educational and authorized red team use only**.  
> Any misuse or unauthorized deployment is strictly prohibited and may violate local or international laws.  
> Use responsibly and only in controlled environments.

---

## 📂 Repository Structure

```bash
ghostvpn_ultra.py         # 🔁 All-in-one agent script
requirements.txt          # 📦 Dependencies
README.md                 # 📖 This documentation
ghostvpn.log              # 📝 Runtime logs (if enabled)
```

---

## 🧠 Author Note

GhostVPN is a lightweight, modular privacy agent built for **practical stealth operations**.  
Its single-file architecture ensures **portability, simplicity**, and **rapid deployment** in hostile or controlled environments.

Stay invisible. Stay safe. 👻
