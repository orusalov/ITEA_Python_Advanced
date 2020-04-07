from flask import Flask
from flask_restful import Api
from resources import UserResource


app = Flask(__name__)
api = Api(app)

# @app.route('user', methods=['GET','PUT','POST','DELETE'])
# def user():
#     if request.method == 'GET':
#         pass
#     elif request.method == 'PUT':
#         pass
#     elif request.method == 'POST':
#         pass
#     elif request.method == 'DELETE':
#         pass
#     else:
#         return abort(403)

api.add_resource(UserResource, '/users', '/users/<user_id>')

    
if __name__ == '__main__':
    app.run(debug=True)