import threading
import UserClass
import CommandHandler
from Enums import Status


class Agent(threading.Thread):
    def __init__(self, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.user = None
        self.request_handler_thread = None
        self.notification_handler_thread = None

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

                self.request_handler_thread = threading.Thread(target=self.handle_requests)
                self.request_handler_thread.start()

                self.notification_handler_thread = threading.Thread(target=self.handle_notifications)
                self.notification_handler_thread.start()

                self.request_handler_thread.join()
                self.notification_handler_thread.join()
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                self.client.close()

    def handle_requests(self):
        command_handler = CommandHandler.CommandHandler(self.client)

        while True:
            self.client.send("Enter command: ".encode())
            command = self.client.recv(1024).decode().strip()

            if command == "exit":
                break
            else:
                command_handler.handle_command(command)

    # TODO
    def handle_notifications(self):
        pass
