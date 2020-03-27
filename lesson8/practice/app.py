from flask import Flask, render_template
from db_model import User

app = Flask(__name__)

@app.route('/')
def index():
    page_title = 'User choose'
    return render_template('index.html', page_title=page_title)

@app.route('/categories')
@app.route('/categories/<string:category_name>')
@app.route('/categories/<string:category_name>/<string:product_name>')
def categories_and_products(category_name=None, product_name=None):

    user = User()

    if not category_name:
        page_title = 'categories'
        data = user.get_categories()

        return render_template('categories.html', page_title=page_title, data=data)
    elif category_name and not product_name:
        page_title = category_name
        data = user.get_products_name_by_category_name(category_name)

        return render_template('product_list.html', page_title=page_title, category_name=category_name, data=data)
    elif category_name and product_name:
        page_title = product_name
        data = user.get_product_by_cat_name_prod_name(category_name, product_name)

        return render_template('product_detail.html', page_title=page_title, category_name=category_name, data=data)


# @app.route('/posts')
# @app.route('/posts/<int:post_id>')
# def posts(post_id=None):
#
#     if post_id:
#         return render_template('postbody.html', post=POSTS[post_id - 1])
#
#     return render_template('posts.html', posts=POSTS)

# @app.route('/posts')
# def posts():
#     return render_template('posts.html', posts=POSTS)

if __name__ == '__main__':
    app.run(debug=True)


