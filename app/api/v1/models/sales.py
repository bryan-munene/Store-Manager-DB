from .db_conn import conn, cur
sale_items_temp = []


class SalesModel():
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
        query = """INSERT INTO sale_items(sale_id, item_id, item_name, quantity, price, total, created_by)\
                VALUES(%s,%s,%s,%s,%s,%s,%s);"""

        cur.execute(
            query,
            (sale_id,
             item_id,
             item_name,
             quantity,
             price,
             total,
             auth))
        conn.commit()

        query_confirm = """SELECT * FROM sale_items WHERE sale_id = %s;"""
        cur.execute(query_confirm, (sale_id, ))
        self.sale_items = cur.fetchall()

        return self.sale_items

    def add_sales(self, payment_mode, items, grand, auth):
        '''Adds sale given the above arguements. Then returns the created sale'''
        query = """INSERT INTO sales(payment_mode, number_of_items, grand_total, created_by)\
                VALUES(%s,%s,%s,%s);"""

        cur.execute(query, (payment_mode, items, grand, auth))
        conn.commit()

        sale_id = self.last_sale_id()

        query_confirm = """SELECT * FROM sales WHERE sale_id = %s;"""
        cur.execute(query_confirm, (sale_id, ))
        self.sale = cur.fetchone()

        return self.sale

    def last_sale_id(self):
        '''Retrieves the last added sale id'''
        query = """SELECT sale_id FROM sales ORDER BY sale_id DESC LIMIT 1;"""
        cur.execute(query)
        sale_id = cur.fetchone()
        sale_id = sale_id['sale_id']

        return sale_id

    def get_all_sales(self):
        '''Retrieves all sales records'''
        query = """SELECT * FROM sales;"""
        cur.execute(query)
        self.sales = cur.fetchall()

        return self.sales

    def get_all_sale_items(self):
        '''retrieves all sale items'''
        query = """SELECT * FROM sale_items;"""
        cur.execute(query)
        self.sale_items = cur.fetchall()

        return self.sale_items

    def get_sale_items_by_sale_id(self, sale_id):
        '''retrieves all the sale items from a specific sale by referencing that sales sale id'''
        query = """SELECT * FROM sale_items WHERE sale_id = %s;"""
        cur.execute(query, (sale_id, ))
        self.sale_items = cur.fetchall()

        return self.sale_items

    def get_sales_by_sale_id(self, sale_id):
        '''retrieves a sale by using it's sale id'''
        query = """SELECT * FROM sales WHERE sale_id = %s;"""
        cur.execute(query, (sale_id, ))
        self.sale = cur.fetchone()

        return self.sale

    def get_sales_by_user_id(self, user_id):
        '''retrieves all the sales made by a specific user by referencing their user id'''
        query = """SELECT * FROM sales WHERE created_by = %s;"""
        cur.execute(query, (user_id, ))
        self.sales = cur.fetchall()

        return self.sales
