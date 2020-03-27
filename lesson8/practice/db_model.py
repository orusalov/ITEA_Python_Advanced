from sql_dict import sql_dict
import sqlite3


class UserIsNotAdminError(Exception):
    pass


class MyDBContextManager:

    def __init__(self, dbname):
        self.dbname = dbname

    def __enter__(self):
        self.conn = sqlite3.connect(self.dbname)
        return self.conn

    def __exit__(self, *args):
        self.conn.close()


# Decorator for checkin if user is admin
def check_is_admin(func):
    def inner(self, *args, **kwargs):
        if not self.is_admin:
            raise UserIsNotAdminError('For this operation user should be admin')
        else:
            return func(self, *args, **kwargs)

    return inner


class User:
    DB_NAME = 'market.db'

    def __init__(
            self,
            is_admin=False
    ):
        self._is_admin = is_admin

    @property
    def is_admin(self):
        return self._is_admin

    def _execute_dml_(self, sql, params):
        with MyDBContextManager(self.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid

    def _execute_select_(self, sql, params):

        with MyDBContextManager(self.DB_NAME) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            description = cursor.description
            data = cursor.fetchall()

            names = [desc[0] for desc in description]
            result = []

            for row in data:
                result.append(dict(zip(names,row)))

        return result

    @check_is_admin
    def add_category(self, category_name):

        params = category_name
        sql = sql_dict['insert_category']

        self._execute_dml_(sql, params)

    @check_is_admin
    def add_product(self, category_id, product_name, price, count_in_market, count_in_warehouse):

        params = category_id, product_name, price, c, count_in_warehouse

        sql = sql_dict['insert_product']

        if count_in_market < 0 or count_in_warehouse < 0 or price < 0:
            raise ValueError("counts and price should be non less than zero")

        self._execute_dml_(sql, params)

    @check_is_admin
    def update_product(self, product_id, count_in_market=None, count_in_warehouse=None, product_name=None, price=None):
        params = (
            count_in_market,
            count_in_warehouse,
            product_name,
            price,
            product_id,
            count_in_market,
            count_in_warehouse,
            product_name,
            price
        )

        if any((count_in_market < 0, count_in_warehouse < 0, price < 0)):
            raise ValueError("counts and price should be non less than zero")

        sql = sql_dict['update_product']

        self._execute_dml_(sql, params)

    def get_product_by_cat_name_prod_name(self, category_name, product_name):
        params = (category_name, product_name)
        sql = sql_dict['get_product_by_cat_name_prod_name']
        result = self._execute_select_(sql, params)

        return result

    def get_products_name_by_category_name(self, category_name):
        params = (category_name,)
        sql = sql_dict['select_products_by_category_name']
        result = self._execute_select_(sql, params)

        return result

    def get_categories(self, category_name=None):
        params = (category_name,)
        sql = sql_dict['select_categories']
        result = self._execute_select_(sql, params)

        return result
