from UserClass import User
from ElementClass import Element
from DocTreeClass import DocTree

user = User("user", "user@metu.edu.com.tr", "User", "user123456")

templfile = {"root": 'document',
             "elements": {"document": {"attrs": [], "children": ['meta'], "occurs": '1'},
                          "meta": {"attrs": [], "children": [], "occurs": '?'}}}
doctree = DocTree(templfile)

print("Breakpoint For Debugging")
