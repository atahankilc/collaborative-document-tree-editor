from .Enums import Status

"""
This function iterates over all attached users of document tree and notifies them of the change 
by calling the registered callback function with the appropriate action, arguments, and keyword arguments.
"""


def update_users(function_name):
    def notify_users(func):

        def notify_everyone(users, action, args, kwargs, ret):
            if len(UserHandler.user_dict) > 0:
                for key in UserHandler.user_dict:
                    print(key)
                    if UserHandler.user_dict[key] not in users:
                        UserHandler.user_dict[key].callback(UserHandler.user_dict[key], action=action, args=args, kwargs=kwargs, ret=ret)

        def notify(users, args, kwargs, ret):
            action = None
            if function_name == "removeElement":
                action = "Element deleted/removed"
            elif function_name == "insertElement":
                action = "Element inserted"
            elif function_name == "updateElement":
                action = "Element updated"
            elif function_name == "setElementAttr":
                action = "Element attribute changed"
            elif function_name == "setText":
                action = "Element text changed"
            elif function_name == "setDocumentName":
                action = "Document name changed"
                notify_everyone(users, action, args, kwargs, ret)
            elif function_name == "newDocument":
                action = "New Document Created"
                notify_everyone(users, action, args, kwargs, ret)
            else:
                action = "Undefined action"
            if len(users) > 0:
                for user in users:
                    users[user](user, action=action, args=args, kwargs=kwargs, ret=ret)

        def execute(self, *args, **kwargs):
            ret = None
            try:
                ret = func(self, *args, **kwargs)
            except Exception as e:
                raise e
            notify(self.users, args, kwargs, ret)
            return ret

        return execute

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
            return "INVALID"

    return is_authorized


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class UserHandler:
    def __init__(self):
        self.user_dict = {}

    @staticmethod
    def add_user(user):
        UserHandler.user_dict[user.username] = user

    @staticmethod
    def remove_user(user):
        del UserHandler.user_dict[user.username]


UserHandler = UserHandler()
