from UserClass import User
from DocTreeClass import DocTree

user1 = User("user", "user@metu.edu.com.tr", "User", "123456")
user2 = User("user2", "user2@metu.edu.com.tr", "User2", "123456")

templfile = {"root": 'document',
             "elements": {"document": {"attrs": [], "children": ['meta'], "occurs": '1'},
                          "meta": {"attrs": [], "children": [], "occurs": '?'}}}
doctree = DocTree(templfile)

doctree.attach(user1, lambda: print("callback called"))
doctree.attach(user2, lambda: print("callback called"))
doctree.getElementById(1)

print("Breakpoint For Debugging")