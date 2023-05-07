import pickle
from Editor import Editor


class CommandHandler:
    def __init__(self, client, user):
        self.client = client
        self.user = user
        self.commands = {
            "help": self.help,
            "new_document": self.new_document,
            "list_documents": self.list_documents,
            "open_document": self.open_document,
            "close_document": self.close_document,
            "get_current_document_id": self.get_current_document_id,
            "delete_document": self.delete_document,
            "set_document_name": self.set_document_name,
            "select_element": self.select_element,
            "insert_element": self.insert_element,
            "update_element": self.update_element,
            "set_element_attribute": self.set_element_attribute,
            "delete_element": self.delete_element,
            "get_element_xml": self.get_element_xml,
            "get_element_text": self.get_element_text,
            "get_element_path": self.get_element_path,
            "export": self.export,
        }
        self.commandArgCount = {
            "help": (0, 0),
            "new_document": (1, 1),
            "list_documents": (0, 0),
            "open_document": (1, 1),
            "close_document": (0, 0),
            "get_current_document_id": (0, 0),
            "delete_document": (1, 1),
            "set_document_name": (1, 1),
            "select_element": (1, 1),
            "insert_element": (2, 3),
            "update_element": (2, 3),
            "set_element_attribute": (2, 2),
            "delete_element": (0, 1),
            "get_element_xml": (0, 0),
            "get_element_text": (0, 0),
            "get_element_path": (0, 0),
            "export": (3, 3)
        }
        self.editor = Editor()
        self.current_document = None

    def handle_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd in self.commands:
            if self.commandArgCount[cmd][0] <= len(args) <= self.commandArgCount[cmd][1]:
                self.commands[cmd](*args)
            else:
                self.client.send(pickle.dumps("Unmatched argument count"))
        else:
            self.client.send(pickle.dumps("Invalid command"))

    def help(self):
        help_response = ""
        help_dict = {
            "new_document <doctree_template>": "creates a new document from given template",
            "list_documents": "lists all documents",
            "open_document <document_id>": "opens the document with given id",
            "close_document": "closes the currently opened document",
            "get_current_document_id": "returns the id of the open document",
            "delete_document <document_id>": "deletes the document with given id",
            "set_document_name <new_name>": "sets the name of the open document to given name",
            "select_element <element_id>": "selects the element with given id",
            "insert_element <element_type> <position> <element_id>? ": "inserts a new element of given type and id at "
                                                                       "given position",
            "update_element <element_type> <position> <element_id>?": "changes the element at given position to the "
                                                                      "element of given type and id",
            "set_element_attribute <attr_name> <attr_value>": "sets the attribute of the selected element to given "
                                                              "value",
            "delete_element <element_position>?": "deletes the selected element if element_position is not given, else"
                                                  "deletes the child element of the selected element at given position",
            "get_element_xml": "returns the xml of the selected element",
            "get_element_text": "returns the text of the selected element",
            "get_element_path": "returns the xml of the given element path",
            "export <export_type> <export_path> <file_name>": "exports the open document to given path with given "
                                                              "name (supported export types: html)",
            "help": "get information about command usage",
            "exit": "exit the program",
        }

        for command, description in help_dict.items():
            help_response += f"{command}: {description}\n"

        self.client.send(pickle.dumps(help_response))

    def new_document(self, *template_args):
        try:
            template = " ".join(template_args)
            self.editor.new(eval(template))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while creating the document: {e}"))
        else:
            self.client.send(pickle.dumps("Document created successfully"))

    def list_documents(self):
        try:
            doc_list = self.editor.list()
            self.client.send(pickle.dumps(doc_list))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while listing documents: {e}"))

    def open_document(self, doc_id):
        try:
            if self.current_document is not None:
                if self.current_document.obj.get_id() == int(doc_id):
                    self.client.send(pickle.dumps("Document is already open"))
                    return
                self.close_document()
            self.current_document = self.editor.open(int(doc_id), self.user)
        except KeyError:
            self.client.send(pickle.dumps("There is no document with given id"))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while opening the document: {e}"))
        else:
            self.client.send(pickle.dumps("Document opened successfully"))

    def close_document(self):
        try:
            self.editor.close(self.current_document.obj.get_id(), self.user)
            self.current_document = None
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while closing the document: {e}"))
        else:
            self.client.send(pickle.dumps("Document closed successfully"))

    def get_current_document_id(self):
        if self.current_document is None:
            self.client.send(pickle.dumps("There is no open document"))
        else:
            self.client.send(pickle.dumps(self.current_document.obj.get_id()))

    def delete_document(self, doc_id):
        try:
            if self.current_document is not None and self.current_document.obj.get_id() == int(doc_id):
                self.close_document()
            self.editor.delete(int(doc_id))
        except KeyError:
            self.client.send(pickle.dumps("There is no document with given id"))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while deleting the document: {e}"))
        else:
            self.client.send(pickle.dumps("Document deleted successfully"))

    def set_document_name(self, document_name):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                self.current_document.method_call("change", "document_name", document_name)
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while setting the document name: {e}"))
        else:
            self.client.send(pickle.dumps("Document name changed successfully"))

    def select_element(self, element_id):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                self.current_document.select_element(int(element_id))
        except KeyError:
            self.client.send(pickle.dumps("There is no element with given id"))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while selecting the element: {e}"))
        else:
            self.client.send(pickle.dumps("Element selected successfully"))

    def insert_element(self, element_type, position, element_id=0):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                element_id = None if int(element_id) == 0 else int(element_id)
                self.current_document.method_call("insert_element", element_type, element_id, int(position))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while inserting the element: {e}"))
        else:
            self.client.send(pickle.dumps("Element inserted successfully"))

    def update_element(self, element_type, position, element_id=0):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                element_id = None if int(element_id) == 0 else int(element_id)
                self.current_document.method_call("change", "element_update", element_type, element_id, int(position))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while updating the element: {e}"))
        else:
            self.client.send(pickle.dumps("Element updated successfully"))

    def set_element_attribute(self, attr_name, attr_value):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                self.current_document.method_call("change", "element_attr", attr_name, attr_value)
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while setting the element attribute: {e}"))
        else:
            self.client.send(pickle.dumps("Element attribute set successfully"))

    def delete_element(self, element_position=None):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                if element_position is None:
                    self.current_document.method_call("delete", "element_id")
                else:
                    self.current_document.method_call("delete", "element_child_pos", int(element_position))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while deleting the element: {e}"))
        else:
            self.client.send(pickle.dumps("Element deleted successfully"))

    def get_element_xml(self):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                response = self.current_document.method_call("get", "element_xml")
                self.client.send(pickle.dumps(response))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while getting the element xml: {e}"))

    def get_element_text(self):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                response = self.current_document.method_call("get", "element_text")
                self.client.send(pickle.dumps(response))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while getting the element text: {e}"))

    def get_element_path(self, path):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                response = self.current_document.method_call("get", "element_path", path)
                self.client.send(pickle.dumps(response))
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while getting the element path: {e}"))

    def export(self, export_type, export_path, file_name=None):
        try:
            if self.current_document is None:
                self.client.send(pickle.dumps("There is no open document"))
            else:
                self.current_document.method_call("export", export_type, export_path, file_name)
        except Exception as e:
            self.client.send(pickle.dumps(f"a problem occurred while exporting the document: {e}"))
        else:
            self.client.send(pickle.dumps(f"Document exported successfully to {export_path}"))
