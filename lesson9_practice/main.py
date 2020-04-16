from flask import Flask
from flask_restful import Api
from resources import *

app = Flask(__name__)
api = Api(app)

api.add_resource(FacultyResource, '/faculty', '/faculty/<id>')
api.add_resource(AcademicGroupResource, '/academic_group', '/academic_group/<id>')
api.add_resource(CuratorResource, '/curator', '/curator/<id>')
api.add_resource(StudentResource, '/student', '/student/<id>')

if __name__ == '__main__':
    app.run(debug=True)