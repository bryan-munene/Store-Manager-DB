from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import datetime
from .db_conn import conn, cur


class UserModel():
    
    def add_user(self, name, email, usrnm, pswrd, is_admin):
        self.password = generate_password_hash(pswrd, method='sha256')
        query = """INSERT INTO users(name, username, email, password, is_admin)\
                VALUES(%s,%s,%s,%s,%s);"""

        cur.execute(query, (name, usrnm, email, self.password, is_admin))
        conn.commit()

        query_confirm = """SELECT * FROM users WHERE email = %s;"""
        cur.execute(query_confirm, (email, ))
        self.user = cur.fetchone()        

        return self.user

    def get_all(self):
        query = """SELECT * FROM users;"""
        cur.execute(query)
        self.users = cur.fetchall()
        return self.users

    def get_user_by_email(self, email):
        query = """SELECT * FROM users WHERE email = %s;"""
        cur.execute(query, (email, ))
        self.user = cur.fetchone()        

        return self.user

    def get_user_by_id(self, user_id):
        query = """SELECT * FROM users WHERE user_id = %d;"""
        cur.execute(query, (user_id))
        self.user = cur.fetchone()        

        return self.user

    def get_user_password_by_email(self, email):
        query = """SELECT password FROM users WHERE email = %s;"""
        cur.execute(query, (email, ))
        self.user = cur.fetchone()        

        return self.user
    
    def get_user_username_by_email(self, email):
        query = """SELECT username FROM users WHERE email = %s;"""
        cur.execute(query, (email, ))
        self.user = cur.fetchone()        

        return self.user

    def get_user_role_by_email(self, email):
        query = """SELECT is_admin FROM users WHERE email = %s;"""
        cur.execute(query, (email, ))
        self.user_role = cur.fetchone()        

        return self.user_role

    def check_credentials(self, user_password_hash, password):
        
        return check_password_hash(user_password_hash, password)

    def get_by_id(self, user_id):
        query = """SELECT * FROM users WHERE user_id = %d;"""
        cur.execute(query, (user_id))
        self.users = cur.fetchone()
            
        return self.users

    def update_user(self, user_id, name, usrnm, pswrd):
        query = """UPDATE users 
                  SET name = %s, username = %s, password = %s
                  WHERE user_id = %d
                """
        cur.execute(query, (name, usrnm, pswrd, user_id))
        conn.commit()

        query_confirm = """SELECT * FROM users WHERE user_id = %d;"""
        cur.execute(query_confirm, (user_id))
        self.user = cur.fetchone()
            
        return self.user

    def update_user_role(self, user_id, is_admin):
        query = """UPDATE users 
                  SET is_admin = %s
                  WHERE user_id = %d
                """
        cur.execute(query, (is_admin, user_id))
        conn.commit()

        query_confirm = """SELECT * FROM users WHERE user_id = %d;"""
        cur.execute(query_confirm, (user_id))
        self.user = cur.fetchone()
            
        return self.user

    def delete_user(self, user_id):
        query = """DELETE FROM users WHERE user_id = %d;;"""
        cur.execute(query, (user_id))

        query_confirm = """SELECT * FROM users WHERE user_id = %d;"""
        cur.execute(query_confirm, (user_id))
        self.user = cur.fetchone()
            
        return self.user

    def access_token(self, email, password):
        self.password_output = self.get_user_password_by_email(email)
        self.password = self.password_output[0]
        credentials = self.check_credentials(self.password, password)
        exp = datetime.timedelta(minutes=15)
        if credentials:
            identity = email
            fresh=True
            token = create_access_token(identity, fresh, exp)
            return token
        return False
