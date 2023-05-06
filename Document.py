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
        return getattr(self, method_name)(*method_args, user=self.active_user,
                                          selected_element_id=self.selected_element_id)


class Document:
    def __init__(self, templfile):
        self._id = uuid4().int
        self.mutex = Lock()
        self.doctree = DocTree(templfile)
        self.selected_element = None

    def insert_element(self, child_element_name, child_element_id, child_element_pos, **kwargs):
        new_element = Element(name=child_element_name, doctree=self.doctree, id=child_element_id)
        with self.mutex:
            self.doctree.getElementById(kwargs["selected_element_id"]).insertChild(new_element, child_element_pos)

    def get(self, action, path=None, **kwargs):
        with self.mutex:
            if action == "element_xml":
                return self.doctree.getElementById(kwargs["selected_element_id"]).getXML()
            elif action == "element_text":
                return self.doctree.getElementById(kwargs["selected_element_id"]).getText()
            elif action == "element_path":
                return self.doctree.getElementByPath(path)

    # method_args = (
    #               (document_name|change_element_name|element_attr)?,
    #               (change_element_id|element_attr_value)?,
    #               (change_element_pos)?,
    #               )
    def change(self, action, *method_args, **kwargs):
        with self.mutex:
            if action == "document_name":
                self.doctree.setName(method_args[0])
            elif action == "element_update":
                new_element = Element(name=method_args[0], doctree=self.doctree, id=method_args[1])
                self.doctree.getElementById(kwargs["selected_element_id"]).updateChild(new_element, method_args[2])
            elif action == "element_attr":
                self.doctree.getElementById(kwargs["selected_element_id"]).setAttr(method_args[0], method_args[1])

    def delete(self, action, child_pos=None, **kwargs):
        with self.mutex:
            if action == "element_id":
                self.doctree.deleteElement(kwargs["selected_element_id"])
            elif action == "element_child_pos":
                self.doctree.getElementById(kwargs["selected_element_id"]).removeChild(child_pos)

    # TODO
    def export(self):
        with self.mutex:
            self.doctree.export(None, None)

    def add_user(self, **kwargs):
        with self.mutex:
            self.doctree.attach(kwargs["user"])

    def remove_user(self, **kwargs):
        with self.mutex:
            self.doctree.detach(kwargs["user"])

    def get_id(self):
        return self._id
