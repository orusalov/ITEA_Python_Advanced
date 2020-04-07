from flask_restful import Resource
from flask import request
from models import User

class UserResource(Resource):

    def get(self, user_id=None):
        if user_id:
            return User.objects.get(id=user_id).to_json()
        elif not user_id:
            return User.objects.to_json()

    def post(self):

        data = request.get_json()
        user = User.objects.create(**data)

        return user.to_json()

    def put(self, user_id):
        pass

    def delete(self, user_id):
        pass