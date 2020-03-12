from datetime import date, timedelta
from random import randint


class AdminCounterException(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class WrongUsernameOrPassword(Exception):
    pass


class User:
    user_dict = {}

    def __init__(self, username, password, is_admin=False):
        self._username = username.lower()
        self._password = password
        self._is_admin = is_admin
        self._registration_date = date.today() - timedelta(randint(0, 1000))
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
                print('Password should consist of:\n    at least 8 characters and\n\
    a minimum of 1 lower case letter [a-z] and\n\
    a minimum of 1 upper case letter [A-Z] and\n\
    a minimum of 1 numeric character [0-9] and\n\
    a minimum of 1 special character: !#$%&"() *+,-./:;<=>?@[\]^_`{|}~\'')
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


class SNPost:

    def __init__(self):

        self._content = input('You are creating post. What\'s on your mind?: ')
        self._date = date.today() - timedelta(randint(0, 1000))

    def __str__(self):
        return f'{self._date}\n{self._content}'


def main():

    sn = SocialNetwork()
    sn.register_user()

    # Main loop
    while True:
        choise = input('You want to login(1), register(2) or exit(3)?: ').strip()
        if choise not in set('123'):

            print('Wrong input!')
            continue

        elif choise == '3':

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
