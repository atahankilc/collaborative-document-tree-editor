import sys

sys.path.append("..")
from comman_utils.Decorators import singleton
from .Client import Client


@singleton
class ClientHandler:
    def __init__(self):
        self.client_dict = {}

    def add_session(self, session_id):
        self.client_dict[session_id] = Client(50001)

    def remove_session(self, session_id):
        del self.client_dict[session_id]


ClientHandler = ClientHandler()

# -- for debugging --
# ClientHandler.add_session(1)
# while(True):
#     print(ClientHandler.client_dict[1].pop_from_receiving_queue())
#     data = input()
#     ClientHandler.client_dict[1].add_to_sending_queue(data)
#     if data == "exit":
#         break
# print(ClientHandler.client_dict)
