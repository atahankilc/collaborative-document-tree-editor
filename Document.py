from DocTreeClass import DocTree
from ElementClass import Element
from threading import *
from uuid import uuid4


class DocumentInstancePerUser:
    def __init__(self, document, user):
        self.obj = document
        self.active_user = user
        self.selected_element_id = 0  # root

    def __getattr__(self, item):
        if self.active_user in self.obj.doctree.users.keys():
            return getattr(self.obj, item)
        else:
            raise Exception("Document is closed by the user")

    def select_element(self, element_id):
        if self.active_user in self.obj.doctree.users.keys():
            self.selected_element_id = element_id
        else:
            raise Exception("Document is closed by the user")

    def method_call(self, method_name, *method_args):
        return getattr(self, method_name)(method_args, user=self.active_user,
                                          selected_element_id=self.selected_element_id)


class Document:
    def __init__(self, templfile):
        self._id = uuid4().int
        self.mutex = Lock()
        self.doctree = DocTree(templfile)
        self.selected_element = None

    # method_args = (child_element_name, child_element_id, child_element_pos, )
    def insert_element(self, method_args, **kwargs):
        new_element = Element(name=method_args[0], doctree=self.doctree, id=method_args[1])
        with self.mutex:
            self.doctree.getElementById(kwargs["selected_element_id"]).insertChild(new_element, method_args[2])

    # method_args = (action, path?, )
    def get(self, method_args, **kwargs):
        with self.mutex:
            if method_args[0] == "element_xml":
                return self.doctree.getElementById(kwargs["selected_element_id"]).getXML()
            elif method_args[0] == "element_text":
                return self.doctree.getElementById(kwargs["selected_element_id"]).getText()
            elif method_args[0] == "element_path":
                return self.doctree.getElementByPath(method_args[1])

    # method_args = (
    #               action,
    #               (document_name|change_element_name|element_attr)?,
    #               (change_element_id|element_attr_value)?,
    #               (change_element_pos)?,
    #               )
    def change(self, method_args, **kwargs):
        with self.mutex:
            if method_args[0] == "document_name":
                self.doctree.setName(method_args[1])
            elif method_args[0] == "element_update":
                new_element = Element(name=method_args[1], doctree=self.doctree, id=method_args[2])
                self.doctree.getElementById(kwargs["selected_element_id"]).updateChild(new_element, method_args[3])
            elif method_args[0] == "element_attr":
                self.doctree.getElementById(kwargs["selected_element_id"]).setAttr(method_args[1], method_args[2])

    # method_args = (action, child_pos?, )
    def delete(self, method_args, **kwargs):
        with self.mutex:
            if method_args[0] == "element_id":
                self.doctree.deleteElement(kwargs["selected_element_id"])
            elif method_args[0] == "element_child_pos":
                self.doctree.getElementById(kwargs["selected_element_id"]).removeChild(method_args[1])

    # TODO
    def export(self):
        with self.mutex:
            self.doctree.export(None, None)

    def add_user(self, *args, **kwargs):
        with self.mutex:
            self.doctree.attach(kwargs["user"])

    def remove_user(self, *args, **kwargs):
        with self.mutex:
            self.doctree.detach(kwargs["user"])

    def get_id(self):
        return self._id
