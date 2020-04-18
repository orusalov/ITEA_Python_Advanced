import random
from models import (
    Faculty,
    AcademicGroup,
    Curator,
    Student,
    Mark
)


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def get_random_word(word_length):
    return_list = []
    for i in range(word_length):
        return_list.append(random.choice(ALPHABET))

    return_ = ''.join(return_list).strip()
    return return_


def get_faculty_data():
    return_ = {}
    words = []
    for word_count in range(random.randint(2,5)):
        words.append(get_random_word(random.randint(6,15)))

    return_['faculty_name'] = ' '.join(words).title()
    return_['faculty_abbreviation'] = ''.join([word[0] for word in words]).upper()

    return return_


def get_academic_group_data(faculty):
    return_ = {}
    return_['faculty'] = faculty
    return_['academic_group_name'] = f'{get_random_word(random.randint(1,3)).upper()}-{random.randint(10,99)}'

    return return_


def get_curator_data(faculty):
    return_ = {}
    return_['faculty'] = faculty
    return_['curator_name'] = get_random_word(random.randint(7,10)).title()
    return_['curator_surname'] = get_random_word(random.randint(2,15)).title()

    return return_


def get_student_data():
    return_ = {}
    faculty = random.choice(Faculty.objects())
    return_['curator'] = random.choice(Curator.objects(faculty=faculty))
    return_['academic_group'] = random.choice(AcademicGroup.objects(faculty=faculty))

    return_['student_card'] = random.randint(0,100000000000000)
    return_['student_name'] = get_random_word(random.randint(2,10)).title()
    return_['student_surname'] = get_random_word(random.randint(2,15)).title()

    return_['marks'] = []
    lower_mark = random.randint(2, 5)
    for i in range(random.randint(5, 10)):
        mark = Mark()
        mark.mark = random.randint(lower_mark, 5)
        return_['marks'].append(mark)

    return return_



def create_faculty(**kwargs):
    requirede_fields = ('faculty_name', 'faculty_abbreviation')
    [kwargs[arg] for arg in requirede_fields]

    return Faculty.objects.create(**kwargs)



def create_academic_group(**kwargs):
    requirede_fields = ('faculty', 'academic_group_name')
    [kwargs[arg] for arg in requirede_fields]

    return AcademicGroup.objects.create(**kwargs)


def create_curator(**kwargs):
    requirede_fields = ('faculty', 'curator_name', 'curator_surname')
    [kwargs[arg] for arg in requirede_fields]

    return Curator.objects.create(**kwargs)


def create_student(**kwargs):
    requirede_fields = ('academic_group', 'student_name', 'student_surname', 'student_card')
    [kwargs[arg] for arg in requirede_fields]

    return Student.objects.create(**kwargs)

if __name__ == '__main__':

    for i in range(5):
        print(create_faculty(**get_faculty_data()))

    for fac in Faculty.objects():
        for i in range(random.randint(1,3)):
            print(create_academic_group(**get_academic_group_data(fac)))

    for fac in Faculty.objects():
        for i in range(random.randint(2, 5)):
            print(create_curator(**get_curator_data(fac)))

    for i in range(100):
        print(create_student(**get_student_data()))