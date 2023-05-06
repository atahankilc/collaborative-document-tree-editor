import threading
import pickle
from UserClass import User
from CommandHandler import CommandHandler
from Enums import Status


class Agent(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.user = None
        self.request_handler_thread = None
        self.notification_handler_thread = None

    def run(self):
        with self.conn:
            try:
                while self.user is None or self.user.status == Status.UNAUTHORIZED:
                    self.conn.send(pickle.dumps("Enter username: "))
                    username = pickle.loads(self.conn.recv(1024)).strip()
                    self.conn.send(pickle.dumps("Enter email: "))
                    email = pickle.loads(self.conn.recv(1024)).strip()
                    self.conn.send(pickle.dumps("Enter fullname: "))
                    fullname = pickle.loads(self.conn.recv(1024)).strip()
                    self.conn.send(pickle.dumps("Enter password: "))
                    passwd = pickle.loads(self.conn.recv(1024)).strip()

                    self.user = User(username, email, fullname, passwd)
                    self.user.auth(passwd)

                    if self.user.status == Status.UNAUTHORIZED:
                        self.conn.send(pickle.dumps("Invalid username or password"))

                print(f"User {self.user.username} logged in successfully")

                self.request_handler_thread = threading.Thread(target=self.handle_requests)
                self.request_handler_thread.start()

                self.notification_handler_thread = threading.Thread(target=self.handle_notifications)
                self.notification_handler_thread.start()

                self.request_handler_thread.join()
                self.notification_handler_thread.join()
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                self.conn.close()

    def handle_requests(self):
        command_handler = CommandHandler(self.conn)

        while True:
            self.conn.send(pickle.dumps("Enter command: "))
            command = pickle.loads(self.conn.recv(1024)).strip()

            if command == "exit":
                break
            else:
                command_handler.handle_command(command)

    # TODO
    def handle_notifications(self):
        pass
