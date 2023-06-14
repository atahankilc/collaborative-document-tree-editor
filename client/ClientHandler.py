import sys

sys.path.append("..")
from comman_utils.Decorators import singleton
from .Client import Client


@singleton
class ClientHandler:
    def __init__(self):
        self.client_dict = {}
        self.port = None

    @staticmethod
    def set_port(port):
        ClientHandler.port = port

    @staticmethod
    def add_session(session_id):
        ClientHandler.client_dict[session_id] = Client(ClientHandler.port)

    @staticmethod
    def get_session(session_id):
        return ClientHandler.client_dict[session_id]

    @staticmethod
    def remove_session(session_id):
        del ClientHandler.client_dict[session_id]

    @staticmethod
    def send_to_session(session_id, command, token=''):
        ClientHandler.client_dict[session_id].add_to_sending_queue(f'{token} {command}')

    @staticmethod
    def receive_from_session(session_id, ending_condition):
        message_block = ''
        while True:
            message = f'{ClientHandler.client_dict[session_id].pop_from_receiving_queue()}'
            if message == '%INVALID_TOKEN%':
                ClientHandler.terminate_session(session_id)
                return "Invalid Token"
            message_block += message
            if message.startswith(ending_condition):
                return message_block
            message_block += '\n'

    @staticmethod
    def terminate_session(session_id):
        del ClientHandler.client_dict[session_id]
        ClientHandler.add_session(session_id)


ClientHandler = ClientHandler()

# -- for debugging --
# ClientHandler.add_session(1)
# while(True):
#     data = input()
#     ClientHandler.client_dict[1].add_to_sending_queue(data)
#     if data == "exit":
#         break
#     print(ClientHandler.client_dict[1].pop_from_receiving_queue())
#     if data == "logout":
#         print(ClientHandler.client_dict[1].pop_from_receiving_queue())
# print(ClientHandler.client_dict)
