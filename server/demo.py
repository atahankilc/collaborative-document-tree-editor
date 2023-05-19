import UserClass
import DocTreeClass
import ElementClass


#################################
#                               #
# USER CLASS DEMO APP FUNCTIONS #
#                               #
#################################

def constructor_user(user_name="demo_user", email="demo_user@metu.edu.tr", fullname="demo user", passwd="123"):
    user_object = UserClass.User(user_name, email, fullname, passwd)
    return user_object


def get_user(user_object):
    print(user_object.get())


def update_user(user_object, user_name="demo_user_updated", email="demo_user_updated@metu.edu.tr",
                fullname="demo user updated", passwd="123updated"):
    user_object.update(user_name, email, fullname, passwd)
    get_user(user_object)


def delete_user(user_object, user_name=True, email=True, fullname=True, passwd=True):
    user_object.delete(user_name, email, fullname, passwd)
    get_user(user_object)


def user_class_test_run():
    print("----- User Class Tests -----")
    demo_user = constructor_user()
    print("- User Class constructor -")
    print(demo_user)
    print("- User Class get -")
    get_user(user_object=demo_user)
    print("- User Class update -")
    update_user(user_object=demo_user)
    print("- User Class delete -")
    delete_user(user_object=demo_user)
    print("----------------------------")


####################################
#                                  #
# DOCTREE CLASS DEMO APP FUNCTIONS #
#                                  #
####################################

demo_templfile_doctree = {"root": 'document',
                          "elements": {
                              "document": {"attrs": [], "children": ['meta', 'abstract'], "occurs": '1'},
                              "meta": {"attrs": [], "children": ['author', 'date', 'title'], "occurs": '1'},
                              "abstract": {"attrs": [], "children": [], "occurs": '?'},
                              "author": {"attrs": [], "children": [], "occurs": '?'},
                              "date": {"attrs": [], "children": [], "occurs": '?'},
                              "title": {"attrs": [], "children": [], "occurs": '1'}}
                          }

demo_user_doctree = constructor_user(user_name="demo_user_doctree", email="demo_user_doctree@metu.edu.tr",
                                     fullname="demo user doctree", passwd="123doctree")


def demo_callback_doctree(**kw):
    print("{}. args = {}, kwargs = {}".format(kw["action"], kw["arg"], kw["kw"]))


def constructor_doctree(templfile=None):
    if templfile is None:
        templfile = demo_templfile_doctree
    doctree_object = DocTreeClass.DocTree(templfile)
    return doctree_object


def print_doctree(doctree_object):
    print("\t***** DocTree Object *****\n\tname = {}\n\tusers = {}\n\tdoctree XML = \n{}"
          "\t**************************".format(doctree_object.name, doctree_object.users,
                                                doctree_object.root.getXML()))


def setName_doctree(doctree_object, name="demo_doctree"):
    doctree_object.setName(name)
    print_doctree(doctree_object)


def getElementById_doctree(doctree_object, id=0):
    return doctree_object.getElementById(id)


def getElementByPath_doctree(doctree_object, path="document"):
    return doctree_object.getElementByPath(path)


def deleteElement_doctree(doctree_object, id=None):
    if id is None:
        demo_element_doctree = ElementClass.Element("abstract", doctree_object, 1)
        document_element = doctree_object.getElementById(0)
        document_element.insertChild(demo_element_doctree, 1)
        print("\tid is not specified, dummy element \"abstract\" is added.")
        print_doctree(doctree_object)
        doctree_object.deleteElement(1)
        print("\tdummy element is deleted.")
        print_doctree(doctree_object)
    else:
        doctree_object.deleteElement(id)
        print_doctree(doctree_object)


def attach_doctree(doctree_object, user=demo_user_doctree, callback=demo_callback_doctree):
    doctree_object.attach(user)
    print_doctree(doctree_object)


def detach_doctree(doctree_object, user=demo_user_doctree):
    doctree_object.detach(user)
    print_doctree(doctree_object)


def doctree_class_test_run():
    print("----- DocTree Class Tests -----")
    demo_doctree = constructor_doctree()
    print("- DocTree Class constructor -")
    print_doctree(demo_doctree)
    #print("- DocTree Class setName -")
    #setName_doctree(doctree_object=demo_doctree)
    #print("- DocTree Class getElementById -")
    #print(getElementById_doctree(doctree_object=demo_doctree))
    #print("- DocTree Class getElementByPath -")
    #print(getElementByPath_doctree(doctree_object=demo_doctree))
    print("- DocTree Class attach -")
    attach_doctree(doctree_object=demo_doctree)
    print("- DocTree Class deleteElement / User Will Be Notified -")
    deleteElement_doctree(doctree_object=demo_doctree)
    #print("- DocTree Class detach -")
    #detach_doctree(doctree_object=demo_doctree)
    #print("- DocTree Class deleteElement / No User Will Be Notified -")
    #deleteElement_doctree(doctree_object=demo_doctree)
    #print("-------------------------------")


####################################
#                                  #
# ELEMENT CLASS DEMO APP FUNCTIONS #
#                                  #
####################################

def demo_callback_element(**kw):
    print("{}. args = {}, kwargs = {}".format(kw["action"], kw["arg"], kw["kw"]))


demo_templfile_element = {"root": 'document',
                          "elements": {
                              "document": {"attrs": [], "children": ['meta'], "occurs": '1'},
                              "meta": {"attrs": [], "children": ['demo_element_1'], "occurs": '1'},
                              "demo_element_1": {"attrs": [],
                                                 "children": ['demo_element_2', 'demo_element_3', 'demo_element_4'],
                                                 "occurs": '?'},
                              "demo_element_2": {"attrs": [], "children": ['text'], "occurs": '+'},
                              "demo_element_3": {"attrs": [], "children": [], "occurs": '?'},
                              "demo_element_4": {"attrs": [], "children": [], "occurs": '*'},
                              "demo_element_5": {"attrs": [], "children": [], "occurs": '*'}}
                          }

demo_user_element = UserClass.User("demo_user", "demo_user@metu.edu.tr", "demo user", "123")
demo_doctree_element = DocTreeClass.DocTree(demo_templfile_element)
demo_doctree_element.attach(demo_user_element)


def constructor_element(name="demo_element_1", doctree=demo_doctree_element, id="1"):
    element_object = ElementClass.Element(name, doctree, id)
    return element_object


def print_element(element_object):
    print("\t***** Element Object *****\n\tname = {}\n\tid = {}\n\tdoctree = {}\n\tchildren = {}\n\tattributes = {}\n"
          "\t**************************".format(element_object.name, element_object.id,
                                                element_object.doctree,
                                                element_object.children,
                                                element_object.attrs))


def getXML_element(element_object):
    print(element_object.getXML())


def getText_element(element_object):
    return element_object.getText()


def insertChild_element(element_object, pos, child_element=None):
    if child_element is None:
        child_element = ElementClass.Element("demo_element_3", demo_doctree_element, 3)
        element_object.insertChild(child_element, pos)
    else:
        element_object.insertChild(child_element, pos)
    getXML_element(element_object)


def updateChild_element(element_object, pos, child_element=None):
    if child_element is None:
        child_element = ElementClass.Element("demo_element_4", demo_doctree_element, 4)
        print("returned element = ", element_object.updateChild(child_element, pos))
    else:
        print("returned element = ", element_object.updateChild(child_element, pos))
    getXML_element(element_object)


def removeChild_element(element_object, pos):
    print("returned element = ", element_object.removeChild(pos))
    getXML_element(element_object)


def setAttr_element(element_object, attr="demo_attr", value=0):
    element_object.setAttr(attr, value)
    getXML_element(element_object)


def element_class_normal_test_run():
    print("----- Element Class Tests -----")
    demo_element = constructor_element()
    print("- Element Class constructor -")
    print_element(demo_element)
    print("- Element Class getXML -")
    getXML_element(demo_element)
    print("- Element Class insertChild -")
    insertChild_element(demo_element, 0)
    print("- Element Class updateChild -")
    updateChild_element(demo_element, 0)
    print("- Element Class removeChild -")
    removeChild_element(demo_element, 0)
    print("- Element Class setAttr -")
    setAttr_element(demo_element)
    print("-------------------------------")


def element_class_incorrect_element_name():
    print("----- Element Class Incorrect Element Name -----")
    constructor_element("no_template_with_this_name")
    print("------------------------------------------------")


def element_class_insert_nonchild_element():
    print("----- Element Class Insert Nonchild Element -----")
    demo_element = constructor_element()
    child_element = constructor_element(name="demo_element_5")
    insertChild_element(demo_element, child_element=child_element, pos=0)
    print("-------------------------------------------------")


def element_class_insert_incorrect_count():
    print("----- Element Class Insert Incorrect Count-----")
    demo_element = constructor_element()
    child_element_1 = constructor_element(name="demo_element_3")
    child_element_2 = constructor_element(name="demo_element_3")
    insertChild_element(demo_element, child_element=child_element_1, pos=0)
    insertChild_element(demo_element, child_element=child_element_2, pos=0)
    print("-----------------------------------------------")


def element_class_remove_incorrect_count():
    print("----- Element Class Remove Incorrect Count-----")
    demo_element = constructor_element()
    removeChild_element(demo_element, pos=0)
    print("-----------------------------------------------")


def element_class_update_incorrect_count():
    print("----- Element Class Update Incorrect Count-----")
    demo_element = constructor_element()
    child_element = constructor_element(name="demo_element_3")
    updateChild_element(demo_element, child_element=child_element, pos=0)
    print("-----------------------------------------------")


def element_class_getText():
    print("----- Element Class getText -----")
    demo_element = constructor_element(name="demo_element_2")
    print(getText_element(demo_element))
    print("---------------------------------")


def element_class_incorrect_getText():
    print("----- Element Class Incorrect getText -----")
    demo_element = constructor_element(name="demo_element_5")
    print(getText_element(demo_element))
    print("-------------------------------------------")


# DocumentInstancePerUser test
# class B:
#     def method_1(self, arg1, **kwargs):
#         print(arg1, kwargs)
#     def method_2(self, *args, **kwargs):
#         print(kwargs)
# class A:
#     def __init__(self):
#         self.obj = B()
#     def __getattr__(self, item):
#         return getattr(self.obj, item)
#     def get_method(self, method_name, *method_args):
#         return getattr(self, method_name)(*method_args, additional_arg="additional_arg")
# a = A()
# a.get_method("method_1", "arg1")
# a.get_method("method_2")
