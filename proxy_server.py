import socket
import threading

def handle_client(client_socket):
    try:
        client_socket.recv(262)
        client_socket.send(b"\x05\x00")
        req = client_socket.recv(4)
        mode = req[1]
        addrtype = req[3]

        if addrtype == 1:
            address = socket.inet_ntoa(client_socket.recv(4))
        elif addrtype == 3:
            domain_length = client_socket.recv(1)[0]
            address = client_socket.recv(domain_length).decode()
        port = int.from_bytes(client_socket.recv(2), 'big')

        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((address, port))
        client_socket.send(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + b"\x00\x00")

        threading.Thread(target=forward, args=(client_socket, remote)).start()
        threading.Thread(target=forward, args=(remote, client_socket)).start()

    except Exception as e:
        client_socket.close()

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.send(data)
    except:
        source.close()
        destination.close()

def start_socks5_server(listen_ip='127.0.0.1', listen_port=1080):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((listen_ip, listen_port))
        server.listen(5)
        print(f"[+] SOCKS5 proxy server started on {listen_ip}:{listen_port}")
        while True:
            client_socket, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except Exception as e:
        print(f"Proxy server error: {e}")import socket
import threading

def handle_client(client_socket):
    try:
        client_socket.recv(262)
        client_socket.send(b"\x05\x00")
        req = client_socket.recv(4)
        mode = req[1]
        addrtype = req[3]

        if addrtype == 1:
            address = socket.inet_ntoa(client_socket.recv(4))
        elif addrtype == 3:
            domain_length = client_socket.recv(1)[0]
            address = client_socket.recv(domain_length).decode()
        port = int.from_bytes(client_socket.recv(2), 'big')

        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((address, port))
        client_socket.send(b"\x05\x00\x00\x01" + socket.inet_aton("0.0.0.0") + b"\x00\x00")

        threading.Thread(target=forward, args=(client_socket, remote)).start()
        threading.Thread(target=forward, args=(remote, client_socket)).start()

    except Exception as e:
        client_socket.close()

def forward(source, destination):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.send(data)
    except:
        source.close()
        destination.close()

def start_socks5_server(listen_ip='127.0.0.1', listen_port=1080):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((listen_ip, listen_port))
        server.listen(5)
        print(f"[+] SOCKS5 proxy server started on {listen_ip}:{listen_port}")
        while True:
            client_socket, addr = server.accept()
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    except Exception as e:
        print(f"Proxy server error: {e}")
