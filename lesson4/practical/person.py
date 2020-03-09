from abc import ABC, abstractmethod
from datetime import date


class Person(ABC):
    """Создайте класс ПЕРСОНА с абстрактными методами, позволяющими
    вывести на экран информацию о персоне, а также определить ее возраст (в
    текущем году). Создайте дочерние классы: АБИТУРИЕНТ (фамилия, дата
    рождения, факультет), СТУДЕНТ (фамилия, дата рождения, факультет, курс),
    ПРЕПОДАВАТЕЛЬ (фамилия, дата рождения, факультет, должность, стаж),
    со своими методами вывода информации на экран и определения возраста.
    Создайте список из n персон, выведите полную информацию из базы на
    экран, а также организуйте поиск персон, чей возраст попадает в заданный
    диапазон."""

    def __init__(self, surname, birth_date, faculty):

        self.surname = surname

        if not isinstance(birth_date, date):
            raise ValueError('birth_date should be datetime.date')

        self.birth_date = birth_date
        self.faculty = faculty

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = value

    @property
    def faculty(self):
        return self._faculty

    @faculty.setter
    def faculty(self, value):
        self._faculty = value

    @abstractmethod
    def get_age(self):

        dt = date.today()
        birthday_this_year = date(dt.year, self.birth_date.month, self.birth_date.day)

        if dt < birthday_this_year:
            return dt.year - self.birth_date.year - 1
        else:
            return dt.year - self.birth_date.year

    @abstractmethod
    def get_information(self):
        pass


class Enrollee(Person):

    def __init__(self, surname, birth_date, faculty):
        super().__init__(surname, birth_date, faculty)

    def get_age(self):
        return super().get_age()

    def get_information(self):
        info = {'Surname': self.surname, 'Birth': self.birth_date, 'Age': self.get_age(), 'Faculty': self.faculty}
        longest_key = len(sorted(info.keys(), key=lambda x: len(x)).pop())

        print('Enrollee:')
        for key, val in info.items():
            print(f'    {key}:{" " * (longest_key - len(key))}', val)
        print()


class Student(Person):

    def __init__(self, surname, birth_date, faculty, course):
        super().__init__(surname, birth_date, faculty)
        self.course = course

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, value):
        self._course = value

    def get_age(self):
        age = super().get_age()
        return age

    def get_information(self):
        info = {'Surname': self.surname, 'Birth': self.birth_date, 'Age': self.get_age(), 'Faculty': self.faculty,
                'Course': self.course}
        longest_key = len(sorted(info.keys(), key=lambda x: len(x)).pop())

        print('Student:')
        for key, val in info.items():
            print(f'    {key}:{" " * (longest_key - len(key))}', val)
        print()


class Lecturer(Person):

    def __init__(self, surname, birth_date, faculty, position, experience):
        super().__init__(surname, birth_date, faculty)
        self.position = position
        self.experience = experience

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        self._experience = value

    def get_age(self):
        age = super().get_age()
        return age

    def get_information(self):
        info = {
            'Surname': self.surname,
            'Birth': self.birth_date,
            'Age': self.get_age(),
            'Faculty': self.faculty,
            'Position': self.position,
            'Experience': self.experience
        }
        longest_key = len(sorted(info.keys(), key=lambda x: len(x)).pop())

        print('Lecturer:')
        for key, val in info.items():
            print(f'    {key}:{" " * (longest_key - len(key))}', val)
        print()


def person_search_by_age(person_list):
    age_from = int(input('Type from which age should we filter(including): ').strip())
    age_to = int(input('Type to wich age should we filter(including): ').strip())

    filtered_list = list(filter(lambda x: age_from <= x.get_age() <= age_to, person_list))

    return filtered_list


enrollee_rusal = Enrollee('Rusalovskyi', date(1988, 8, 25), 'ITS')
student_gyrenko = Student('Gyrenko', date(1986, 1, 23), 'ABHSS', 4)
lecturer_khomenko = Lecturer('Khomenko', date(1985, 2, 6), 'FAKS', 'Professor', 12)

person_list = [enrollee_rusal, student_gyrenko, lecturer_khomenko]

for p in person_list:
    p.get_information()

print('\n\n\n')

for p in person_search_by_age(person_list):
    p.get_information()
