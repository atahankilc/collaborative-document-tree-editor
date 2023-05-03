from DocTreeClass import DocTree
from ElementClass import Element
from threading import *
from uuid import uuid4


class Document:
    def __init__(self, templfile):
        self._id = uuid4().int
        self.mutex = Lock()
        self.doctree = DocTree(templfile)
        self.selected_element = None

    def change_document_name(self, name):
        with self.mutex:
            self.doctree.setName(name)

    def get_element_Text(self, id):
        with self.mutex:
            self.doctree.getElementById(id).getText()

    def insert_element(self, parent_id, element_name, element_pos, element_id = None):
        element = Element(name=element_name, doctree=self.doctree, id=element_id)
        with self.mutex:
            self.doctree.getElementById(parent_id).insertChild(element, element_pos)

    # TODO: merge delete_element and remove_element
    def delete_element(self, id):
        with self.mutex:
            self.doctree.deleteElement(id)
    def remove_element(self, parent_id, pos):
        with self.mutex:
            self.doctree.getElementById(parent_id).removeChild(pos)

    # TODO
    def change_element(self):
        # updateElement
        # setAttr
        pass

    # TODO: merge get_XML_by_path and get_element_XML
    def get_XML_by_path(self, path):
        with self.mutex:
            return self.doctree.getElementByPath(path)
    def get_element_XML(self, id):
        with self.mutex:
            self.doctree.getElementById(id).getXML()

    # TODO
    def export(self):
        with self.mutex:
            self.doctree.export(None, None)

    def add_user(self, user):
        with self.mutex:
            self.doctree.attach(user)

    def remove_user(self, user):
        with self.mutex:
            self.doctree.detach(user)

    def get_id(self):
        return self._id
