from Enums import Status

"""
This function iterates over all attached users of document tree and notifies them of the change 
by calling the registered callback function with the appropriate action, arguments, and keyword arguments.
"""


def update_users(function_name):
    def notify_users(func):
        def notify(self, *arg, **kw):
            if function_name == "removeChild":
                for user in self.users:
                    self.users[user](action="Element deleted/removed", arg=arg, kw=kw)
            elif function_name == "insertChild":
                for user in self.users:
                    self.users[user](action="Element inserted", arg=arg, kw=kw)
            elif function_name == "updateChild":
                for user in self.users:
                    self.users[user](action="Element updated", arg=arg, kw=kw)
            elif function_name == "setAttr":
                for user in self.users:
                    self.users[user](action="Element attribute changed", arg=arg, kw=kw)
            return func(self, *arg, **kw)

        return notify

    return notify_users


"""
This function checks whether the user is authorized and returns an error message if not. 
Otherwise, it calls the original function with the given arguments and returns its return value.
"""


def auth_required(func):
    def is_authorized(self, *arg, **kw):
        if self.status & Status.AUTHORIZED:
            ret = func(self, *arg, **kw)
            return ret
        else:
            return "UNAUTHORIZED USER: ACTION DENIED"

    return is_authorized


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
