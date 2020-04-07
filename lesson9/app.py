from flask import Flask
from flask import render_template, request, jsonify
import json

app = Flask(__name__)

users = []

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        users.append(request.form.to_dict())
        # response = app.response_class(
        #     response=json.dumps(users),
        #     status=200,
        #     mimetype='application/json'
        # )
        # return response
        return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)