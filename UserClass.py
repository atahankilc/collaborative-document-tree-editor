import hashlib
import os
import uuid
import json
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

    # CRUD operations
    def get(self):
        objectdict = {"username": self.username,
                      "email": self.email,
                      "fullname": self.fullname,
                      "passwd": self.passwd}
        return json.dumps(objectdict)

    def update(self, username=None, email=None, fullname=None, passwd=None):
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if fullname is not None:
            self.fullname = fullname
        if passwd is not None:
            sha256 = hashlib.sha256()
            sha256.update(passwd.encode())
            self.passwd = sha256.hexdigest()

    def delete(self, username=False, email=False, fullname=False, passwd=False):
        if username is not False:
            self.username = None
        if email is not False:
            self.email = None
        if fullname is not False:
            self.fullname = None
        if passwd is not False:
            self.passwd = None

    def auth(self, plainpass):
        sha256 = hashlib.sha256()
        sha256.update(plainpass.encode())
        given_passwd = sha256.hexdigest()
        if self.passwd == given_passwd:
            self.status = User.Status.AUTHORIZED
            return True
        else:
            self.status = User.Status.UNAUTHORIZED
            return False

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

    # debugging
    def getstatus(self):
        return self.status
