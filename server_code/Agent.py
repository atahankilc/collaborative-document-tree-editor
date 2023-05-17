import threading
import pickle
import re
from UserClass import User
from CommandHandler import CommandHandler
from Enums import Status


class Agent(threading.Thread):
    BUFFER_SIZE = 1024
    EMAIL_REGEX = r"^\S+@\S+\.\S+$"

    def __init__(self, conn, address, server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.server = server
        self.user = None
        self.exit_flag = False
        self.request_handler_thread = None
        self.notification_handler_thread = None

    def run(self):
        with self.conn:
            try:
                while self.user is None or self.user.status == Status.UNAUTHORIZED:
                    self.conn.send(pickle.dumps("You need to register or login to use collaborative document tree "
                                                "editor\nPlease write 'register' or 'login' to continue: "))
                    auth_type = pickle.loads(self.receive()).strip()

                    if auth_type == "register":
                        self.conn.send(pickle.dumps("Enter credentials: "))
                        response = pickle.loads(self.receive()).strip()
                        response = response.split()
                        username = response[0]
                        email = response[1]
                        fullname = " ".join(response[2:-1])
                        passwd = response[-1]

                        if username in self.server.user_dict:
                            self.conn.send(pickle.dumps("Username already exists. Please choose another username"))
                            continue

                        if not re.fullmatch(self.EMAIL_REGEX, email):
                            self.conn.send(pickle.dumps("Please enter a valid email address"))
                            continue

                        self.user = User(username, email, fullname, passwd)
                        self.user.auth(passwd)
                        self.server.add_new_user(self.user, passwd)
                    elif auth_type == "login":
                        self.conn.send(pickle.dumps("Enter username and password: "))
                        response = pickle.loads(self.receive()).strip()
                        username, passwd = response.split()

                        try:
                            self.user = self.server.user_dict[username]
                        except KeyError:
                            self.conn.send(pickle.dumps("You are not registered. Please register first."))
                            continue

                        self.user.auth(passwd)
                    else:
                        self.conn.send(pickle.dumps("Invalid command. Please write 'register' or 'login' to continue"))
                        continue

                    if self.user.status == Status.UNAUTHORIZED:
                        self.conn.send(pickle.dumps("Invalid username or password"))

                self.conn.send(pickle.dumps(f"Welcome, {self.user.username}. You are now logged in.\nYou can write "
                                            f"'help' to see the list of commands you can use.\n"))

                self.request_handler_thread = threading.Thread(target=self.handle_requests)
                self.request_handler_thread.start()

                self.notification_handler_thread = threading.Thread(target=self.handle_notifications)
                self.notification_handler_thread.start()

                self.request_handler_thread.join()
                self.notification_handler_thread.join()
            except Exception as e:
                print(f"Exception: {e}")

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

            if command == "exit":
                self.exit_flag = True
                with self.user.mutex:
                    self.user.cond.notify()
                break

    def handle_notifications(self):
        while True:
            with self.user.mutex:
                while (not self.user.threadContinueFlag) or (len(self.user.message_queue) == 0) or self.exit_flag:
                    if self.exit_flag:
                        return
                    self.user.cond.wait()
                self.conn.send(pickle.dumps(self.user.message_queue.pop(0)))
