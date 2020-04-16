from marshmallow import Schema, fields, ValidationError, validates, validates_schema
import re


def validate_academic_group_name(value):
    p = re.compile('[A-ZА-Я]{1,3}-[0-9]{2}')
    is_group_name = bool(p.fullmatch(value))
    if not is_group_name:
        raise ValidationError('Value should be [A-ZА-Я]{1,3}-[0-9]{2}')


def validate_faculty_post_put_del(value):
    if value and not ((value.isupper() and value.isalpha()) or (value.istitle() and value.replace(' ', '').isalpha())):
        raise ValidationError('Faculty should be given as abbreviation or faculty name\n\
abbreviation should be only upper case and faculty name in Title Case')


def validate_curator_surname(value: str):
    if value and not (value.istitle() and value.replace(' ', '').isalpha()):
        raise ValidationError('Value should be titled and alpha only')


def validate_curator_name(value: str):
    if value and not (value.istitle() and value.replace(' ', '').isalpha()):
        raise ValidationError('Value should be titled and alpha only')


class FacultySchema(Schema):
    id = fields.String(dump_only=True)

    faculty_name = fields.String(required=True)
    faculty_abbreviation = fields.String()

    @validates('faculty_name')
    def validate_faculty_name(self, value: str):
        if value and not (value.istitle() and value.replace(' ', '').isalpha()):
            raise ValidationError('Value should be titled and alpha only')

    @validates('faculty_abbreviation')
    def validate_faculty_abbreviation(self, value: str):
        if value and not (value.isupper() and value.isalpha()):
            raise ValidationError('Value should be uppered and alpha only')

class FacultyPutSchema(FacultySchema):
    def __init__(self):
        super().__init__()
        self.fields['faculty_name'].required = False


class AcademicGroupSchema(Schema):
    id = fields.String(dump_only=True)
    academic_group_name = fields.String(required=True, validate=validate_academic_group_name)
    faculty = fields.Nested(FacultySchema, dump_only=True, required=True)


class AcademicGroupPostSchema(AcademicGroupSchema):
    faculty = fields.String(load_only=True, required=True, validate=validate_faculty_post_put_del)


class AcademicGroupPutSchema(AcademicGroupPostSchema):
    def __init__(self):
        super().__init__()
        self.fields['academic_group_name'].required = False
        self.fields['faculty'].required = False


class CuratorSchema(Schema):
    id = fields.String(dump_only=True)

    curator_surname = fields.String(required=True, validate=validate_curator_surname)
    curator_name = fields.String(required=True, validate=validate_curator_name)
    faculty = fields.Nested(FacultySchema, dump_only=True, required=True)


class CuratorPostSchema(CuratorSchema):
    faculty = fields.String(load_only=True, required=True, validate=validate_faculty_post_put_del)


class CuratorPutSchema(CuratorPostSchema):
    def __init__(self):
        super().__init__()
        self.fields['curator_surname'].required = False
        self.fields['curator_name'].required = False
        self.fields['faculty'].required = False


class MarkSchema(Schema):
    mark = fields.Int(required=True,validate=lambda mark: (2 <= mark <= 5))


class StudentSchema(Schema):
    id = fields.String(dump_only=True)

    student_card = fields.Int(required=True, validate=lambda card: card > 0)
    student_surname = fields.String(required=True)
    student_name = fields.String(required=True)
    academic_group = fields.Nested(AcademicGroupSchema, required=True, dump_only=True)
    curator = fields.Nested(CuratorSchema, dump_only=True)
    marks = fields.List(fields.Nested(MarkSchema), dump_only=True)

    @validates('student_surname')
    def validate_student_surname(self, value: str):
        if not (value.istitle() and value.replace(' ', '').isalpha()):
            raise ValidationError('Value should be titled and alpha only')

    @validates('student_name')
    def validate_student_name(self, value: str):
        if not (value.istitle() and value.replace(' ', '').isalpha()):
            raise ValidationError('Value should be titled and alpha only')


class StudentPostSchema(StudentSchema):
    curator_name = fields.String(load_only=True, validate=validate_curator_name)
    curator_surname = fields.String(load_only=True, validate=validate_curator_surname)
    academic_group = fields.String(load_only=True, required=True, validate=validate_academic_group_name)
    faculty = fields.String(load_only=True, required=True, validate=validate_faculty_post_put_del)
    marks = fields.String(load_only=True)

    @validates('marks')
    def validate_marks(self, value):
        p = re.compile('\d( *, *\d)*')
        is_group_name = bool(p.fullmatch(value))
        if not is_group_name:
            raise ValidationError('Marks should be digits and separated by comma')

    @validates_schema
    def validate_curator_requires_faculty(self, data, **kwargs):
        if (('curator_name' in data and ('curator_surname' not in data or 'faculty' not in data)) or
            ('curator_surname' in data and ('curator_name' not in data or 'faculty' not in data))):
            raise ValidationError('curator requires name, surname and faculty')


class StudentPutSchema(StudentPostSchema):
    def __init__(self):
        super().__init__()
        self.fields['student_card'].required = False
        self.fields['student_surname'].required = False
        self.fields['student_name'].required = False
        self.fields['academic_group'].required = False
        self.fields['faculty'].required = False
        self.fields['curator_name'].required = False
        self.fields['curator_surname'].required = False

    @validates_schema
    def validate_academic_group_requires_faculty(self, data, **kwargs):
        if 'academic_group' in data and 'faculty' not in data:
            raise ValidationError('academic_group requires faculty')