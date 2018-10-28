from .db_conn import conn, cur

class CategoriesModel():
    
    def add_category(self, name, description):
        query = """INSERT INTO categories(name, description)\
                VALUES(%s,%s);"""

        cur.execute(query, ('name', 'description'))
        conn.commit()

        query_confirm = """SELECT * FROM categories WHERE name LIKE %s;"""
        cur.execute(query_confirm, (name))
        self.category = cur.fetchone() 

        return self.category

    def get_all(self):
        query = """SELECT * FROM categories;"""
        cur.execute(query)
        self.categories = cur.fetchall()
        
        return self.categories

    def get_by_id(self, category_id):
        query = """SELECT * FROM categories WHERE category_id = %d;"""
        cur.execute(query, (category_id))
        self.category = cur.fetchone()
            
        return self.category

    def get_by_name(self, name):
        query = """SELECT * FROM categories WHERE name LIKE %s;"""
        cur.execute(query, (name))
        self.category = cur.fetchone() 

        return self.category

    def update_category(self, category_id, name, description):
        query = """UPDATE categories 
                  SET name = %s, description = %s 
                  WHERE category_id= %d
                """
        cur.execute(query, (name, description, category_id))
        conn.commit()

        query_confirm = """SELECT * FROM categories WHERE category_id = %d;"""
        cur.execute(query_confirm, (category_id))
        self.category = cur.fetchone()
            
        return self.category


    def delete_category(self, category_id):
        query = """DELETE FROM categories WHERE category_id = %s"""
        cur.execute(query, (category_id))
        conn.commit()

        query_confirm = """SELECT * FROM categories;"""
        cur.execute(query_confirm)
        self.categories = cur.fetchall()
            
        return self.categories
