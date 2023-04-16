from Enums import Status


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


def auth_required(func):
    def is_authorized(self, *arg, **kw):
        if self.status & Status.AUTHORIZED:
            ret = func(self, *arg, **kw)
            return ret
        else:
            return "UNAUTHORIZED USER: ACTION DENIED"

    return is_authorized
