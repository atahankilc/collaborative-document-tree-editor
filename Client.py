import sys
import socket
import pickle
import threading


class Client:
    BUFFER_SIZE = 1024

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", self.port))
        self.exit_flag = False
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.receive_thread.start()
        self.send_thread = threading.Thread(target=self.send_loop)
        self.send_thread.start()

    def send(self, data):
        self.sock.sendall(pickle.dumps(data))

    def send_loop(self):
        while True:
            data = input()
            self.send(data)

            if data == "exit":
                self.exit_flag = True
                break

    def receive(self):
        serialized_data = b''
        while True:
            chunk = self.sock.recv(self.BUFFER_SIZE)
            if not chunk:
                break
            serialized_data += chunk
            if len(chunk) < self.BUFFER_SIZE:
                break
        return pickle.loads(serialized_data)

    def receive_loop(self):
        while self.exit_flag is False:
            data = self.receive()
            print(data)

        self.close()

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            port = int(sys.argv[2])
            client = Client(port)
        except ValueError:
            print("Invalid port number")
    else:
        print("usage: python Client.py --port <port_number>")