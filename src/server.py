import socket
import subprocess
import os
import json
import struct


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
                try: # attempt to connect to client
                    connection, addr = server_tcp.accept()
                    print(f"[*] Connection from {addr}")
                    while True: # receive the commands to execute from client
                        data = connection.recv(1024).decode('utf-8')
                        if not data:
                            break
                        print(f"Received data from {addr}: {data}")
                        commands = data.split(":")
                        print(commands)
                        parse_cmd = commands[0].split() # run the first command
                        subprocess.run([parse_cmd[0], parse_cmd[1]])
                        # Execute commands
                        # Run parse_metrics.py to get a json file at /data/*filename*.json
                        subprocess.run(["python3", "UnixMidtermServer/src/parse_metrics.py"])
                        # Rename the json to /data/*servername*/*filename*.json
                        metrics_path = [entry.name for entry in os.scandir("UnixMidtermServer/data") if entry.is_file()]
                        os.makedirs(os.path.join("UnixMidtermServer/data", socket.gethostname()), exist_ok=True)
                        os.rename("UnixMidtermServer/data/" + metrics_path[0], "data/" + socket.gethostname() + "/" + metrics_path[0])
                        # send the file path and name to the client
                        connection.sendall(("data/" + socket.gethostname() + "/" + metrics_path[0]).encode('utf-8'))
                        # open the json file and read the contents
                        json_file = str("data/" + socket.gethostname() + "/" + metrics_path[0])
                        print("[*] Opening json file")
                        with open(json_file, "r") as f:
                            json_data = json.load(f)
                        print("[*] JSON file opened, parsing data")
                        json_str = json.dumps(json_data)
                        json_bytes = json_str.encode('utf-8')

                        # send the length of the JSON first (4 bytes)
                        connection.sendall(struct.pack('!I', len(json_bytes)))

                        # send the JSON data in chunks
                        for i in range(0, len(json_bytes), 1024):
                            chunk = json_bytes[i:i + 1024]
                            connection.sendall(chunk)
                except Exception as e: # error handling
                    print(f"[*] Connection error: {e}")
                    break
                finally: # close connection if an error occurs
                    connection.close()
                    print("[*] Connection closed, waiting for new client")


if __name__ == "__main__":
    s = Server()
    s.start()
