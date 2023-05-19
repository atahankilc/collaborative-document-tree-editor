import uuid
from comman_utils.Enums import Occurs
from comman_utils.Decorators import update_users


class Element:
    def __init__(self, name, doctree, id=None):
        """
        Constructor for the Element class

        @param name: (str) the name of the element
        @param doctree: (DocTree) the DocTree object that this element belongs to
        @param id: (int) the unique ID of the element (If not provided, a new unique ID will be generated using uuid)

        @note The constructor initializes the element with the template by inserting all necessary
        children by calling the initialize_with_template method
        """

        self.name = name
        self.doctree = doctree
        self.id = uuid.uuid4().int if id is None else id
        if name not in self.doctree.templates:
            raise Exception("Name is not valid")
        self.template = self.doctree.templates[name]
        self.children = []
        self.attrs = {}
        self.text = ""
        self.parent = None
        self.users = doctree.users
        self.initialize_with_template()

    def getXML(self, level=0):
        """
        Returns the XML representation of the element

        @param level: (int) the level of the element in the tree (used for indentation)
        @return: the XML representation of the element as a string
        """

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
        """
        Checks if the element has textual content from the template and returns the text content

        @return: the text content of the element as a string
        """

        if self.template.hasTextualContent:
            return self.text

    @update_users(function_name="insertElement")
    def insertChild(self, element, pos):
        """
        Inserts a child element at the specified position.

        @param element: (Element) the child element to insert
        @param pos: (int) the position to insert the child element at

        @note Before inserting the child element, the method checks if the child element is allowed to be inserted
        by checking the template of the element. If the child element is allowed to be inserted,
        the method inserts the child element at the given position and updates the users of the DocTree object.
        If the child element is not allowed to be inserted, an exception is raised.

        @note If the given position is not a valid position (a negative number), an exception is raised.

        @note If the given position is greater than the number of children, the child element is inserted at the end.
        """
        self._insert(element, pos)

    def _insert(self, element, pos):
        if pos < 0:
            raise Exception("Position is not valid")

        child_count = self.count_child_occurrence(element.name)

        # check if the resulting element with the inserted child is valid according to the template
        if not self.check_child_occurrence(element.name, child_count + 1):
            raise Exception("Child element cannot be inserted")

        element.parent = self
        self.children.insert(min(pos, len(self.children)), element)

    @update_users(function_name="removeElement")
    def removeChild(self, pos):
        """
        Removes the child element at the specified position.

        @param pos: (int) the position of the child element to remove
        @return: the removed element

        @note Before removing the child element, the method checks if the child element is allowed to be removed
        since the resulting element must still be valid. If the child element is allowed to be removed,
        the method removes the child element at the given position and updates the users of the DocTree object.
        If the child element is not allowed to be removed, an exception is raised.

        @note If the given position is not a valid position (larger than number of children or negative number),
        an exception is raised.
        """
        return self._remove(pos)

    def _remove(self, pos):
        if pos >= len(self.children) or pos < 0:
            raise Exception("Position is not valid")

        child = self.children[pos]
        child_count = self.count_child_occurrence(child.name)

        # check if the resulting element with the removed child is valid according to the template
        if not self.check_child_occurrence(child.name, child_count - 1):
            raise Exception("Child element cannot be removed")

        return self.children.pop(pos)

    @update_users(function_name="updateElement")
    def updateChild(self, element, pos):
        """
        Replaces the child element at the specified position with the given element.

        @param element: (Element) the element to replace the child element with
        @param pos: (int) the position of the child element to replace
        @return: (Element) the replaced element

        @note Before replacing the child element, the method checks if the child element is allowed to be replaced. If
        the child to be removed has the same type as the child to be inserted, the method replaces the child element.
        Otherwise, the method removes the child element at the given position and inserts the new child element at the
        same position. The checks for this case are already implemented in the removeChild and insertChild methods.
        If the remove operation is successful but the insert operation raises an exception, the method inserts the
        removed child element back at the same position. If the child element is not allowed to be replaced,
        an exception is raised.

        @note If the given position is not a valid position (negative number or larger than number of children),
        an exception is raised.
        """

        if pos >= len(self.children) or pos < 0:
            raise Exception("Position is not valid")

        old_child = self.children[pos]

        if old_child.name == element.name:
            self.children[pos] = element
        else:
            try:
                self._remove(pos)
            except Exception:
                raise Exception("Child element cannot be updated")
            else:
                try:
                    self._insert(element, pos)
                except Exception:
                    self._insert(old_child, pos)
                    raise Exception("Child element cannot be updated")

        return old_child

    @update_users(function_name="setElementAttr")
    def setAttr(self, attr, value):
        """
        Sets the value of the attribute with the given name as a key value pair in the attrs dictionary.

        @param attr: (str) the name of the attribute
        @param value: the value of the attribute
        """

        self.attrs[attr] = value

    def traverse(self, func):
        """
        Traverses the element and its children and applies the given function to each element. (pre-order traversal)

        @param func: (function) the function to apply to each element
        """

        func(self)
        for child in self.children:
            child.traverse(func)

    def initialize_with_template(self):
        """
        Initializes the element with the template. This method is called when the element is created.

        @note To find the required children, the method checks the template of the element and inserts the children
        with occurrence requirements of ONE or ONE_MORE.

        @note Since this method is called upon creation of the element, the created elements are always valid.
        """

        for child in self.template.children:
            child_template = self.doctree.templates[child]
            if child_template.occurs == Occurs.ONE or child_template.occurs == Occurs.ONE_MORE:
                self.insertChild(Element(child, self.doctree), len(self.children))

    def count_child_occurrence(self, child_name):
        """
        Counts the number of children with the given name.

        @param child_name: (str) the name of the child element to count
        @return: (int) the number of children with the given name
        """

        count = 0
        for child in self.children:
            if child.name == child_name:
                count += 1
        return count

    def check_child_occurrence(self, child_name, child_count):
        """
        Checks if the given number of children with the given name is allowed based on the occurrence
        requirements of the child element in the template.

        @param child_name: (str) the name of the child element to check
        @param child_count: (int) the number of children with the given name to check
        @return: (bool) True if the given number of children with the given name is allowed, False otherwise
        """

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
