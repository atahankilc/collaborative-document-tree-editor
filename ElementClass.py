import uuid
from Enums import Occurs
from Decorators import update_users


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
        self.users = doctree.users
        self.initialize_with_template()

    def getXML(self, level=0):
        xml = f"{'    ' * level}<{self.name} id='{self.id}'"

        for attr, value in self.attrs.items():
            xml += f" {attr}='{value}'"

        if not self.children and not self.text:
            return xml + "/>\n"
        xml += ">\n"

        for child in self.children:
            xml += child.getXML(level + 1)

        if self.text:
            xml += f"{'    ' * (level + 1)}{self.text}\n"

        xml += f"{'    ' * level}</{self.name}>\n"

        return xml

    def getText(self):
        if self.template.hasTextualContent:
            return self.text

    @update_users(function_name="insertChild")
    def insertChild(self, element, pos):
        child_count = self.count_child_occurrence(element.name)

        if not self.check_child_occurrence(element.name, child_count + 1):
            raise Exception("Child element cannot be inserted")

        element.parent = self
        self.children.insert(min(pos, len(self.children)), element)

    @update_users(function_name="removeChild")
    def removeChild(self, pos):
        if pos >= len(self.children):
            raise Exception("Child element does not exist")

        child = self.children[pos]
        child_count = self.count_child_occurrence(child.name)

        if not self.check_child_occurrence(child.name, child_count - 1):
            raise Exception("Child element cannot be removed")

        return self.children.pop(pos)

    @update_users(function_name="updateChild")
    def updateChild(self, element, pos):
        if pos >= len(self.children):
            raise Exception("Child element does not exist")

        old_child = self.children[pos]

        if old_child.name == element.name:
            self.children[pos] = element
        else:
            try:
                self.removeChild(pos)
            except Exception:
                raise Exception("Child element cannot be updated")
            else:
                self.insertChild(element, pos)

        return old_child

    @update_users(function_name="setAttr")
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
