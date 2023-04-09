from UserClass import User

user = User("user", "user@metu.edu.com.tr", "User", "user123456")
print(user.get())

user.update(username="other_user", fullname="Other User")
print(user.get())

user.update(email="other.user@metu.edu.tr")
print(user.get())

user.update(username="user", email="user@metu.edu.com.tr", fullname="User", passwd="123user456")
print(user.get())

user.delete(username=True, email=True)
print(user.get())

