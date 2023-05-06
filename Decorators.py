from Enums import Status
from threading import Thread

"""
This function iterates over all attached users of document tree and notifies them of the change 
by calling the registered callback function with the appropriate action, arguments, and keyword arguments.
"""


# TODO: change update user decorator from calling callback to putting message to queue
def update_users(function_name):
    def notify_users(func):
        def notify(users, action, args, kwargs):
            if len(users) > 0:
                for user in users:
                    users[user](user, action=action, args=args, kwargs=kwargs)

        def execute(self, *args, **kwargs):
            action = None
            if function_name == "removeChild":
                action = "Element deleted/removed"
            elif function_name == "insertChild":
                action = "Element inserted"
            elif function_name == "updateChild":
                action = "Element updated"
            elif function_name == "setAttr":
                action = "Element attribute changed"
            else:
                action = "Undefined action"
            th = Thread(target=notify, args=(self.users, action, args, kwargs))
            th.start()
            ret = func(self, *args, **kwargs)
            th.join()
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
            return "UNAUTHORIZED USER: ACTION DENIED"

    return is_authorized


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
