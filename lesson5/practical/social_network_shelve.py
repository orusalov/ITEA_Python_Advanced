from datetime import date, timedelta
from random import randint
import shelve

class AdminCounterException(Exception):
    pass


class WrongUsernameOrPassword(Exception):
    pass


class User:
    user_dict = {}

    def __init__(
            self,
            username,
            password,
            is_admin=False,
            registration_date=date.today() - timedelta(randint(0, 1000))
    ):
        self._username = username.lower().strip()
        self._password = password
        self._is_admin = is_admin
        self._registration_date = registration_date
        self._posts = []

        if not is_admin and not User.user_dict:
            raise AdminCounterException('Network first user has to be admin')

    @property
    def username(self):
        return self._username

    @property
    def is_admin(self):
        return self._is_admin

    @property
    def registration_date(self):
        return self._registration_date

    @property
    def posts(self):
        return self._posts

    def check_password(self, value):
        return True if self._password == value else False

    def create_post(self):
        self._posts.append(SNPost())

    def see_posts(self, which_user=None):

        if self.is_admin and which_user:

            print(which_user)
            which_user = User.user_dict.get(which_user)

            if which_user:

                for post in which_user.posts:
                    print(post, end='\n\n')

            print('\n\n')

        elif self.is_admin:

            for username in User.user_dict:
                self.see_posts(username)

        else:

            for post in self.posts:
                print(post, end='\n\n')

    def see_user_list(self):

        if self.is_admin:

            for val in User.user_dict.values():
                print(val.username, val.registration_date)

        else:
            print(self.username, self.registration_date)


class SocialNetwork:

    PWD_LOWER_ALPHABET = set('abcdefghijklmnopqrstuvwxyz')
    PWD_UPPER_ALPHABET = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    PWD_NUMBERS = set('0123456789')
    PWD_SPECIAL_CHARACTERS = set('!#$%&"()*+,-./:;<=>?@[\]^_`{}~\'')
    PWD_INVALID_CHARS = set(' |')

    def load(self, filename):
        with shelve.open(filename) as user_dict_shelve:
            for user, attributes in user_dict_shelve.items():
                parts = attributes.split('|')
                registration_date = parts[3].split('-')
                registration_date = [int(i) for i in registration_date]
                print(user, parts[1], parts[2] == 'True', date(*registration_date))
                User.user_dict[user] = User(user, parts[1], parts[2] == 'True', date(*registration_date))


    def save(self, filename):
        with shelve.open(filename) as user_dict_shelve:
            for user, attributes in User.user_dict.items():
                parts = '|'.join([
                    attributes.username,
                    attributes._password,
                    str(attributes.is_admin),
                    str(attributes.registration_date)
                ])
                user_dict_shelve[user] = parts

    def register_user(self):

        if User.user_dict:

            register_str = 'Enter desired username: '
            is_admin = False

        else:

            register_str = 'Enter admin login: '
            is_admin = True

        while True:

            username = input(register_str).strip().lower()
            if User.user_dict.get(username):
                print('Such user already exists in network')
                continue

            break

        while True:

            password = input('Type password: ')

            if password != input('Retype password: '):

                print('You did not retype password')
                continue

            if not self.check_password_complexity(password):
                print(f'Password should consist of:\n    at least 8 characters and\n\
    a minimum of 1 lower case letter [a-z] and\n\
    a minimum of 1 upper case letter [A-Z] and\n\
    a minimum of 1 numeric character [0-9] and\n\
    a minimum of 1 special character: {"".join(self.PWD_INVALID_CHARS)}')
                continue

            break

        try:

            User.user_dict[username] = User(username, password, is_admin)

        except AdminCounterException as err:

            print(err)

    def authenticate(self, username, password):

        user = User.user_dict.get(username.strip().lower())

        if not (user and user.check_password(password)):
            raise WrongUsernameOrPassword('Wrong username or password')

        return user

    def check_password_complexity(self, password):

        password_strength = False
        if len(password) >= 8:
            password_strength = True

        for s in self.PWD_LOWER_ALPHABET:

            if password_strength and s in password:
                break
            elif not password_strength:
                break

        else:
            password_strength = False

        for s in self.PWD_UPPER_ALPHABET:

            if password_strength and s in password:
                break
            elif not password_strength:
                break

        else:
            password_strength = False

        for s in self.PWD_SPECIAL_CHARACTERS:

            if password_strength and s in password:
                break
            elif not password_strength:
                break

        else:
            password_strength = False

        for s in self.PWD_NUMBERS:

            if password_strength and s in password:
                break
            elif not password_strength:
                break

        else:
            password_strength = False

        for s in self.PWD_INVALID_CHARS:

            if password_strength and s in password:
                password_strength = False
                break
            elif not password_strength:
                break

        return password_strength


class SNPost:

    def __init__(self):

        self._content = input('You are creating post. What\'s on your mind?: ')
        self._date = date.today() - timedelta(randint(0, 1000))

    def __str__(self):
        return f'{self._date}\n{self._content}'


def main():

    sn = SocialNetwork()

    USER_DICT_FILE = 'user_dict_file'
    sn.load(USER_DICT_FILE)


    # Main loop
    while True:
        choise = input('You want to login(1), register(2) or exit(3)?: ').strip()
        if choise not in set('123'):

            print('Wrong input!')
            continue

        elif choise == '3':

            sn.save(USER_DICT_FILE)
            print('Goodbye!!!')
            break

        elif choise == '2':

            sn.register_user()
            continue

        elif choise == '1':

            try:
                user = sn.authenticate(input('login: '), input('password: '))
            except WrongUsernameOrPassword as err:
                print(err)
                continue

        while True:

            choise = input('You want to see_user_list(1), create_post(2), see_posts(3) or exit(4)?: ').strip()
            if choise not in set('1234'):

                print('Wrong input!')
                continue

            elif choise == '4':

                print('Goodbye!!!')
                break

            elif choise == '3':

                user.see_posts()
                continue

            elif choise == '2':

                user.create_post()
                continue

            elif choise == '1':

                user.see_user_list()
                continue


if __name__ == '__main__':
    main()
