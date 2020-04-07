from marshmallow import Schema, fields, ValidationError, validates, validate

# def except_sprinter(value):
#     if value =='Sprinter':
#         raise ValidationError('Value can\'t be Sprinter')


class BusSchema(Schema):
    id = fields.String(dump_only=True)
    # model_ = fields.String(validate=except_sprinter)
    model_ = fields.String()
    seats = fields.Int(validate=validate.Range(min=4, max=50))

    @validates('model_')
    def validate_model(self, value):
        if value == 'Sprinter':
            raise ValidationError('Value can\'t be Sprinter')


class TripSchema(Schema):
    id = fields.String(dump_only=True)
    destination = fields.String()
    bus = fields.Nested(BusSchema, dump_only=True)


class TripPostSchema(TripSchema):
    bus = fields.String(load_only=True)


class PassengerSchema(Schema):
    name = fields.String(required=True)
    surname = fields.String(required=True)
    trip = fields.String(dump_only=True)
