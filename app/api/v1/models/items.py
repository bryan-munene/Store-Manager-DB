from .db_conn import conn, cur

class ItemsModel():
    
    def add_item(self, name, price, quantity, category, reorder_point):
        query = """INSERT INTO items(name, price, quantity, category, reorder_point)\
                VALUES(%s,%d,%d,%s,%d);"""

        cur.execute(query, ('name', 'price', 'quantity', 'category', 'reorder_point'))
        conn.commit()

        query_confirm = """SELECT * FROM items WHERE name LIKE %s AND price = %d;"""
        cur.execute(query_confirm, (name, price))
        self.item = cur.fetchone() 

        return self.item

    def get_all(self):
        query = """SELECT * FROM items;"""
        cur.execute(query)
        self.items = cur.fetchall()
        
        return self.items

    def get_by_id(self, item_id):
        query = """SELECT * FROM items WHERE item_id = %d;"""
        cur.execute(query, (item_id))
        self.item = cur.fetchone()
            
        return self.item

    def get_by_category(self, category):
        query = """SELECT * FROM items WHERE category LIKE %s;"""
        cur.execute(query, (category))
        self.item = cur.fetchall()
            
        return self.item

    def get_by_name_and_price(self, name, price):
        query = """SELECT * FROM items WHERE name LIKE %s AND price = %d;"""
        cur.execute(query, (name, price))
        self.item = cur.fetchone() 

        return self.item

    def update_item(self, item_id, price, quantity, category, reorder_point):
        query = """UPDATE items 
                  SET name = %s, price = %d, quantity = %d, category = %s, reorder_point = %d 
                  WHERE item_id= %d
                """
        cur.execute(query, (name, price, quantity, category, reorder_point, item_id))
        conn.commit()

        query_confirm = """SELECT * FROM items WHERE item_id = %d;"""
        cur.execute(query_confirm, (item_id))
        self.item = cur.fetchone()
            
        return self.item

    def update_item_quantity(self, item_id, quantity):
        query = """UPDATE items 
                  SET quantity = %d
                  WHERE item_id= %d
                """
        cur.execute(query, (quantity, item_id))
        conn.commit()

        query_confirm = """SELECT * FROM items WHERE item_id = %d;"""
        cur.execute(query_confirm, (item_id))
        self.item = cur.fetchone()
            
        return self.item

    def delete_item(self, item_id):
        query = """DELETE FROM items WHERE item_id = %s"""
        cur.execute(query, (item_id))
        conn.commit()

        query_confirm = """SELECT * FROM items;"""
        cur.execute(query_confirm)
        self.items = cur.fetchall()
            
        return self.items
