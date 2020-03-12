from datetime import date, timedelta
from random import randint

class AdminCounterException(Exception):
    pass

class UserAlreadyExists(Exception):
    pass

class WrongUsernameOrPassword(Exception):
    pass

class User:

    admin_counter = 0

    def __init__(self, username, password, is_admin=False):
        self._username = username.lower()
        self._password = password
        self._is_admin = is_admin
        self._registration_date = date.today() - timedelta(randint(0,1000))

        if is_admin and not User.admin_counter:
            User.admin_counter += 1
        elif is_admin and User.admin_counter:
            raise AdminCounterException('Network already has admin')
        elif not is_admin and not User.admin_counter:
            raise AdminCounterException('Network first user has to be admin')

    @property
    def username(self):
        return self._username

    @property
    def is_admin(self):
        return self.is_admin

    def check_password(self, value):
        return True if self._password == value else False


class SocialNetwork:

    def __init__(self):
        self.user_dict = {}

    def register_user(self):

        if self.user_dict:
            register_str = 'Enter desired username: '
            is_admin = False
        else:
            register_str = 'Enter admin login: '
            is_admin = True

        while True:
            username = input(register_str).strip().lower()
            if self.user_dict.get(username):
                print('Such user already exists in network')
                continue
            break

        while True:
            password = input('Enter password: ')
            if not self.check_password_complexity(password):
                print('Password should consist of:\n    at least 8 characters and\n\
    a minimum of 1 lower case letter [a-z] and\n\
    a minimum of 1 upper case letter [A-Z] and\n\
    a minimum of 1 numeric character [0-9] and\n\
    a minimum of 1 special character: !#$%&"() *+,-./:;<=>?@[\]^_`{|}~\'')
                continue
            break

        try:
            self.user_dict[username] = User(username, password, is_admin)
        except AdminCounterException as err:
            print(err)

    def authenticate(self, username, password):

        user  = self.user_dict.get(username)

        if not (user and user.check_password(password)):
            raise WrongUsernameOrPassword('Wrong username or password')

        return user

    def check_password_complexity(self, password):

        lower_alphabet = set('abcdefghijklmnopqrstuvwxyz')
        upper_alphabet = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        numbers = set('0123456789')
        special_characters = set(' !#$%&"()*+,-./:;<=>?@[\]^_`{|}~\'')

        password_strength = False
        if len(password) >= 8:
            password_strength = True

        for s in lower_alphabet:
            if password_strength and s in password:
                break
            elif not password_strength:
                break
        else:
            password_strength = False

        for s in upper_alphabet:
            if password_strength and s in password:
                break
            elif not password_strength:
                break
        else:
            password_strength = False

        for s in special_characters:
            if password_strength and s in password:
                break
            elif not password_strength:
                break
        else:
            password_strength = False

        for s in numbers:
            if password_strength and s in password:
                break
            elif not password_strength:
                break
        else:
            password_strength = False

        return password_strength


sn = SocialNetwork()

sn.register_user()

user = sn.authenticate(input('login:'), input('password: '))