from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
import datetime
from .db_conn import conn, cur


class UserModel():
    def __init__(self, name=None, email=None, usrnm=None, pswrd=None, is_admin=None, user_id=None):
        self.name = name
        self.email = email
        self.username = usrnm
        self.pswrd = pswrd
        self.is_admin = is_admin
        self.user_id = user_id

    def add_user(self, name, email, usrnm, pswrd, is_admin):
        self.password = generate_password_hash(pswrd, method='sha256')
        query = """INSERT INTO users(name, username, email, password, is_admin)\
                VALUES(%s,%s,%s,%s,%s);"""

        cur.execute(query, (name, usrnm, email, self.password, is_admin))
        conn.commit()

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users WHERE email = %s;"""
        cur.execute(query_confirm, (email, ))
        self.user = cur.fetchone()        

        return self.user

    def get_all(self):
        query = """SELECT user_id, name, username, email, is_admin FROM users;"""
        cur.execute(query)
        self.users = cur.fetchall()
        return self.users

    def get_user_by_email(self, email):
        query = """SELECT user_id, name, username, email, is_admin FROM users WHERE email = %s;"""
        cur.execute(query, (email, ))
        self.user = cur.fetchone()        

        return self.user

    def get_user_by_id(self, user_id):
        query = """SELECT user_id, name, username, email, is_admin FROM users WHERE user_id = %s;"""
        cur.execute(query, (user_id, ))
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

    def get_user_id_by_email(self, email):
        query = """SELECT user_id FROM users WHERE email = %s;"""
        cur.execute(query, (email, ))
        self.users = cur.fetchone()
            
        return self.users

    def update_user(self, user_id, name, usrnm, pswrd):
        self.password = generate_password_hash(pswrd, method='sha256')
        query = """UPDATE users 
                  SET name = %s, username = %s, password = %s
                  WHERE user_id = %s;
                """
        cur.execute(query, (name, usrnm, self.password, user_id))
        conn.commit()

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users WHERE user_id = %s;"""
        cur.execute(query_confirm, (user_id, ))
        self.user = cur.fetchone()
            
        return self.user

    def update_user_role(self, user_id, is_admin):
        query = """UPDATE users 
                  SET is_admin = %s
                  WHERE user_id = %s
                """
        cur.execute(query, (is_admin, user_id))
        conn.commit()

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users WHERE user_id = %s;"""
        cur.execute(query_confirm, (user_id, ))
        self.user = cur.fetchone()
            
        return self.user

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        print(user)
        if user:
            query = """DELETE FROM users WHERE user_id = %s;"""
            cur.execute(query, (user_id, ))
        else:
            return False

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users;"""
        cur.execute(query_confirm, (user_id, ))
        self.user = cur.fetchall()
            
        return self.user

    def access_token(self, email, password):
        self.password_output = self.get_user_password_by_email(email)
        self.password = self.password_output['password']
        self.user = self.get_user_by_email(email)
        credentials = self.check_credentials(self.password, password)
        if credentials:
            identity = self.user
            fresh=True
            exp = datetime.timedelta(minutes=900)
            token = create_access_token(identity, fresh, exp)
            return token
        return False
