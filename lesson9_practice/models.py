from db_config import DB_CONFIG
import mongoengine as me

me.connect(**DB_CONFIG)


class Faculty(me.Document):
    faculty_name = me.StringField(min_length=4, max_length=256, unique=True, required=True)
    faculty_abbreviation = me.StringField(min_length=2, max_length=7, unique=True)

    def get_students(self):
        students = []
        for student in Student.objects():
            if student.faculty == self:
                students.append(student)

        return students

    def get_best_students(self):
        THRESHOLD = 4.5
        best_students = []
        for student in self.get_students():
            if student.get_avg_mark() >= THRESHOLD:
                best_students.append(student)

        return best_students


class AcademicGroup(me.Document):
    academic_group_name = me.StringField(min_length=4, max_length=7, regex='[A-ZА-Я]{1,3}-[0-9]{2}', unique=True,
                                         required=True)
    faculty = me.ReferenceField(Faculty, required=True)

    @property
    def students(self):
        return Student.objects(academic_group=self)


class Curator(me.Document):
    curator_surname = me.StringField(min_length=2, max_length=64, required=True)
    curator_name = me.StringField(min_length=2, max_length=64, required=True)
    faculty = me.ReferenceField(Faculty, required=True)

    @property
    def students(self):
        return Student.objects(curator=self)


class Mark(me.EmbeddedDocument):
    mark = me.IntField(min_value=2, max_value=5, required=True)

    def __str__(self):
        return str(self.mark)


class Student(me.Document):
    student_card = me.IntField(min_length=0, unique=True, required=True)
    student_surname = me.StringField(min_length=2, max_length=64, required=True)
    student_name = me.StringField(min_length=2, max_length=64, required=True)
    academic_group = me.ReferenceField(AcademicGroup, required=True)
    curator = me.ReferenceField(Curator)
    marks = me.EmbeddedDocumentListField(Mark)

    def get_avg_mark(self):
        marks = [m.mark for m in self.marks]
        if marks:
            return sum(marks)/len(marks)

    @property
    def faculty(self):
        return self.academic_group.faculty
