import pickle
from Editor import Editor


class CommandHandler:
    def __init__(self, client):
        self.client = client
        self.commands = {
            "new_document": self.new_document,
            "list_documents": self.list_documents,
            "open_document": self.open_document,
            "close_document": self.close_document,
            "delete_document": self.delete_document,
        }
        self.editor = Editor()

    def handle_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd in self.commands:
            self.commands[cmd](*args)
        else:
            self.client.send(pickle.dumps("Invalid command"))

    def new_document(self, template):
        self.editor.new(eval(template))

    def list_documents(self):
        doc_list = self.editor.list()
        self.client.send(pickle.dumps(doc_list))

    def open_document(self, doc_id):
        self.editor.open(int(doc_id))

    def close_document(self, doc_id):
        self.editor.close(int(doc_id))

    def delete_document(self, doc_id):
        self.editor.delete(int(doc_id))
