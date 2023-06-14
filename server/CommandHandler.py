import re
from Editor import Editor
from UserClass import User
from comman_utils.Enums import *


class CommandHandler:
    EMAIL_REGEX = r"^\S+@\S+\.\S+$"

    def __init__(self, agent):
        self.agent = agent
        self.commands = {
            "help": self.help,
            "login": self.login,
            "signup": self.signup,
            "logout": self.logout,
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
            "export": self.export
        }
        self.commandArgCount = {
            "help": (0, 0),
            "login": (2, 2),
            "signup": (4, 4),
            "logout": (0, 0),
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
            "export": (2, 3)
        }
        self.editor = Editor()
        self.current_document = None

    def handle_command(self, command):
        cmd = command[0] if len(command) > 0 else ""
        args = command[1:]
        if cmd not in self.commands:
            self.agent.send("Invalid command")
        elif (len(args) < self.commandArgCount[cmd][0]) or (len(args) > self.commandArgCount[cmd][1]):
            self.agent.send("Unmatched argument count")
        else:
            self.commands[cmd](*args)

    def help(self):
        help_response = ""
        help_dict = {
            "login": "login",
            "signup": "signup",
            "logout": "logput",
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
            "help": "get information about command usage"
        }

        for command, description in help_dict.items():
            help_response += f"{command}: {description}\n"

        self.agent.send(help_response)

    def login(self, username, passwd):
        try:
            self.agent.user = self.agent.server.user_dict[username]
            self.agent.user.auth(passwd)

            if self.agent.user.status == Status.UNAUTHORIZED:
                self.agent.user = None
                self.agent.send("Invalid username or password")
            else:
                token = self.agent.user.login()
                self.agent.send(f"token: {token}")
                self.agent.start_notification()
        except KeyError:
            self.agent.send("You are not registered. Please register first.")

    def signup(self, username, email, fullname, passwd):
        if username in self.agent.server.user_dict:
            self.agent.send("Username already exists. Please choose another username")
        elif not re.fullmatch(self.EMAIL_REGEX, email):
            self.agent.send("Please enter a valid email address")
        else:
            self.agent.user = User(username, email, fullname, passwd)
            self.agent.user.auth(passwd)
            token = self.agent.user.login()
            self.agent.send(f"token: {token}")
            self.agent.start_notification()
            self.agent.server.add_new_user(self.agent.user, passwd)

    def logout(self):
        if self.current_document is not None:
            self.close_document()
        with self.agent.user.mutex:
            self.agent.user.cond.notifyAll()
        self.agent.user = None
        self.agent.send("User logout successfully")

    def new_document(self, *template_args):
        try:
            template = " ".join(template_args)
            self.editor.new(eval(template))
        except Exception as e:
            self.agent.send(f"a problem occurred while creating the document: {e}")
        else:
            self.agent.send("Document created successfully")

    def list_documents(self):
        try:
            doc_list = self.editor.list()
            self.agent.send(doc_list)
        except Exception as e:
            self.agent.send(f"a problem occurred while listing documents: {e}")

    def open_document(self, doc_id):
        try:
            if self.current_document is not None:
                if self.current_document.obj.get_id() == int(doc_id):
                    self.agent.send("Document is already open")
                    return
                self.close_document()
            self.current_document = self.editor.open(int(doc_id), self.agent.user)
        except KeyError:
            self.agent.send("There is no document with given id")
        except Exception as e:
            self.agent.send(f"a problem occurred while opening the document: {e}")
        else:
            self.agent.send("Document opened successfully")

    def close_document(self):
        try:
            self.editor.close(self.current_document.obj.get_id(), self.agent.user)
            self.current_document = None
        except Exception as e:
            self.agent.send(f"a problem occurred while closing the document: {e}")
        else:
            self.agent.send("Document closed successfully")

    def get_current_document_id(self):
        if self.current_document is None:
            self.agent.send("There is no open document")
        else:
            self.agent.send(self.current_document.obj.get_id())

    def delete_document(self, doc_id):
        try:
            if self.current_document is not None and self.current_document.obj.get_id() == int(doc_id):
                self.close_document()
            self.editor.delete(int(doc_id))
        except KeyError:
            self.agent.send("There is no document with given id")
        except Exception as e:
            self.agent.send(f"a problem occurred while deleting the document: {e}")
        else:
            self.agent.send("Document deleted successfully")

    def set_document_name(self, document_name):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                self.current_document.method_call("change", "document_name", document_name)
        except Exception as e:
            self.agent.send(f"a problem occurred while setting the document name: {e}")

    def select_element(self, element_id):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                self.current_document.select_element(int(element_id))
        except KeyError:
            self.agent.send("There is no element with given id")
        except Exception as e:
            self.agent.send(f"a problem occurred while selecting the element: {e}")
        else:
            self.agent.send("Element selected successfully")

    def insert_element(self, element_type, position, element_id=0):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                element_id = None if int(element_id) == 0 else int(element_id)
                self.current_document.method_call("insert_element", element_type, element_id, int(position))
        except Exception as e:
            self.agent.send(f"a problem occurred while inserting the element: {e}")

    def update_element(self, element_type, position, element_id=0):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                element_id = None if int(element_id) == 0 else int(element_id)
                self.current_document.method_call("change", "element_update", element_type, element_id, int(position))
        except Exception as e:
            self.agent.send(f"a problem occurred while updating the element: {e}")

    def set_element_attribute(self, attr_name, attr_value):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                self.current_document.method_call("change", "element_attr", attr_name, attr_value)
        except Exception as e:
            self.agent.send(f"a problem occurred while setting the element attribute: {e}")

    def delete_element(self, element_position=None):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                if element_position is None:
                    self.current_document.method_call("delete", "element_id")
                else:
                    self.current_document.method_call("delete", "element_child_pos", int(element_position))
        except Exception as e:
            self.agent.send(f"a problem occurred while deleting the element: {e}")

    def get_element_xml(self):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                response = self.current_document.method_call("get", "element_xml")
                self.agent.send(response)
        except Exception as e:
            self.agent.send(f"a problem occurred while getting the element xml: {e}")

    def get_element_text(self):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                response = self.current_document.method_call("get", "element_text")
                self.agent.send(response)
        except Exception as e:
            self.agent.send(f"a problem occurred while getting the element text: {e}")

    def get_element_path(self, path):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                response = self.current_document.method_call("get", "element_path", path)
                self.agent.send(response)
        except Exception as e:
            self.agent.send(f"a problem occurred while getting the element path: {e}")

    def export(self, export_type, export_path, file_name=None):
        try:
            if self.current_document is None:
                self.agent.send("There is no open document")
            else:
                self.current_document.method_call("export", export_type, export_path, file_name)
        except Exception as e:
            self.agent.send(f"a problem occurred while exporting the document: {e}")
        else:
            self.agent.send(f"Document exported successfully to {export_path}")
