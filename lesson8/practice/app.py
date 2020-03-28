from flask import Flask
from flask import render_template, request, jsonify
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

@app.route('/add_product', methods=['POST', 'GET'])
def add_product():

    user = User(is_admin=True)
    page_title = 'Adding Product'

    if request.method == 'GET':
        data = user.get_categories()
        return render_template(
            'add_product.html',
            page_title=page_title,
            categories=data
        )
    elif request.method == 'POST':
        dict_values = request.form.to_dict()
        for k, v in dict_values.items():
            if k != 'product_name':
                dict_values[k] = int(float(v)*100) if k == 'price' else int(v)

        user.add_product(**dict_values)

        data = user.get_categories()
        return render_template(
            'add_product.html',
            page_title=page_title,
            categories=data,
            successfully_added='Successfully Added'
        )

@app.route('/add_product/add_category', methods=['POST', 'GET'])
def add_new_category():

    user = User(is_admin=True)
    page_title = 'Adding Category'

    if request.method == 'GET':
        data = user.get_categories()
        return render_template(
            'add_category.html',
            page_title=page_title,
            categories=data
        )
    elif request.method == 'POST':
        dict_values = request.form.to_dict()

        user.add_category(**dict_values)

        data = user.get_categories()
        return render_template(
            'add_category.html',
            page_title=page_title,
            categories=data,
            successfully_added='Successfully Added'
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0')


