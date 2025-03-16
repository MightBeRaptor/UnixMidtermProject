import socket
import subprocess
import os
import json


class Server:
    def __init__(self):
        self.socket = None
        self.host = '0.0.0.0' # Change to use the VM internal IP address
        self.port = 12345 # Replace with server port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_tcp:
            server_tcp.bind((self.host, self.port))
            server_tcp.listen(1)  # Allow up to 1 connection
            print("[*] Waiting for connection")
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
                        print(commands)
                        parse_cmd = commands[0].split()
                        subprocess.run([parse_cmd[0], parse_cmd[1]])
                        # Execute commands
                        # Run parse_metrics.py to get a json file at /data/*filename*.json
                        subprocess.run(["python3", "parse_metrics.py"])
                        # Rename the json to /data/*servername*/*filename*.json
                        metrics_path = [entry.name for entry in os.scandir("data") if entry.is_file()]
                        os.makedirs(os.path.join("data", socket.gethostname()), exist_ok=True)
                        os.rename("data/" + metrics_path[0], "data/" + socket.gethostname() + "/" + metrics_path[0])
                        connection.sendall(("data/" + socket.gethostname() + "/" + metrics_path[0]).encode('utf-8'))
                        json_file = str("data/" + socket.gethostname() + "/" + metrics_path[0])
                        print("[*] Opening json file")
                        with open(json_file, "r") as f:
                            json_data = json.load(f)
                        print("[*] JSON file opened, parsing data")
                        json_str = json.dumps(json_data)
                        print("[*] Sending the data to client")
                        for i in range(0, len(json_str), 1024):
                            chunk = json_str[i:i + 1024]
                            connection.sendall(chunk.encode('utf-8'))
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
