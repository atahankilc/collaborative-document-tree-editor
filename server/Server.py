from UserClass import User
from Agent import Agent
import socket
import json
import sys


class Server:
    def __init__(self, port):
        self.port = port
        self.sock = None
        self.user_dict = {}
        self._get_user_dict()

    def _get_user_dict(self):
        with open("database.JSON", "r") as f:
            for userObj in json.load(f)["users"]:
                self.user_dict[userObj["username"]] = User(userObj["username"], userObj["email"], userObj["fullname"],
                                                           userObj["password"])

    def add_new_user(self, user, plainpass):
        self.user_dict[user.username] = user
        with open("database.json", "r") as f:
            data = json.load(f)
            data["users"].append({
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "password": plainpass
            })

        with open("database.json", "w") as f:
            json.dump(data, f, indent=4)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", self.port))
        self.sock.listen()

        while True:
            print("Waiting for connection...")
            conn, address = self.sock.accept()
            print(f"Connection from {address}")
            agent = Agent(conn, address, self)
            agent.start()

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
