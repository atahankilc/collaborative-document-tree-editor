import threading
import pickle
import re
from UserClass import User
from CommandHandler import CommandHandler
from Enums import Status


class Agent(threading.Thread):
    BUFFER_SIZE = 1024
    EMAIL_REGEX = r"^\S+@\S+\.\S+$"

    def __init__(self, conn, address, user_dict):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.user_dict = user_dict
        self.user = None
        self.exit_flag = False
        self.request_handler_thread = None
        self.notification_handler_thread = None

    def run(self):
        with self.conn:
            try:
                while self.user is None or self.user.status == Status.UNAUTHORIZED:
                    self.conn.send(pickle.dumps("Enter username: "))
                    username = pickle.loads(self.receive()).strip()

                    while True:
                        self.conn.send(pickle.dumps("Enter email: "))
                        email = pickle.loads(self.receive()).strip()
                        if re.fullmatch(self.EMAIL_REGEX, email):
                            break
                        self.conn.send(pickle.dumps("Please enter a valid email address"))

                    self.conn.send(pickle.dumps("Enter fullname: "))
                    fullname = pickle.loads(self.receive()).strip()
                    self.conn.send(pickle.dumps("Enter password: "))
                    passwd = pickle.loads(self.receive()).strip()

                    self.user = User(username, email, fullname, passwd)
                    self.user.auth(passwd)

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
