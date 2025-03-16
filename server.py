import socket
import subprocess
import threading


class Server:
    def __init__(self):
        self.socket = None
        self.host = '0.0.0.0' # Change to use the VM internal IP address
        self.port = 12345 # Replace with server port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
            server_tcp.bind((self.host, self.port))
            server_tcp.listen(1)  # Allow up to 1 connection
            print("[*] Waiting for connections")
            while True:
                try:
                    connection, addr = server_tcp.accept()
                    print(f"[*] Connection from {addr}")
                    while True:
                        data = connection.recv(1024).decode('utf-8')
                        if not data:
                            break
                        print(f"Received data from {addr}: {data}")
                        commands = data.split(":")
                        connection.sendall("Hello from server".encode('utf-8'))
                except Exception as e:
                    print(f"[*] Connection error: {e}")
                    break
                finally:
                    connection.close()
                    server_tcp.close()
                    print("[*] Connection closed, waiting for new client")

if __name__ == "__main__":
    s = Server()
    s.start()
