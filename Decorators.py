from Enums import Status


def update_users(function_name):
    def notify_users(func):
        def notify(self, *arg, **kw):
            for user in self.users:
                print("update_users Decorator Called for {}. Update Information: func={} *arg={} **kw={}".format(
                    user.username, function_name, arg, kw))
                self.users[user]()
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
