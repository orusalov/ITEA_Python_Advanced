import shelve
from sql_dict import sql_dict


class UserIsNotAdminError(Exception):
    pass


class WrongUsernameOrPassword(Exception):
    pass


class MyDBContextManager:

    def __init__(self, dbname):
        self.dbname = dbname

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        return self.conn

    def __exit__(self, *args):
        self.conn.close()

# Decorator for checkin if user is admin
def check_is_admin(func):
    def inner(self, *args, **kwargs):
        if not self.is_admin:
            raise UserIsNotAdminError('For this operation user should be admin')
        else:
            return func(self, *args, **kwargs)

    return inner


class User:
    user_dict = {}

    DB_NAME = 'market.db'

    def __init__(
            self,
            username,
            is_admin=False
    ):
        self._username = username.lower().strip()
        self._is_admin = is_admin

    @property
    def username(self):
        return self._username

    @property
    def is_admin(self):
        return self._is_admin

    def _execute_dml_(self, sql, params):
        with MyDBContextManager(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid

    def _execute_select_(self, sql, params):

        with MyDBContextManager(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            description = cursor.description
            result = cursor.fetchall()

        return description, result

    @check_is_admin
    def add_category(self, category_name):

        params = category_name
        sql = sql_dict['insert_category']

        self._execute_dml_(sql, params)

    @check_is_admin
    def add_product(self, category_id, product_name, price, count_in_market, count_in_warehouse):

        params = category_id, product_name, price, c, count_in_warehouse

        sql = sql_dict['insert_product']

        if count_in_market < 0 or count_in_warehouse < 0 or price < 0:
            raise ValueError("counts and price should be non less than zero")

        self._execute_dml_(sql, params)

    @check_is_admin
    def update_product(self, product_id, count_in_market=None, count_in_warehouse=None, product_name=None, price=None):
        params = (
            count_in_market,
            count_in_warehouse,
            product_name,
            price,
            product_id,
            count_in_market,
            count_in_warehouse,
            product_name,
            price
        )

        if any(count_in_market < 0,
               count_in_warehouse < 0,
               price < 0):
            raise ValueError("counts and price should be non less than zero")

        sql = sql_dict['update_product']

        self._execute_dml_(sql, params)

    def select_product_by_id(self, product_id):
        params = (product_id,)
        sql = sql_dict['select_product_by_id']
        description, result = self._execute_select_(sql, params)

        return description, result

    def select_products_name_by_category_id(self, category_id):
        params = (category_id,)
        sql = sql_dict['select_products_by_category_id']
        description, result = self._execute_select_(sql, params)

        return description, result

    def select_categories(self):
        sql = sql_dict['select_categories']
        description, result = self._execute_select_(sql, None)

        return description, result


class StudensDBUserNetwork:

    def load(self, filename):
        with shelve.open(filename) as user_dict_shelve:
            for user, attributes in user_dict_shelve.items():
                User.user_dict[user] = attributes

    def save(self, filename):
        with shelve.open(filename) as user_dict_shelve:
            for user, attribute in User.user_dict.items():
                user_dict_shelve[user] = attribute

    def register_user(self):

        while True:
            username = input('Enter desired username: ').strip().lower()
            if User.user_dict.get(username):
                print('Such user already exists in network')
                continue

            break

        is_admin = False
        while True:
            is_admin_str = input('Is user Admin?(Y/N): ').strip().lower()

            if is_admin_str not in set('yn'):
                print('Wrong answer!')
                continue

            is_admin = is_admin_str == 'y'

            break

        User.user_dict[username] = User(username, is_admin)

    def authenticate(self, username):

        user = User.user_dict.get(username.strip().lower())
        if not user:
            raise WrongUsernameOrPassword('No such user in system')

        return user


def main():
    students_db_usage = StudensDBUserNetwork()

    USER_DICT_FILE = 'users_dict_file'
    students_db_usage.load(USER_DICT_FILE)

    # Main loop
    try:
        user = None
        while True:
            choise = input('You want to login(1), register(2) or exit(3)?: ').strip()
            if choise not in set('123'):
                print('Wrong input!')
                continue
            elif choise == '3':
                students_db_usage.save(USER_DICT_FILE)
                print('Goodbye!!!')
                break
            elif choise == '2':
                students_db_usage.register_user()
                continue
            elif choise == '1':
                try:
                    user = students_db_usage.authenticate(input('login: '))
                except WrongUsernameOrPassword as err:
                    print(err)
                    continue

            while True and user:
                choise = input('You want to:\
                \n see students full list(1);\
                \n see list of students who has marks higher than 4(2);\
                \n search student by students card(3);\
                \n add new student(4);\
                \n add marks(5);\
                \n update student\'s information(6);\
                \n exit(7): ').strip()

                if choise not in set('1234567'):
                    print('Wrong input!')
                    continue
                elif choise == '1':
                    print(beautify_dataset(*(user.get_students_list_all())))
                    continue
                elif choise == '2':
                    print(beautify_dataset(*(user.get_students_list_higher_than_4())))
                    continue
                elif choise == '3':
                    inputed_students_card = input('Type students card: ').strip().lower()
                    print(beautify_dataset(*(user.get_student_by_students_card(inputed_students_card))))
                    continue
                elif choise == '4':
                    student_name = input('Student\' name: ').strip().capitalize()
                    student_surname = input('Student\'s last name: ').strip().capitalize()
                    faculty = input('Student\'s faculty: ').strip().upper()
                    academic_group = input('Student\'s group name: ').strip().upper()

                    try:
                        inputed_students_card = user.add_student(student_name, student_surname, faculty, academic_group)
                    except UserIsNotAdminError as err:
                        print(err)
                        continue

                    print(beautify_dataset(*(user.get_student_by_students_card(inputed_students_card))))
                    continue
                elif choise == '5':
                    inputed_students_card = input('Type students card: ').strip().lower()

                    header, student = user.get_student_by_students_card(inputed_students_card)

                    print(beautify_dataset(header, student))
                    if not student:
                        print('There is no such student')
                        continue
                    try:
                        while True:
                            input_mark = input('Which mark add(2/3/4/5 or empty to finish adding): ')
                            if input_mark and (input_mark not in set('2345')):
                                print('Wrong input!')
                                continue
                            elif not input_mark:
                                break
                            user.add_mark(inputed_students_card, int(input_mark))
                    except UserIsNotAdminError as err:
                        print(err)
                        continue

                    print(beautify_dataset(*(user.get_student_by_students_card(inputed_students_card))))

                    continue
                elif choise == '6':
                    inputed_students_card = input('Type students card: ').strip().lower()

                    header, student = user.get_student_by_students_card(inputed_students_card)

                    print(beautify_dataset(header, student))
                    if not student:
                        print('There is no such student')
                        continue

                    student_name = input('Student\' name: ').strip().capitalize()
                    student_surname = input('Student\'s last name: ').strip().capitalize()
                    faculty = input('Student\'s faculty: ').strip().upper()
                    academic_group = input('Student\'s group name: ').strip().upper()

                    student_name = None if not student_name else student_name
                    student_surname = None if not student_surname else student_surname
                    faculty = None if not faculty else faculty
                    academic_group = None if not academic_group else academic_group

                    try:
                        user.change_student(inputed_students_card, student_name, student_surname, faculty,
                                            academic_group)
                    except UserIsNotAdminError as err:
                        print(err)
                        continue

                    print(beautify_dataset(*(user.get_student_by_students_card(inputed_students_card))))

                    continue
                elif choise == '7':
                    print('Goodbye!!!')
                    break

    except Exception as err:
        students_db_usage.save(USER_DICT_FILE)
        raise err


if __name__ == '__main__':
    try:
        main()

    except sqlite3.DatabaseError as err:
        print(err)
