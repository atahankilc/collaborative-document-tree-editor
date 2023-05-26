import sys

sys.path.append("..")

import pickle
import threading
from CommandHandler import CommandHandler


class Agent(threading.Thread):
    BUFFER_SIZE = 1024
    EMAIL_REGEX = r"^\S+@\S+\.\S+$"

    def __init__(self, conn, address, server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address
        self.server = server
        self.mutex = threading.Lock()
        self.cond = threading.Condition(self.mutex)
        self.user = None
        self.request_handler_thread = None
        self.notification_handler_thread_created = False
        self.notification_handler_thread_kill = False
        self.notification_handler_thread = None

    def run(self):
        with self.conn:
            try:
                self.request_handler_thread = threading.Thread(target=self.handle_requests)
                self.request_handler_thread.start()
                self.request_handler_thread.join()
                if self.notification_handler_thread_created:
                    self.notification_handler_thread.join()
            except Exception as e:
                print(f"Exception: {e}")
            print("Agent exited")

    def handle_requests(self):
        command_handler = CommandHandler(self)
        while True:
            if self.user is not None:
                message = self.receive().split()
                token = message[0]
                command = message[1:]
                is_session_valid = self.user.checksession(token)
                if is_session_valid == "Invalid":
                    self.notification_handler_thread_kill = True
                    with self.user.mutex:
                        self.user.cond.notifyAll()
                    self.send('%INVALID_TOKEN%')
                    break
            else:
                command = self.receive().split()
            command_handler.handle_command(command)

    def handle_notifications(self):
        print("notification started")
        while True:
            with self.user.mutex:
                while self.notification_handler_thread_kill or \
                        self.user is None or \
                        (not self.user.notification_handler_thread_flag) or \
                        (len(self.user.message_queue) == 0):
                    if self.notification_handler_thread_kill or \
                            self.user is None:
                        self.notification_handler_thread_created = False
                        print("notification ended")
                        return
                    self.user.cond.wait()
                self.send(self.user.message_queue.pop(0))

    def start_notification(self):
        self.notification_handler_thread = threading.Thread(target=self.handle_notifications)
        self.notification_handler_thread_created = True
        self.notification_handler_thread.start()

    def receive(self):
        serialized_data = b''
        while True:
            chunk = self.conn.recv(self.BUFFER_SIZE)
            if not chunk:
                break
            serialized_data += chunk
            if len(chunk) < self.BUFFER_SIZE:
                break
        return pickle.loads(serialized_data).strip()

    def send(self, message):
        self.conn.send(pickle.dumps(message))
