from .db_conn import conn, cur

class ItemsModel():
    
    def add_item(self, name, price, quantity, category, reorder_point):
        query = "INSERT INTO items(name, price, quantity, category, reorder_point)\
                VALUES(%s,%d,%d,%s,%d);"

        cur.execute(query, ('name', 'price', 'quantity', 'category', 'reorder_point'))
        conn.commit()

        query_confirm = "SELECT * FROM items WHERE name LIKE %s AND price LIKE %d;"
        cur.execute(query_confirm, ('email', 'price'))
        self.item = cur.fetchone() 

        return self.item

    def get_all(self):
        query = "SELECT * FROM items;"
        cur.execute(query)
        self.items = cur.fetchall()
        
        return self.items

    def get_by_id(self, item_id):
        query = "SELECT * FROM items WHERE item_id LIKE %d;"
        cur.execute(query, ('item_id'))
        self.item = cur.fetchone()
            
        return self.item

    def get_by_name_and_price(self, name, price):
        query_confirm = "SELECT * FROM items WHERE name LIKE %s AND price LIKE %d;"
        cur.execute(query_confirm, ('email', 'price'))
        self.item = cur.fetchone() 

        return self.item
