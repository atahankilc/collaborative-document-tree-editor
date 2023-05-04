import sys
import socket
import threading
import UserClass
from Enums import Status


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
            agent = Agent(client, address)
            agent.start()

    def close(self):
        self.sock.close()


class Agent(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.user = None

    def run(self):
        with self.client:
            try:
                while self.user is None or self.user.status == Status.UNAUTHORIZED:
                    self.client.send("Enter username: ".encode())
                    username = self.client.recv(1024).decode().strip()
                    self.client.send("Enter email: ".encode())
                    email = self.client.recv(1024).decode().strip()
                    self.client.send("Enter fullname: ".encode())
                    fullname = self.client.recv(1024).decode().strip()
                    self.client.send("Enter password: ".encode())
                    passwd = self.client.recv(1024).decode().strip()

                    self.user = UserClass.User(username, email, fullname, passwd)
                    self.user.auth(passwd)

                    if self.user.status == Status.UNAUTHORIZED:
                        self.client.send("Invalid username or password".encode())

                while True:
                    self.client.send("Enter command: ".encode())
                    command = self.client.recv(1024).decode().strip()
                    print(f"Received command: {command} from {self.user.username}")
                    # TODO: make calls based on command
                    if command == "close":
                        break
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                self.client.close()


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
