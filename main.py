from UserClass import User

user = User("user", "user@metu.edu.com.tr", "User", "user123456")
print(user.getstatus())

user.login()
print(user.getstatus())

user.auth("user123456")
print(user.getstatus())

token = user.login()
print(user.getstatus())

print(user.checksession(token))

user.logout()
print(user.getstatus())

print(user.checksession(token))

