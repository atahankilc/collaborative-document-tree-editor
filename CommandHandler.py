import Editor


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
        self.editor = Editor.Editor()

    def handle_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd in self.commands:
            self.commands[cmd](*args)
        else:
            self.client.send("Invalid command".encode())

    def new_document(self, template):
        # TODO: template is received as a string, convert it to a dictionary
        self.editor.new(template)

    def list_documents(self):
        doc_list = self.editor.list()
        self.client.send(doc_list.encode())

    def open_document(self, doc_id):
        self.editor.open(int(doc_id))

    def close_document(self, doc_id):
        self.editor.close(int(doc_id))

    def delete_document(self, doc_id):
        self.editor.delete(int(doc_id))
