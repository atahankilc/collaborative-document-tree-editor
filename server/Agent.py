import sys

sys.path.append("..")

import re
import pickle
import threading
from comman_utils.Enums import *
from UserClass import User
from CommandHandler import CommandHandler


class Agent(threading.Thread):
    BUFFER_SIZE = 1024
    EMAIL_REGEX = r"^\S+@\S+\.\S+$"

    def __init__(self, conn, address, server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.server = server
        self.user = None
        self.logout_flag = False
        self.exit_flag = False
        self.request_handler_thread = None
        self.notification_handler_thread = None

    def run(self):
        with self.conn:
            while True:
                try:
                    while self.user is None or self.user.status == Status.UNAUTHORIZED:
                        response = pickle.loads(self.receive()).strip().split()
                        if response[0] == "login":
                            self.login(response)
                        elif response[0] == "signup":
                            self.signup(response)
                        elif response[0] == "exit":
                            self.exit_flag = True
                            break

                        if self.user is None:
                            continue
                        elif self.user.status == Status.UNAUTHORIZED:
                            self.conn.send(pickle.dumps("Invalid username or password"))
                        else:
                            token = self.user.login()
                            self.conn.send(pickle.dumps(f"token: {token}"))

                    if self.exit_flag:
                        break

                    self.request_handler_thread = threading.Thread(target=self.handle_requests)
                    self.request_handler_thread.start()

                    self.notification_handler_thread = threading.Thread(target=self.handle_notifications)
                    self.notification_handler_thread.start()

                    self.request_handler_thread.join()
                    self.notification_handler_thread.join()

                    self.logout()

                except Exception as e:
                    print(f"Exception: {e}")

    def login(self, response):
        username, passwd = response[1], response[2]

        try:
            self.user = self.server.user_dict[username]
            self.user.auth(passwd)
        except KeyError:
            self.conn.send(pickle.dumps("You are not registered. Please register first."))

    def signup(self, response):
        username, email, fullname, passwd = response[1], response[2], " ".join(response[3:-1]), response[-1]

        if username in self.server.user_dict:
            self.conn.send(pickle.dumps("Username already exists. Please choose another username"))
        elif not re.fullmatch(self.EMAIL_REGEX, email):
            self.conn.send(pickle.dumps("Please enter a valid email address"))
        else:
            self.user = User(username, email, fullname, passwd)
            self.user.auth(passwd)
            self.server.add_new_user(self.user, passwd)

    def logout(self):
        self.user.logout()
        self.user = None
        self.logout_flag = False
        self.conn.send(pickle.dumps("User logout successfully"))

    def receive(self):
        serialized_data = b''
        while True:
            chunk = self.conn.recv(self.BUFFER_SIZE)
            if not chunk:
                break
            serialized_data += chunk
            if len(chunk) < self.BUFFER_SIZE:
                break
        return serialized_data

    def handle_requests(self):
        command_handler = CommandHandler(self.conn, self.user)

        while True:
            command = pickle.loads(self.receive()).strip()
            command_handler.handle_command(command)

            if command == "logout":
                self.logout_flag = True
                with self.user.mutex:
                    self.user.cond.notify()
                break

    def handle_notifications(self):
        while True:
            with self.user.mutex:
                while self.logout_flag or (not self.user.threadContinueFlag) or (len(self.user.message_queue) == 0):
                    if self.logout_flag:
                        return
                    self.user.cond.wait()
                self.conn.send(pickle.dumps(self.user.message_queue.pop(0)))
