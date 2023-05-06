from Decorators import update_users
from ElementClass import Element
from Enums import Occurs


class DocTree:
    # importfile will be implemented in Phase-2
    def __init__(self, templfile, importfile=None):
        """
        Constructor for the DocTree class

        @param templfile: (dict) template of the document tree
        @param importfile: the file to be imported into the document tree

        @note The constructor initializes the document tree with the root element. Since Element class constructor
        initializes the element based on the template by inserting all required children, the document tree
        will have all the required elements.
        """

        self.name = "Unnamed"
        self.templates = DocTree.generate_templates(templfile["elements"])
        self.users = {}
        self.searched_element = None
        self.root = Element(templfile["root"], self, 0)

    def setName(self, name):
        """
        Sets the name of the document tree
        @param name: (str) the name of the document tree
        """

        self.name = name

    def getElementById(self, id):
        """
        Returns the element with the given ID

        @param id: (int) the ID of the searched element
        @return: searched element if found, None otherwise
        """

        self.search_element(id=id)
        return self.searched_element

    def getElementByPath(self, path):
        """
        Returns the element with the given path

        @param path: (str) the path of the searched element
        @return: XML representation of the searched element if found
        """

        path_array = path.split("/")
        path_array.reverse()
        self.search_element(path_array=path_array)
        if self.searched_element is not None:
            return self.searched_element.getXML()

    def deleteElement(self, id):
        """
        Deletes the element with the given ID

        @param id: (int) the ID of the element to be deleted
        """

        self.search_element(id=id)
        if self.searched_element is not None:
            for index, child in enumerate(self.searched_element.parent.children):
                if child == self.searched_element:
                    self.searched_element.parent.removeChild(index)

    def attach(self, user):
        """
        Attaches a user to the document tree

        @param user: (User) the user to be attached
        """

        self.users[user] = user.callback

    def detach(self, user):
        """
        Detaches a user from the document tree

        @param user: (User) the user to be detached
        """

        del self.users[user]

    # TODO
    def export(self, exptype, filename):
        pass

    def search_element(self, id=None, path_array=None):
        """
        Searches the element with the given ID or path

        @param id: (int) ID of the element to be searched
        @param path_array: (list) path of the element to be searched

        @note The function searches the element with the given ID or path and sets the searched_element
        attribute of the document tree to the found element.

        @note Based on the type of the search, the function calls the corresponding search function (id_search or
        path_search). These functions are given as parameters to the traverse function of the root element. The
        traverse function traverses the document tree recursively and calls the given function on each element.
        """

        def id_search(element):
            """
            Searches the element with the given ID

            @param element: (Element) the element to be searched
            """

            if element.id == id:
                element.doctree.searched_element = element

        def path_search(element):
            """
            Searches the element with the given path

            @param element: (Element) the element to be searched

            @note The function traverses the path array and checks if the element has the same name as the current
            item in the path array. If the element has the same name, the function sets the current element to the
            parent of the current element and continues the search. If the element does not have the same name,
            the function breaks the loop and continues the search with the next element.
            """

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
        """
        Generates the template of the document tree as a dictionary

        @param elements: (dict) the elements in the template of the document tree
        @return: (dict) the templates of the document tree
        """

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
            """
            Constructor for the Template class

            @param attrs:
            @param children:
            @param occurs:
            """

            self.attrs = attrs
            self.children = children
            self.hasTextualContent = True if 'text' in children else False
            self.occurs = Occurs.from_str(occurs)

        def change_children_arr_to_children_dict(self, templates):
            """
            Converts the children array to a dictionary

            @param templates: (dict) the templates of the document tree
            """

            children_dict = {}
            for child in self.children:
                if child != "text":
                    children_dict[child] = templates[child]
            self.children = children_dict
