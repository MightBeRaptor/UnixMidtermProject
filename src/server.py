import socket


class Server:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3300 # Replace with server port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
            try:
                server_tcp.bind((self.host, self.port))
                # Wait for a client connection
                while True:
                    server_tcp.listen()
                    print("[*] Waiting for connection")
                    # Establish client connection
                    connection, addr = server_tcp.accept()
                    with connection:
                        print(f'[*] Established connection from IP {addr[0]} port : {addr[1]}')
                        connection.send(b'Hello, client!')
            except Exception as e:
                print(f"[*] Connection error: {e}")
            finally:
                print(f"[*] Closing connection from IP {addr[0]} port : {addr[1]}")
                connection.close()


if __name__ == "__main__":
    s = Server()
    s.start()
