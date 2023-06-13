import sys

sys.path.append("..")

import pickle
import threading
from CommandHandler import CommandHandler
import asyncio
from websockets.server import serve


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

        self.CLIENTS = set()
        self.ws_port = None
        self.ws_token = None

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
                self.ws_token = token
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
            if command[0] == "%WS_PORT%":
                self.send(str(self.ws_port))
                continue
            command_handler.handle_command(command)

    async def relay(self, queue, websocket):
        while True:
            # Implement custom logic based on queue.qsize() and
            # websocket.transport.get_write_buffer_size() here.
            message = await queue.get()
            await websocket.send(message)

    async def client_handler(self, websocket):
        queue = asyncio.Queue()
        relay_task = asyncio.create_task(self.relay(queue, websocket))
        self.CLIENTS.add(queue)
        try:
            await websocket.wait_closed()
        finally:
            self.CLIENTS.remove(queue)
            relay_task.cancel()

    def notification_sender(self):
        with self.user.mutex:
            while self.notification_handler_thread_kill or \
                    self.user is None or \
                    (not self.user.notification_handler_thread_flag) or \
                    (len(self.user.message_queue) == 0):
                if self.notification_handler_thread_kill or \
                        self.user is None:
                    self.notification_handler_thread_created = False
                    return "%EXIT%"
                self.user.cond.wait()
            if self.user.checksession(self.ws_token) == "Invalid":
                return "%EXIT%"
            return self.user.message_queue.pop(0)

    async def notification_main(self):
        async with serve(self.client_handler, "localhost", None) as ws:
            print(ws.sockets[0].getsockname()[1])
            self.ws_port = ws.sockets[0].getsockname()[1]
            while True:
                print("waiting")
                message = await asyncio.get_event_loop().run_in_executor(None, lambda: self.notification_sender())
                print(message)
                if message == "%EXIT%":
                    break
                for queue in self.CLIENTS:
                    queue.put_nowait(message)

    def handle_notifications(self):
        print("notification started")
        asyncio.run(self.notification_main())
        print("notification ended")

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
