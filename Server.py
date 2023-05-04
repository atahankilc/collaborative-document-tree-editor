import sys
import socket
import threading
import UserClass


class Server:
    def __init__(self, port):
        self.port = port
        self.sock = None

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", self.port))
        self.sock.listen()

        while True:
            client, address = self.sock.accept()
            # TODO: create agent

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            port = int(sys.argv[2])
            server = Server(port)
            server.start()
        except ValueError:
            print("Invalid port number")
    else:
        print("usage: python Server.py --port <port_number>")
