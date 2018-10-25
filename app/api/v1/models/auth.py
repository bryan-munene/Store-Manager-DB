from werkzeug.security import generate_password_hash, check_password_hash
from .db_conn import conn, cur


class UserModel():
    
    def add_user(self, name, email, usrnm, pswrd, is_admin):
        self.password = generate_password_hash(pswrd, method='pbkdf2:sha256', salt_length=12)
        query = """INSERT INTO users(name, username, email, password, is_admin)\
                VALUES(%s,%s,%s,%s,%s);"""

        cur.execute(query, ('name', 'usrnm', 'email', self.password, 'is_admin'))
        conn.commit()

        query_confirm = """SELECT * FROM users WHERE email LIKE %s;"""
        cur.execute(query_confirm, ('email'))
        self.user = cur.fetchone()        

        return self.user

    def get_all(self):
        query = """SELECT * FROM users;"""
        cur.execute(query)
        self.users = cur.fetchall()
        return self.users

    def get_user_by_email(self, email):
        query = """SELECT * FROM users WHERE email LIKE %s;"""
        cur.execute(query, ('email'))
        self.user = cur.fetchone()        

        return self.user

    def check_password(self, password):
        query_confirm = """SELECT password FROM users WHERE email LIKE %s;"""
        cur.execute(query_confirm, ('email'))
        self.user_password = cur.fetchone() 
       
        return check_password_hash(self.user_password, password)

    def get_by_id(self, user_id):
        query = """SELECT * FROM items WHERE user_id LIKE %d;"""
        cur.execute(query, ('user_id'))
        self.users = cur.fetchone()
            
        return self.users