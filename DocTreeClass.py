from ElementClass import Element
from Enums import Occurs


class DocTree:
    # importfile will be implemented in Phase-2
    def __init__(self, templfile, importfile=None):
        self.name = "Unnamed"
        self.templates = DocTree.generateTemplates(templfile["elements"])
        self.element = Element(templfile["root"], self, 0)
        self.users = {}

    def setName(self, name):
        self.name = name

    def getElementById(self, id):
        pass

    def getElementByPath(self, path):
        pass

    def deleteElement(self, id):
        pass

    def attach(self, user, callback):
        self.users[user] = callback

    def detach(self, user):
        self.users.pop(user)

    # export method will be implemented in Phase-2
    def export(self, exptype, filename):
        pass

    @staticmethod
    def generateTemplates(elements):
        templates = {}
        for key in elements:
            templates[key] = DocTree.Template(elements[key]["attrs"],
                                              elements[key]["children"],
                                              elements[key]["occurs"])
        for key in templates:
            templates[key].changeChildrenArrToChildrenDict(templates)
        return templates

    class Template:
        def __init__(self, attrs, children, occurs):
            self.attrs = attrs
            self.children = children
            self.hasTextualContent = True if 'text' in children else False
            self.occurs = Occurs.from_str(occurs)

        def changeChildrenArrToChildrenDict(self, templates):
            children_dict = {}
            for child in self.children:
                children_dict[child] = templates[child]
            self.children = children_dict
