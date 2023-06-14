import os
import uuid
import json
import hashlib
from threading import Lock, Condition
from comman_utils.Decorators import auth_required
from comman_utils.Enums import Status


class User:
    def __init__(self, username, email, fullname, passwd):
        """
        User class constructor

        @param username: (str) username of the user
        @param email: (str) email of the user
        @param fullname: (str) full name of the user
        @param passwd: (str) password of the user

        @note The password is hashed using SHA256.
        """

        self.username = username
        self.email = email
        self.fullname = fullname

        # password hashing
        sha256 = hashlib.sha256()
        sha256.update(passwd.encode())
        self.passwd = sha256.hexdigest()

        # user status
        self.status = Status.UNAUTHORIZED
        self.token = None

        # notification
        self.callback = User._callback
        self.message_queue = []
        self.mutex = Lock()
        self.cond = Condition(self.mutex)
        self.notification_handler_thread_flag = True

    # CRUD operations
    def get(self):
        """
        @return: (dict) a dictionary containing the user's information
        """

        objectdict = {"username": self.username,
                      "email": self.email,
                      "fullname": self.fullname,
                      "passwd": self.passwd}
        return json.dumps(objectdict)

    def update(self, username=None, email=None, fullname=None, passwd=None):
        """
        Updates the user's information

        @param username: (str) new username of the user
        @param email: (str) new email of the user
        @param fullname: (str) new name of the user
        @param passwd: (str) new password of the user
        """

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
        """
        Deletes the user's information

        @param username: (bool) if not False, username will be deleted
        @param email: (bool) if not False, email will be deleted
        @param fullname: (bool) if not False, fullname will be deleted
        @param passwd: (bool) if not False, passwd will be deleted
        """

        if username is not False:
            self.username = None
        if email is not False:
            self.email = None
        if fullname is not False:
            self.fullname = None
        if passwd is not False:
            self.passwd = None

    def auth(self, plainpass):
        """
        Authenticates the user and sets auth status

        @param plainpass: (str) plain text password
        @return: (bool) True if the password is correct, False otherwise

        @note The given plain text password is hashed and compared with the stored password.
        """

        sha256 = hashlib.sha256()
        sha256.update(plainpass.encode())
        given_passwd = sha256.hexdigest()
        if self.passwd == given_passwd:
            self.status = Status.AUTHORIZED
            return True
        else:
            self.status = Status.UNAUTHORIZED
            return False

    @auth_required
    def login(self):
        """
        Logs the user in, generates a token, and sets status to LOGGED_IN

        @return: (str) token of the user
        """
        self.status = Status.LOGGED_IN
        self.token = uuid.UUID(bytes=os.urandom(16), version=4).hex
        return self.token

    # TODO
    @auth_required
    def checksession(self, token):
        """
        Checks if the user token is valid

        @param token: (str) token of the user
        @return: (str) "Valid" if the token is valid, "Invalid" otherwise
        """

        if self.token == token:
            return "Valid"
        else:
            return "Invalid"

    @auth_required
    def logout(self):
        """
        Logs the user out, deletes the token, and sets status to LOGGED_OUT
        """

        self.status = Status.LOGGED_OUT
        self.token = None

    # debugging
    def getstatus(self):
        """
        @return: (Status) authentication status of the user
        """

        return self.status

    def _callback(self, **message):
        self.notification_handler_thread_flag = False
        with self.mutex:
            self.message_queue.append(
                "{} - {}. args = {}, kwargs = {}, ret = {}".format(self.username, message["action"], message["args"], message["kwargs"],
                                                              message["ret"]))
            self.notification_handler_thread_flag = True
            self.cond.notifyAll()
