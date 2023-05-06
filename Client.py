import socket
import pickle


class Client:
    def __init__(self, port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(("localhost", self.port))

    def send(self, data):
        self.socket.sendall(pickle.dumps(data))

    def receive(self):
        return pickle.loads(self.socket.recv(1024))

    def close(self):
        self.socket.close()
