from .db_conn import conn, cur

class SalesModel():
        
    def add_sale_items(self, sale_id, item_id, item_name, quantity, price, total):
        query = """INSERT INTO sale_items(sale_id, item_id, item_name, quantity, price, total)\
                VALUES(%d,%d,%s,%d,%d,%d);"""

        cur.execute(query, ('sale_id', 'item_id', 'item_name', 'quantity', 'price', 'total'))
        conn.commit()

        query_confirm = """SELECT * FROM sale_items WHERE sale_id LIKE %d;"""
        cur.execute(query_confirm, ('sale_id'))
        self.sale_items = cur.fetchone() 

        return self.sale_items

    def add_sales(self, payment_mode, number_of_items, grand_total, auth):
        query = """INSERT INTO sales(payment_mode, number_of_items, grand_total, created_by)\
                VALUES(%d,%d,%s,%d,%d,%d);"""

        cur.execute(query, ('payment_mode', 'items', 'grand', 'auth'))
        conn.commit()

        sale_id = self.last_sale_id()

        query_confirm = """SELECT * FROM sales WHERE sale_id LIKE %d;"""
        cur.execute(query_confirm, ('sale_id'))
        self.sale = cur.fetchone()

        return self.sale

    def last_sale_id(self):
        query = """SELECT sale_id FROM sales ORDER BY sale_id DESC LIMIT 1;"""
        cur.execute(query)
        sale_id = cur.fetchall()
        
        return sale_id

    def get_all_sales(self):
        query = """SELECT * FROM sales;"""
        cur.execute(query)
        self.sales = cur.fetchall()
        
        return self.sales

    def get_all_sale_items(self):
        query = """SELECT * FROM sale_items;"""
        cur.execute(query)
        self.sale_items = cur.fetchall() 

        return self.sale_items
        
    def get_sale_items_by_sale_id(self, sale_id):
        query = """SELECT * FROM sale_items WHERE sale_id LIKE %d;"""
        cur.execute(query, ('sale_id'))
        self.sale_items = cur.fetchall() 

        return self.sale_items
        

    def get_sales_by_sale_id(self, sale_id):
        query = """SELECT * FROM sales WHERE sale_id LIKE %d;"""
        cur.execute(query, ('sale_id'))
        self.sale = cur.fetchone() 

        return self.sale
            

    