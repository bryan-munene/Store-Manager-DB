from .db_conn import ModelSetup

sale_items_temp = []


class SalesModel(ModelSetup):
    '''Handles the data logic of the sales section'''
    def __init__(
            self,
            item_id=None,
            name=None,
            quantity=None,
            price=None,
            total=None,
            auth=None,
            user_id=None):
        '''Initializes the variables for the sales class'''
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.total = total
        self.auth = auth
        self.user_id = user_id

    def add_sale_items_list(self, item_id, name, quantity, price, total, auth):
        '''Adds sale items to a temporary list until the sale object is created'''
        self.sale_item_id = len(sale_items_temp) + 1
        sale_item = {
            "sale_item_id": self.sale_item_id,
            "item_id": item_id,
            "item_name": name,
            "quantity": quantity,
            "price": price,
            "total": total,
            "auth": auth
        }

        sale_items_temp.append(sale_item)

        return sale_item

    def add_sale_items(
            self,
            sale_id,
            item_id,
            item_name,
            quantity,
            price,
            total,
            auth):
        '''Adds sale items given the above arguements. Then returns the sale items of the completed sale'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """INSERT INTO sale_items(sale_id, item_id, item_name, quantity, price, total, created_by)\
                VALUES(%s,%s,%s,%s,%s,%s,%s);"""

        self.cur.execute(
            query,
            (sale_id,
             item_id,
             item_name,
             quantity,
             price,
             total,
             auth))
        self.conn.commit()

        query_confirm = """SELECT * FROM sale_items WHERE sale_id = %s;"""
        self.cur.execute(query_confirm, (sale_id, ))
        self.sale_items = self.cur.fetchall()

        return self.sale_items

    def add_sales(self, payment_mode, items, grand, auth):
        '''Adds sale given the above arguements. Then returns the created sale'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """INSERT INTO sales(payment_mode, number_of_items, grand_total, created_by)\
                VALUES(%s,%s,%s,%s);"""

        self.cur.execute(query, (payment_mode, items, grand, auth))
        self.conn.commit()

        sale_id = self.last_sale_id()

        query_confirm = """SELECT * FROM sales WHERE sale_id = %s;"""
        self.cur.execute(query_confirm, (sale_id, ))
        self.sale = self.cur.fetchone()

        return self.sale

    def last_sale_id(self):
        '''Retrieves the last added sale id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT sale_id FROM sales ORDER BY sale_id DESC LIMIT 1;"""
        self.cur.execute(query)
        sale_id = self.cur.fetchone()
        sale_id = sale_id['sale_id']

        return sale_id

    def get_all_sales(self):
        '''Retrieves all sales records'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sales;"""
        self.cur.execute(query)
        self.sales = self.cur.fetchall()

        return self.sales

    def get_all_sale_items(self):
        '''retrieves all sale items'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sale_items;"""
        self.cur.execute(query)
        self.sale_items = self.cur.fetchall()

        return self.sale_items

    def get_sale_items_by_sale_id(self, sale_id):
        '''retrieves all the sale items from a specific sale by referencing that sales sale id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sale_items WHERE sale_id = %s;"""
        self.cur.execute(query, (sale_id, ))
        self.sale_items = self.cur.fetchall()

        return self.sale_items

    def get_sales_by_sale_id(self, sale_id):
        '''retrieves a sale by using it's sale id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sales WHERE sale_id = %s;"""
        self.cur.execute(query, (sale_id, ))
        self.sale = self.cur.fetchone()

        return self.sale

    def get_sales_by_user_id(self, user_id):
        '''retrieves all the sales made by a specific user by referencing their user id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sales WHERE created_by = %s;"""
        self.cur.execute(query, (user_id, ))
        self.sales = self.cur.fetchall()

        return self.sales


    def get_sales_by_user_id_last_five(self, user_id):
        '''retrieves all the last 5 sales made by a specific user by referencing their user id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sales WHERE created_by = %s ORDER BY sale_id DESC LIMIT 5;"""
        self.cur.execute(query, (user_id, ))
        self.sales = self.cur.fetchall()

        return self.sales


    def get_sales_last_five(self):
        '''retrieves the last 5 sales'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM sales ORDER BY sale_id DESC LIMIT 5;"""
        self.cur.execute(query)
        self.sales = self.cur.fetchall()

        return self.sales


    def count_sales_by_user_id(self, user_id):
        '''counts all the sales made by a specific user by referencing their user id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT COUNT(*) FROM sales WHERE created_by = %s ORDER BY sale_id DESC LIMIT 5;"""
        self.cur.execute(query, (user_id, ))
        self.sales = self.cur.fetchall()

        return self.sales

    def count_sales(self):
        '''counts all the sales'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT COUNT(*) FROM sales;"""
        self.cur.execute(query)
        self.sales = self.cur.fetchall()

        return self.sales
