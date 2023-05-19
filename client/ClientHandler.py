import sys

sys.path.append("..")
from comman_utils.Decorators import singleton


@singleton
class ClientHandler:
    def __init__(self):
        self.client_dict = {}


ClientHandler = ClientHandler()
