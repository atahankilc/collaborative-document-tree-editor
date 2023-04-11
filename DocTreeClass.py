from Decorators import update_users
from ElementClass import Element
from Enums import Occurs


class DocTree:
    # importfile will be implemented in Phase-2
    def __init__(self, templfile, importfile=None):
        self.name = "Unnamed"
        self.templates = DocTree.generate_templates(templfile["elements"])
        self.root = Element(templfile["root"], self, 0)
        self.users = {}
        self.searched_element = None

    def setName(self, name):
        self.name = name

    def getElementById(self, id):
        self.search_element(id=id)
        return self.searched_element

    def getElementByPath(self, path):
        path_array = path.split("/")
        path_array.reverse()
        self.search_element(path_array=path_array)
        if self.searched_element is not None:
            # TODO: return XML content
            return self.searched_element

    def deleteElement(self, id):
        self.search_element(id=id)
        if self.searched_element is not None:
            for index, child in enumerate(self.searched_element.parent.children):
                if child == self.searched_element:
                    self.searched_element.parent.children.pop(index)

    def attach(self, user, callback):
        self.users[user] = callback

    def detach(self, user):
        self.users.pop(user)

    # export method will be implemented in Phase-2
    def export(self, exptype, filename):
        pass

    def search_element(self, id = None, path_array=None):
        def id_search(element):
            if element.id == id:
                element.doctree.searched_element = element

        def path_search(element):
            current_element = element
            is_correct_path = True
            for item in path_array:
                if current_element is None or current_element.name != item:
                    is_correct_path = False
                    break
                current_element = current_element.parent
            if is_correct_path:
                element.doctree.searched_element = element

        self.searched_element = None
        if id is not None:
            self.root.traverse(id_search)
        elif path_array is not None:
            self.root.traverse(path_search)

    @staticmethod
    def generate_templates(elements):
        templates = {}
        for key in elements:
            templates[key] = DocTree.Template(elements[key]["attrs"],
                                              elements[key]["children"],
                                              elements[key]["occurs"])
        for key in templates:
            templates[key].change_children_arr_to_children_dict(templates)
        return templates

    class Template:
        def __init__(self, attrs, children, occurs):
            self.attrs = attrs
            self.children = children
            self.hasTextualContent = True if 'text' in children else False
            self.occurs = Occurs.from_str(occurs)

        def change_children_arr_to_children_dict(self, templates):
            children_dict = {}
            for child in self.children:
                children_dict[child] = templates[child]
            self.children = children_dict
