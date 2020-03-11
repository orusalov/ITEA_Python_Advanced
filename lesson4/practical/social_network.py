from datetime import date, timedelta
from random import randint

class AlreadyHasAdmin(Exception):
    pass


class User:

    admin_counter = 0

    def __init__(self, username, password, is_admin=False):
        self._username = username.lower()
        self._password = password
        self._is_admin = is_admin
        self._registration_date = date.today() - timedelta(randint(0,1000))

        if is_admin and not admin_counter:
            admin_counter += 1
        else:
            raise AlreadyHasAdmin('System already has admin')

    @property
    def username(self):
        return self._username

    @property
    def is_admin(self):
        return self.is_admin




    def check_password(self, value):
        return True if self._password == value else False


class Registration:

