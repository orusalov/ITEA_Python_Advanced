from flask import Flask, render_template
from db import POSTS

app = Flask(__name__)

@app.route('/')
def index():
    page_title = 'Orusalov page'
    name = 'Oleksandr'
    return render_template('index.html', page_title=page_title, name=name)

@app.route('/hi')
def hola():

    names = ['Orusalov','Gyrenko','Klymyk','Mans']
    return render_template('greetings.html',names = names)

@app.route('/posts')
@app.route('/posts/<int:post_id>')
def posts(post_id=None):

    if post_id:
        return render_template('postbody.html', post=POSTS[post_id - 1])

    return render_template('posts.html', posts=POSTS)

# @app.route('/posts')
# def posts():
#     return render_template('posts.html', posts=POSTS)

if __name__ == '__main__':
    app.run(debug=True)


