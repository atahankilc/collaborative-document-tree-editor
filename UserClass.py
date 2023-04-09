import hashlib
import os
import uuid
from enum import Enum


class User:
    class Status(Enum):
        UNAUTHORIZED = 0
        AUTHORIZED = 1
        LOGGED_IN = 11
        LOGGED_OUT = 21

        def __and__(self, other):
            return self.value & other.value

    def __init__(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname

        # password hashing
        sha256 = hashlib.sha256()
        sha256.update(passwd.encode())
        self.passwd = sha256.hexdigest()

        # user status
        self.status = User.Status.UNAUTHORIZED
        self.token = None

    def auth(self, plainpass):
        sha256 = hashlib.sha256()
        sha256.update(plainpass.encode())
        given_passwd = sha256.hexdigest()
        if self.passwd == given_passwd:
            self.status = User.Status.AUTHORIZED
        else:
            self.status = User.Status.UNAUTHORIZED

    def auth_required(func):
        def is_authorized(self, *arg, **kw):
            if self.status & User.Status.AUTHORIZED:
                ret = func(self, *arg, **kw)
                return ret
            else:
                return "UNAUTHORIZED USER: ACTION DENIED"
        return is_authorized

    @auth_required
    def login(self):
        self.status = User.Status.LOGGED_IN
        self.token = uuid.UUID(bytes=os.urandom(16), version=4).hex
        return self.token

    # TODO
    @auth_required
    def checksession(self, token):
        if self.token == token:
            return "Valid"
        else:
            return "Invalid"

    @auth_required
    def logout(self):
        self.status = User.Status.LOGGED_OUT
        self.token = None

    # CRUD operations
    # TODO
    def get(self):
        pass

    # TODO
    def update(self):
        pass

    # TODO
    def delete(self):
        pass

    # debugging
    def getstatus(self):
        return self.status
