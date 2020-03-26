from context_manager import MyDBContextManager
from context_manager import beautify_dataset

import shelve


class UserIsNotAdminError(Exception):
    pass


class WrongUsernameOrPassword(Exception):
    pass


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

    STUDENTS_DB = 'students.db'

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
        with MyDBContextManager(self.STUDENTS_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid

    @check_is_admin
    def add_mark(self, students_card, mark):
        params = students_card, mark

        sql = """
                insert into marks (student_id, mark)
                values
                (
                (select id from student where students_card = ?),
                ?
                )
              """

        self._execute_dml_(sql, params)

    @check_is_admin
    def add_student(self, student_name, student_surname, faculty, group_name):
        params = student_name, student_surname, faculty, group_name

        sql = """
        insert into student (students_card, student_name, student_surname, academic_group_id)
        values
        (
        (select abs(random())),
        ?,
        ?,
        (SELECT
            ag.id
         from academic_group ag join faculty f on ag.faculty_id = f.id
         where f.faculty_name=?
           and ag.academic_group_name=?
        )
        )
        """

        id = self._execute_dml_(sql, params)
        return self._get_students_list(student_id=id)[1][0][2]

    @check_is_admin
    def change_student(self, students_card, student_name=None, student_surname=None, faculty=None, group_name=None):
        params = (
            student_name,
            student_surname,
            faculty,
            group_name,
            students_card,
            student_name,
            student_surname,
            faculty,
            group_name
        )

        sql = """
            update student
            set student_name = coalesce(?, student_name),
                student_surname = coalesce(?, student_surname),
                academic_group_id = coalesce((SELECT
                                                ag.id
                                             from academic_group ag join faculty f on ag.faculty_id = f.id
                                             where f.faculty_name=?
                                               and ag.academic_group_name=?
                                            ),academic_group_id
                                           )
            where students_card = ?
                and (student_name <> coalesce(?, student_name)
                or student_surname <> coalesce(?, student_surname)
                or academic_group_id <> coalesce((SELECT
                                                     ag.id
                                                  from academic_group ag join faculty f on ag.faculty_id = f.id
                                                  where f.faculty_name=?
                                                    and ag.academic_group_name=?
                                                ),academic_group_id
                                               )
                    )
            """

        self._execute_dml_(sql, params)

    def _get_students_list(self, mark_higher=None, students_card=None, student_id=None):
        params = (
            students_card,
            student_id,
            mark_higher
        )

        sql = """
             select
                 s.student_name "Students Name",
                 s.student_surname "Students Last Name",
                 s.students_card "Student Card",
                 f.faculty_name "Faculty",
                 ag.academic_group_name "Group Name",
                 coalesce(group_concat(m.mark,', '),' ') "Marks"
             from student s 
             join academic_group ag on ag.id = s.academic_group_id
             join faculty f on ag.faculty_id = f.id
             left join marks m on m.student_id=s.id
             where s.students_card = coalesce(?, s.students_card)
                and s.id = coalesce(?, s.id)
             group by s.student_name, s.student_surname, s.students_card, f.faculty_name, ag.academic_group_name
             having coalesce(min(mark),0) >= coalesce(?, min(mark), 0)
             order by 4, 5, 2, 1
              """

        result = None
        description = None
        with MyDBContextManager(self.STUDENTS_DB) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            result = cursor.fetchall()
            description = cursor.description

        return description, result

    def get_student_by_students_card(self, students_card):
        return self._get_students_list(students_card=students_card)

    def get_students_list_higher_than_4(self):
        return self._get_students_list(mark_higher=4)

    def get_students_list_all(self):
        return self._get_students_list()


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
