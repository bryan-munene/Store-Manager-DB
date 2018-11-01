import os
import psycopg2
from flask import Flask
from werkzeug.security import generate_password_hash
from instance.config import app_config


url = os.getenv('DATABASE_URL')

print (url)
class DatabaseSetup(object):
    '''Sets up db connection'''
    def __init__(self, url):
        self.conn = psycopg2.connect(url)
        self.cur = self.conn.cursor()

    
    def create_tables(self):
        queries = self.tables()
        for query in queries:
            self.cur.execute(query)
        self.conn.commit()
        self.cur.close()
        self.conn.close()


    def create_default_admin_user(self):
        password_hash = generate_password_hash('Adm1n234')
        query = "INSERT INTO users(name, username, email, password, is_admin)\
                VALUES(%s,%s,%s,%s,%s);"

        self.cur.execute(query, ('test', 'testeradmin',
                             'test@adminmail.com', password_hash, 'True'))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    
    def commit(self):
        '''commits changes to db'''
        self.conn.commit()

    def tables(self):

        query1 = """CREATE TABLE IF NOT EXISTS users (
            user_id serial PRIMARY KEY NOT NULL,
            name varchar(20) NOT NULL,
            username varchar(20) NOT NULL,
            email varchar(100) NOT NULL,
            password varchar(300) NOT NULL,
            is_admin varchar(20) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """

        query2 = """CREATE TABLE IF NOT EXISTS items (
            product_id serial PRIMARY KEY,
            name varchar(20) NOT NULL,
            price integer,
            price integer,
            quantity integer NOT NULL,
            category varchar(20),
            reorder_point integer NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        
        query3 = """CREATE TABLE IF NOT EXISTS categories (
            category_id serial PRIMARY KEY,
            name varchar(20) NOT NULL,
            description varchar(100),
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """
        
        query4 = """CREATE TABLE IF NOT EXISTS sales (
            sale_id serial PRIMARY KEY NOT NULL,
            payment_mode varchar(20) NOT NULL,
            number_of_items integer NOT NULL,
            grand_total integer NOT NULL,
            created_by varchar(20) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """

        query5 = """CREATE TABLE IF NOT EXISTS sale_items (
            sale_item_id serial PRIMARY KEY NOT NULL,
            sale_id integer NOT NULL,
            item_id integer NOT NULL,
            item_name varchar(20) NOT NULL,
            quantity integer NOT NULL,
            price integer NOT NULL,
            total integer NOT NULL,
            created_by varchar(20) NOT NULL,
            date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL)
            """

        queries = [query1, query2, query3, query4,query5]  
        
        return queries