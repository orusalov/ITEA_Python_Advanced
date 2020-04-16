from flask_restful import Resource
from models import Faculty, AcademicGroup, Curator, Student, Mark
from schemas import (
    FacultySchema,
    FacultyPutSchema,
    AcademicGroupSchema,
    AcademicGroupPostSchema,
    AcademicGroupPutSchema,
    CuratorSchema,
    CuratorPostSchema,
    CuratorPutSchema,
    MarkSchema,
    StudentSchema,
    StudentPostSchema,
    StudentPutSchema,
    ValidationError
)
from flask import request

def get_faculty_by_abr_or_name(faculty: str):
    if faculty.isupper():
        return Faculty.objects.get(faculty_abbreviation=faculty)
    elif faculty.istitle():
        return Faculty.objects.get(faculty_name=faculty)


class FacultyResource(Resource):

    def get(self, id=None):
        if id:
            faculty = Faculty.objects.get(id=id)
            return FacultySchema().dump(faculty)
        else:
            faculties = Faculty.objects()
            return FacultySchema().dump(faculties, many=True)

    def post(self):
        try:
            data = FacultySchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        faculty = Faculty.objects.create(**data)
        return FacultySchema().dump(faculty)

    def put(self, id):
        faculty = Faculty.objects.get(id=id)

        try:
            data = FacultyPutSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        faculty.modify(**data)
        return FacultySchema().dump(faculty)

    def delete(self):
        pass


class AcademicGroupResource(Resource):

    def get(self, id=None):
        if id:
            academic_group = AcademicGroup.objects.get(id=id)
            return AcademicGroupSchema().dump(academic_group)
        else:
            academic_groups = AcademicGroup.objects()
            return AcademicGroupSchema().dump(academic_groups, many=True)

    def post(self):
        try:
            data = AcademicGroupPostSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        data['faculty'] = get_faculty_by_abr_or_name(data['faculty'])

        a_g = AcademicGroup.objects.create(**data)
        return AcademicGroupSchema().dump(a_g)

    def put(self, id):
        a_g = AcademicGroup.objects.get(id=id)

        try:
            data = AcademicGroupPutSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        if data.get('faculty'):
            data['faculty'] = get_faculty_by_abr_or_name(data['faculty'])

        a_g.modify(**data)
        return AcademicGroupSchema().dump(a_g)

    def delete(self):
        pass


class CuratorResource(Resource):

    def get(self, id=None):
        if id:
            curator = Curator.objects.get(id=id)
            return CuratorSchema().dump(curator)
        else:
            curators = Curator.objects()
            return CuratorSchema().dump(curators, many=True)

    def post(self):

        try:
            data = CuratorPostSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        data['faculty'] = get_faculty_by_abr_or_name(data['faculty'])

        curator = Curator.objects.create(**data)
        return CuratorSchema().dump(curator)

    def put(self, id):
        curator = Curator.objects.get(id=id)

        try:
            data = CuratorPutSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        if data.get('faculty'):
            data['faculty'] = get_faculty_by_abr_or_name(data['faculty'])

        curator.modify(**data)
        return CuratorSchema().dump(curator)

    def delete(self):
        pass


class StudentResource(Resource):

    def get(self, id=None):
        if id:
            student = Student.objects.get(id=id)
            return StudentSchema().dump(student)
        else:
            students = Student.objects()
        return StudentSchema().dump(students, many=True)

    def post(self):

        try:
            data = StudentPostSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        if data.get('marks'):
            marks = []
            for m in data['marks'].split(','):
                m_dict = {'mark': int(m.strip())}

                try:
                    m_data = MarkSchema().load(m_dict)
                except ValidationError as err:
                    return str(err)

                mark_obj = Mark(**m_data)
                marks.append(mark_obj)

            data['marks'] = marks

        faculty = get_faculty_by_abr_or_name(data['faculty'])
        del data['faculty']

        if data.get('curator_name') and data.get('curator_surname'):
            data['curator'] = Curator.objects.get(
                faculty=faculty,
                curator_name=data['curator_name'],
                curator_surname=data['curator_surname']
            )

            del data['curator_name']
            del data['curator_surname']

        if not data['curator']:
            #raise ValidationError('No curator found with this name on the same faculty as student')
            return 'No curator found with this name on the same faculty as student'

        data['academic_group'] = AcademicGroup.objects.get(
            academic_group_name=data['academic_group'],
            faculty=faculty
        )

        if not data['academic_group']:
            #raise ValidationError('No academic group found with this name on the same faculty as student')
            return 'No academic group found with this name on the same faculty as student'

        student = Student.objects.create(**data)
        return StudentSchema().dump(student)

    def put(self, id):
        student = Student.objects.get(id=id)

        try:
            data = StudentPutSchema().load(request.get_json())
        except ValidationError as err:
            return str(err)

        if data.get('marks'):
            marks = []
            for m in data['marks'].split(','):
                m_dict = {'mark': int(m.strip())}

                try:
                    m_data = MarkSchema().load(m_dict)
                except ValidationError as err:
                    return str(err)

                mark_obj = Mark(**m_data)
                marks.append(mark_obj)

            data['marks'] = marks

        if data.get('faculty'):
            faculty = get_faculty_by_abr_or_name(data['faculty'])
            del data['faculty']

        if data.get('curator_name') and data.get('curator_surname'):
            data['curator'] = Curator.objects.get(
                faculty=faculty,
                curator_name=data['curator_name'],
                curator_surname=data['curator_surname']
            )

            if not data['curator']:
                #raise ValidationError('No curator found with this name on the same faculty as student')
                return 'No curator found with this name on this faculty'

            del data['curator_name']
            del data['curator_surname']

        if data.get('academic_group'):
            data['academic_group'] = AcademicGroup.objects.get(
                academic_group_name=data['academic_group'],
                faculty=faculty
            )

            if not data['academic_group']:
                #raise ValidationError('No academic group found with this name on the same faculty as student')
                return 'No academic group found with this name on this faculty'

        if (data.get('curator') and
            not data.get('academic_group') and
            data.get('curator').faculty != student.faculty) or \
            (not data.get('curator') and
             data.get('academic_group') and
             student.curator and
             data.get('academic_group').faculty != student.curator.faculty):
            # raise ValidationError('Group and curator are in different faculties')
            return 'Group and curator are in different faculties'

        student.modify(**data)

        return StudentSchema().dump(student)

    def delete(self):
        pass
