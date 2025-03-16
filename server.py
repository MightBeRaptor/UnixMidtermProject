import socket
import subprocess


class Server:
    def __init__(self):
        self.socket = None
        self.host = '127.0.0.1' # Change to use the VM internal IP address
        self.port = 3300 # Replace with server port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
            try:
                server_tcp.bind((self.host, self.port))
                # Wait for a client connection
                print("[*] Waiting for connection")
                while True:
                    server_tcp.listen()
                    # Establish client connection
                    connection, addr = server_tcp.accept()
                    print(f'[*] Established connection from IP {addr[0]} port : {addr[1]}')
                    with connection:
                        data = connection.recv(1024)
                        print(f'[*] Command received: {data.decode('utf-8')}')
            except Exception as e:
                print(f"[*] Connection error: {e}")
                connection.close()

    def start_test(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print("[*] Connection established")
        self.socket.send(f"Hello from {socket.gethostbyname(socket.gethostname())}".encode('utf-8'))
        while True:
            command = self.socket.recv(1024)
            print(f"[*] Received: {command.decode('utf-8')}")




if __name__ == "__main__":
    s = Server()
    s.start_test()
