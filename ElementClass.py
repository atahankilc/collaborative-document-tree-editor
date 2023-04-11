import uuid
from Enums import Occurs


class Element:
    def __init__(self, name, doctree, id=None):
        self.name = name
        self.doctree = doctree
        self.id = uuid.uuid4() if id is None else id
        self.template = self.doctree.templates[name]
        self.children = []
        self.attrs = {}
        self.text = ""
        self.initialize_with_template()

    def getXML(self):
        pass

    def getText(self):
        pass

    def insertChild(self, element, pos):
        pass

    def removeChild(self, pos):
        pass

    def updateChild(self, element, pos):
        pass

    def setAttr(self, attr, value):
        pass

    def initialize_with_template(self):
        for child in self.template.children:
            child_template = self.doctree.templates[child]
            if child_template.occurs == Occurs.ONE or child_template.occurs == Occurs.ONE_MORE:
                self.insertChild(Element(child, self.doctree), len(self.children))