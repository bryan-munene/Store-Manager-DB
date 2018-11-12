from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity)
import datetime
from .db_conn import ModelSetup


class UserModel(ModelSetup):
    '''Handles the data logic of the users section'''
    def __init__(
            self,
            name=None,
            email=None,
            usrnm=None,
            pswrd=None,
            is_admin=None,
            user_id=None):
        '''Initializes the variables for the user class'''
        self.name = name
        self.email = email
        self.username = usrnm
        self.pswrd = pswrd
        self.is_admin = is_admin
        self.user_id = user_id

    def add_user(self, name, email, usrnm, pswrd, is_admin):
        '''Adds user given the above arguements. Then returns the created user'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        self.password = generate_password_hash(pswrd)
        query = """INSERT INTO users(name, username, email, password, is_admin)\
                VALUES(%s,%s,%s,%s,%s);"""

        self.cur.execute(query, (name, usrnm, email, self.password, is_admin))
        self.conn.commit()

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users WHERE email = %s;"""
        self.cur.execute(query_confirm, (email, ))
        self.user = self.cur.fetchone()

        return self.user

    def get_all(self):
        '''gets all records of users in the databas and returns them'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT user_id, name, username, email, is_admin FROM users;"""
        self.cur.execute(query)
        self.users = self.cur.fetchall()
        return self.users

    def get_user_by_email(self, email):
        '''retrieves one user by finding them using their unique email'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT user_id, name, username, email, is_admin FROM users WHERE email = %s;"""
        self.cur.execute(query, (email, ))
        self.user = self.cur.fetchone()

        return self.user

    def get_user_by_id(self, user_id):
        '''retrieves one user by finding them using their unique user_id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT user_id, name, username, email, is_admin FROM users WHERE user_id = %s;"""
        self.cur.execute(query, (user_id, ))
        self.user = self.cur.fetchone()

        return self.user

    def get_user_password_by_email(self, email):
        '''retrieves a user's password by finding it using their unique email'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT password FROM users WHERE email = %s;"""
        self.cur.execute(query, (email, ))
        self.user = self.cur.fetchone()

        return self.user

    def get_user_username_by_email(self, email):
        '''retrieves a user's username by finding it using their unique email'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT username FROM users WHERE email = %s;"""
        self.cur.execute(query, (email, ))
        self.user = self.cur.fetchone()

        return self.user

    def get_user_role_by_email(self, email):
        '''retrieves a user's role by finding it using their unique email'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT is_admin FROM users WHERE email = %s;"""
        self.cur.execute(query, (email, ))
        self.user_role = self.cur.fetchone()

        return self.user_role

    def check_credentials(self, user_password_hash, password):

        return check_password_hash(user_password_hash, password)

    def get_user_id_by_email(self, email):
        '''retrieves a user's user_id by finding it using their unique email'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT user_id FROM users WHERE email = %s;"""
        self.cur.execute(query, (email, ))
        self.users = self.cur.fetchone()

        return self.users

    def update_user(self, user_id, name, usrnm, pswrd):
        '''updates user's details except for the role'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        self.password = generate_password_hash(pswrd)
        query = """UPDATE users
                  SET name = %s, username = %s, password = %s
                  WHERE user_id = %s;
                """
        self.cur.execute(query, (name, usrnm, self.password, user_id))
        self.conn.commit()

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users WHERE user_id = %s;"""
        self.cur.execute(query_confirm, (user_id, ))
        self.user = self.cur.fetchone()

        return self.user

    def update_user_role(self, user_id, is_admin):
        '''updates user's role'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """UPDATE users
                  SET is_admin = %s
                  WHERE user_id = %s
                """
        self.cur.execute(query, (is_admin, user_id))
        self.conn.commit()

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users WHERE user_id = %s;"""
        self.cur.execute(query_confirm, (user_id, ))
        self.user = self.cur.fetchone()

        return self.user

    def delete_user(self, user_id):
        '''deletes a user by finding them using the user_id'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        user = self.get_user_by_id(user_id)

        if user:
            query = """DELETE FROM users WHERE user_id = %s;"""
            self.cur.execute(query, (user_id, ))
        else:
            return False

        query_confirm = """SELECT user_id, name, username, email, is_admin FROM users;"""
        self.cur.execute(query_confirm, (user_id, ))
        self.user = self.cur.fetchall()

        return self.user

    def access_token(self, email, password):
        '''creates user access token if all the credentials are right'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        self.password_output = self.get_user_password_by_email(email)
        self.password = self.password_output['password']
        self.user = self.get_user_by_email(email)
        credentials = self.check_credentials(self.password, password)
        if credentials:
            identity = self.user
            fresh = True
            exp = datetime.timedelta(minutes=900)
            token = create_access_token(identity, fresh, exp)
            return token
        return False

class BlacklistModel(ModelSetup):
    '''Handles the blaclisting of tokens'''
    def __init__(self, jti=None):
        '''Initializes the variables for the blacklist class'''
        self.jti = jti

    def blacklist_token(self, jti):
        '''adds token to blacklist'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """INSERT INTO blacklist_token (token) VALUES (%s);"""
        self.cur.execute(query, (jti, ))
        self.conn.commit()

    def blacklisted_token(self, jti):
        '''checks if token is blacklisted'''
        model = ModelSetup()
        self.conn = model.conn
        self.cur = model.cur
        query = """SELECT * FROM blacklist_token WHERE token = %s;"""
        self.cur.execute(query, (jti, ))
        result = bool(self.cur.fetchone())

        return result