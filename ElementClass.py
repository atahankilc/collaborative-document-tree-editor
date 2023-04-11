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
        xml = f"<{self.name} id='{self.id}'"

        for attr, value in self.attrs.items():
            xml += f" {attr}='{value}'"

        if not self.children and not self.text:
            return xml + "/>"
        xml += ">"

        for child in self.children:
            xml += child.getXML()
        xml += self.text

        xml += f"</{self.name}>"

        return xml

    def getText(self):
        if self.template.hasTextualContent:
            return self.text

    def insertChild(self, element, pos):
        # TODO: check if element is compatible with template
        # TODO: raise exception if element is not valid

        self.children.insert(pos, element)

    def removeChild(self, pos):
        pass

    def updateChild(self, element, pos):
        pass

    def setAttr(self, attr, value):
        self.attrs[attr] = value

    def initialize_with_template(self):
        for child in self.template.children:
            child_template = self.doctree.templates[child]
            if child_template.occurs == Occurs.ONE or child_template.occurs == Occurs.ONE_MORE:
                self.insertChild(Element(child, self.doctree), len(self.children))