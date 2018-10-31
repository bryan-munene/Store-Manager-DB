import os
import psycopg2
import psycopg2.extras
from flask import Flask
from werkzeug.security import generate_password_hash
from instance.config import app_config



class DatabaseSetup(object):
    '''Sets up db connection'''
    def __init__(self, url):
        '''initialize connection and cursor'''
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    def create_tables(self, url):
        '''creates tables by iterating through the list of queries'''
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        queries = self.tables()
        for query in queries:
            try:
                self.cur.execute(query)
            except psycopg2.ProgrammingError as exc:
                print (exc)
                self.conn.rollback()
            except psycopg2.InterfaceError as exc:
                print (exc)
                self.conn = psycopg2.connect(url)
                self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        
    def drop_tables(self, url):
        '''drop tables by iterating through the list of queries'''
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        queries = self.schema()
        for query in queries:
            try:
                self.cur.execute(query)
            except psycopg2.ProgrammingError as exc:
                print (exc)
                self.conn.rollback()
            except psycopg2.InterfaceError as exc:
                print (exc)
                self.conn = psycopg2.connect(url)
                self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def create_default_admin_user(self, url):
        '''creates the base user who is an admin user'''
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        admin = self.check_users(url)
        if not admin:
            password = 'Adm1n234'
            password_hash = generate_password_hash(password, method='sha256')
            query = """INSERT INTO users(name, username, email, password, is_admin)\
                    VALUES(%s,%s,%s,%s,%s);"""

            try:
                self.cur.execute(query, ('test', 'testeradmin', 'test@adminmail.com', password_hash, 'True'))
            except(Exception, psycopg2.DatabaseError) as error:
                print (error)
                try:
                    self.cur.close()
                    self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
                except:
                    self.conn.close()
                    self.conn = psycopg2.connect(url)
                self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

            self.conn.commit()
            self.cur.close()
            self.conn.close()
        else:
            return False
        
        
    def check_users(self, url):
        '''checks if the admin user already exists'''
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
        query = """SELECT * FROM users WHERE email LIKE 'test@adminmail.com';"""
        self.cur.execute(query)
        self.user = self.cur.fetchone()
        
        return self.user

    def tables(self):
        '''creates queries for creation of tables'''
        query1 = """CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY NOT NULL,
            name varchar(20) NOT NULL,
            username varchar(20) NOT NULL,
            email varchar(100) NOT NULL,
            password varchar(300) NOT NULL,
            is_admin varchar(20) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
            UNIQUE(email))
            """

        query2 = """CREATE TABLE IF NOT EXISTS categories (
            category_id serial PRIMARY KEY,
            name varchar(20) NOT NULL,
            description varchar(100),
            created_by integer NOT NULL REFERENCES users(user_id),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """

        query3 = """CREATE TABLE IF NOT EXISTS items (
            item_id serial PRIMARY KEY,
            name varchar(20) NOT NULL,
            price integer NOT NULL,
            quantity integer NOT NULL,
            category integer REFERENCES categories(category_id),
            reorder_point integer NOT NULL,
            created_by integer NOT NULL REFERENCES users(user_id),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        
        query4 = """CREATE TABLE IF NOT EXISTS sales (
            sale_id serial PRIMARY KEY NOT NULL,
            payment_mode varchar(20) NOT NULL,
            number_of_items integer NOT NULL,
            grand_total integer NOT NULL,
            created_by integer NOT NULL REFERENCES users(user_id),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """

        query5 = """CREATE TABLE IF NOT EXISTS sale_items (
            sale_item_id serial PRIMARY KEY NOT NULL,
            sale_id integer NOT NULL REFERENCES sales(sale_id),
            item_id integer NOT NULL REFERENCES items(item_id),
            item_name varchar(20) NOT NULL,
            price integer NOT NULL,
            quantity integer NOT NULL,
            total integer NOT NULL,
            created_by integer NOT NULL REFERENCES users(user_id),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        
        query6 = """CREATE TABLE IF NOT EXISTS blacklist_token (
            token_id serial PRIMARY KEY NOT NULL,
            token varchar(20) NOT NULL)
            """

        queries = [query1, query2, query3, query4, query5, query6]  

        return queries

    def schema(self):
        '''drops the schema and recreates it'''
        query1 = """DROP TABLE IF EXISTS users CASCADE;"""
        query2 = """DROP TABLE IF EXISTS categories CASCADE;"""
        query3 = """DROP TABLE IF EXISTS items CASCADE;"""
        query4 = """DROP TABLE IF EXISTS sales CASCADE;"""
        query5 = """DROP TABLE IF EXISTS sale_items CASCADE;"""
        query6 = """DROP TABLE IF EXISTS blacklist_token CASCADE;"""

        queries = [query1, query2, query3, query4, query5, query6]  

        return queries