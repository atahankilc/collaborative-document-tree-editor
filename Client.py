import socket
import pickle


class Client:
    BUFFER_SIZE = 1024

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", self.port))

    def send(self, data):
        self.sock.sendall(pickle.dumps(data))

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

    def close(self):
        self.sock.close()
