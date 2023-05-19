import sys
import socket
import pickle
import threading


class Client:
    BUFFER_SIZE = 1024

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", self.port))
        self.exit_flag = False
        self.sending_queue = []
        self.sending_mutex = threading.Lock()
        self.sending_cond = threading.Condition(self.sending_mutex)
        self.receiving_queue = []
        self.receiving_mutex = threading.Lock()
        self.receiving_cond = threading.Condition(self.receiving_mutex)
        self.receive_thread = threading.Thread(target=self.receive_loop)
        self.receive_thread.start()
        self.send_thread = threading.Thread(target=self.send_loop)
        self.send_thread.start()

    def send(self, data):
        self.sock.sendall(pickle.dumps(data))

    def send_loop(self):
        while True:
            with self.sending_mutex:
                while len(self.sending_queue) == 0:
                    self.sending_cond.wait()
                data = self.sending_queue.pop()
            self.send(data)
            if data == "exit":
                self.exit_flag = True
                break

    def add_to_sending_queue(self, data):
        with self.sending_mutex:
            self.sending_queue.append(data)
            self.sending_cond.notifyAll()

    def receive(self):
        serialized_data = b''
        while True:
            chunk = self.sock.recv(self.BUFFER_SIZE)
            if not chunk:
                break
            serialized_data += chunk
            if len(chunk) < self.BUFFER_SIZE:
                break
        return pickle.loads(serialized_data)

    def receive_loop(self):
        while not self.exit_flag:
            try:
                data = self.receive()
                with self.receiving_mutex:
                    self.receiving_queue.append(data)
                    self.receiving_cond.notifyAll()
            except EOFError:
                break

        self.close()

    def pop_from_receiving_queue(self):
        with self.receiving_mutex:
            if len(self.receiving_queue) == 0:
                self.receiving_cond.wait()
            return self.receiving_queue.pop()

    def close(self):
        self.sock.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--port":
        try:
            port = int(sys.argv[2])
            client = Client(port)
        except ValueError:
            print("Invalid port number")
    else:
        print("usage: python Client.py --port <port_number>")
