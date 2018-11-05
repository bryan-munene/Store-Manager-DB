from .db_conn import conn, cur


class ItemsModel():
    '''Handles the data logic of the items section'''
    def __init__(
            self,
            name=None,
            price=None,
            quantity=None,
            category_id=None,
            reorder_point=None,
            auth=None):
        '''Initializes the variables for the items class'''
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        self.reorder_point = reorder_point
        self.auth = auth

    def add_item(
            self,
            name,
            price,
            quantity,
            image,
            category_id,
            reorder_point,
            auth):
        '''Adds item given the above arguements. Then returns the created item'''
        query = """INSERT INTO items(name, price, quantity, image, category, reorder_point, created_by)\
                VALUES(%s,%s,%s,%s,%s,%s,%s);"""

        cur.execute(
            query,
            (name,
             price,
             quantity,
             image,
             category_id,
             reorder_point,
             auth))
        conn.commit()

        query_confirm = """SELECT * FROM items WHERE name = %s AND price = %s;"""
        cur.execute(query_confirm, (name, price))
        self.item = cur.fetchone()

        return self.item

    def get_all(self):
        '''gets all records of items in the databas and returns them'''
        query = """SELECT * FROM items;"""
        cur.execute(query)
        self.items = cur.fetchall()

        return self.items

    def get_by_id(self, item_id):
        '''retrieves one item by finding them using their unique item_id'''
        query = """SELECT * FROM items WHERE item_id = %s;"""
        cur.execute(query, (item_id, ))
        self.item = cur.fetchone()

        return self.item

    def get_by_category(self, category):
        '''retrieves items by finding them using their category. all items in the same category are retrieved'''
        query = """SELECT * FROM items WHERE category LIKE %s;"""
        cur.execute(query, (category))
        self.item = cur.fetchall()

        return self.item

    def get_by_name_and_price(self, name, price):
        '''retrieves one item by finding them using their unique unique combination'''
        query = """SELECT * FROM items WHERE name LIKE %s AND price = %s;"""
        cur.execute(query, (name, price))
        self.item = cur.fetchone()

        return self.item

    def update_item(
            self,
            item_id,
            price,
            quantity,
            image,
            category_id,
            reorder_point,
            auth):
        '''updates item's details. the values in the db are changed to what is provided'''
        query = """UPDATE items
                  SET price = %s, quantity = %s, image = %s, category = %s, reorder_point = %s, created_by = %s
                  WHERE item_id= %s
                """
        cur.execute(
            query,
            (price,
             quantity,
             image,
             category_id,
             reorder_point,
             auth,
             item_id))
        conn.commit()

        query_confirm = """SELECT * FROM items WHERE item_id = %s;"""
        cur.execute(query_confirm, (item_id, ))
        self.item = cur.fetchone()

        return self.item

    def update_item_quantity(self, item_id, quantity):
        '''updates item's quantity.adds the quantity added to the quantity available'''
        query = """UPDATE items
                  SET quantity = %s
                  WHERE item_id= %s
                """
        cur.execute(query, (quantity, item_id))
        conn.commit()

        query_confirm = """SELECT * FROM items WHERE item_id = %s;"""
        cur.execute(query_confirm, (item_id, ))
        self.item = cur.fetchone()

        return self.item

    def delete_item(self, item_id):
        '''deletes an item by finding them using the item_id'''
        query = """DELETE FROM items WHERE item_id = %s"""
        cur.execute(query, (item_id, ))
        conn.commit()

        query_confirm = """SELECT * FROM items;"""
        cur.execute(query_confirm)
        self.items = cur.fetchall()

        return self.items
