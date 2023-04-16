import DocTreeClass
import ElementClass
import UserClass


#################################
#                               #
# USER CLASS DEMO APP FUNCTIONS #
#                               #
#################################

def create_user(user_name="demo_user", email="demo_user@metu.edu.tr", fullname="demo user", passwd="123"):
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
    demo_user = create_user()
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

demo_user_doctree = create_user(user_name="demo_user_doctree", email="demo_user_doctree@metu.edu.tr",
                                fullname="demo user doctree", passwd="123doctree")


def demo_callback_doctree(**kw):
    print("{}. args = {}, kwargs = {}".format(kw["action"], kw["arg"], kw["kw"]))


def create_doctree(templfile=None):
    if templfile is None:
        templfile = demo_templfile_doctree
    doctree_object = DocTreeClass.DocTree(templfile)
    return doctree_object


def print_doctree(doctree_object):
    print("\t***** DocTree Object *****\n\tname = {}\n\tusers = {}\n\tdoctree XML = \n{}"
          "\t**************************".format(doctree_object.name, doctree_object.users,
                                                doctree_object.root.getXML()))


def setname_doctree(doctree_object, name="demo_doctree"):
    doctree_object.setName(name)
    print_doctree(doctree_object)


def getelementbyid_doctree(doctree_object, id=0):
    return doctree_object.getElementById(id)


def getelementbypath_doctree(doctree_object, path="document/meta"):
    return doctree_object.getElementByPath(path)


def deleteelement_doctree(doctree_object, id=None):
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
    doctree_object.attach(user, callback)
    print_doctree(doctree_object)


def detach_doctree(doctree_object, user=demo_user_doctree):
    doctree_object.detach(user)
    print_doctree(doctree_object)


def doctree_class_test_run():
    print("----- DocTree Class Tests -----")
    demo_doctree = create_doctree()
    print("- DocTree Class constructor -")
    print_doctree(demo_doctree)
    print("- DocTree Class setName -")
    setname_doctree(doctree_object=demo_doctree)
    print("- DocTree Class getElementById -")
    print(getelementbyid_doctree(doctree_object=demo_doctree))
    print("- DocTree Class getElementByPath -")
    print(getelementbypath_doctree(doctree_object=demo_doctree))
    print("- DocTree Class attach -")
    attach_doctree(doctree_object=demo_doctree)
    print("- DocTree Class deleteElement / User Will Be Notified -")
    deleteelement_doctree(doctree_object=demo_doctree)
    print("- DocTree Class detach -")
    detach_doctree(doctree_object=demo_doctree)
    print("- DocTree Class deleteElement / No User Will Be Notified -")
    deleteelement_doctree(doctree_object=demo_doctree)
    print("-------------------------------")


####################################
#                                  #
# ELEMENT CLASS DEMO APP FUNCTIONS #
#                                  #
####################################

# TODO
