# from .db_conn import conn, cur


class CategoriesModel():
    '''Handles the data logic of the categories section'''
    def __init__(
            self,
            name=None,
            description=None,
            auth=None,
            category_id=None):
        '''Initializes the variables for the categories class'''
        self.name = name
        self.description = description
        self.auth = auth
        self.category_id = category_id

    def add_category(self, name, description, auth):
        '''Adds category given the above arguements. Then returns the created category'''
        query = """INSERT INTO categories(name, description, created_by)\
                VALUES(%s,%s,%s);"""

        cur.execute(query, (name, description, auth))
        conn.commit()

        query_confirm = """SELECT * FROM categories WHERE name LIKE %s;"""
        cur.execute(query_confirm, (name, ))
        self.category = cur.fetchone()

        return self.category

    def get_all(self):
        '''gets all records of categories in the databas and returns them'''
        query = """SELECT * FROM categories;"""
        cur.execute(query)
        self.categories = cur.fetchall()

        return self.categories

    def get_by_id(self, category_id):
        '''retrieves one category by finding them using their unique user_id'''
        query = """SELECT * FROM categories WHERE category_id = %s;"""
        cur.execute(query, (category_id, ))
        self.category = cur.fetchone()

        return self.category

    def get_by_name(self, name):
        '''retrieves one category by finding them using their unique name'''
        query = """SELECT * FROM categories WHERE name LIKE %s;"""
        cur.execute(query, (name, ))
        self.category = cur.fetchone()

        return self.category

    def update_category(self, category_id, name, description):
        '''updates category's details'''
        query = """UPDATE categories
                  SET name = %s, description = %s
                  WHERE category_id= %s
                """
        cur.execute(query, (name, description, category_id))
        conn.commit()

        query_confirm = """SELECT * FROM categories WHERE category_id = %s;"""
        cur.execute(query_confirm, (category_id, ))
        self.category = cur.fetchone()

        return self.category

    def delete_category(self, category_id):
        '''deletes a category by finding them using the category_id'''
        query = """DELETE FROM categories WHERE category_id = %s"""
        cur.execute(query, (category_id, ))
        conn.commit()

        query_confirm = """SELECT * FROM categories;"""
        cur.execute(query_confirm)
        self.categories = cur.fetchall()

        return self.categories
