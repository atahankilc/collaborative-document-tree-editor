import uuid
from Enums import Occurs


class Element:
    def __init__(self, name, doctree, id=None):
        self.name = name
        self.doctree = doctree
        self.id = uuid.uuid4().int if id is None else id
        self.template = self.doctree.templates[name]
        self.children = []
        self.attrs = {}
        self.text = ""
        self.parent = None
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
        child_count = self.count_child_occurrence(element.name)

        if not self.check_child_occurrence(element.name, child_count + 1):
            raise Exception("Child element cannot be inserted")

        element.parent = self
        self.children.insert(pos, element)

    def removeChild(self, pos):
        child = self.children[pos]
        child_count = self.count_child_occurrence(child.name)

        if not self.check_child_occurrence(child.name, child_count - 1):
            raise Exception("Child element cannot be removed")

        return self.children.pop(pos)

    def updateChild(self, element, pos):
        old_child = self.removeChild(pos)
        self.insertChild(element, pos)
        return old_child

    def setAttr(self, attr, value):
        self.attrs[attr] = value

    def traverse(self, func):
        func(self)
        for child in self.children:
            child.traverse(func)

    def initialize_with_template(self):
        for child in self.template.children:
            child_template = self.doctree.templates[child]
            if child_template.occurs == Occurs.ONE or child_template.occurs == Occurs.ONE_MORE:
                self.insertChild(Element(child, self.doctree), len(self.children))

    def count_child_occurrence(self, child_name):
        count = 0
        for child in self.children:
            if child.name == child_name:
                count += 1
        return count

    def check_child_occurrence(self, child_name, child_count):
        if child_name not in self.template.children:
            return False

        child_template = self.doctree.templates[child_name]

        if child_template.occurs == Occurs.ZERO and child_count != 0:
            return False
        elif child_template.occurs == Occurs.ONE and child_count != 1:
            return False
        elif child_template.occurs == Occurs.ONE_MORE and child_count < 1:
            return False
        elif child_template.occurs == Occurs.ZERO_ONE and child_count > 1:
            return False

        return True
