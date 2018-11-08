import os
import psycopg2
import psycopg2.extras
from instance.config import app_config

config = os.getenv('ENV')
print(config)
       
class ModelSetup(object):
    '''Sets up db connection'''
    def __init__(self):
        '''initialize connection and cursor'''
        self.url = app_config[config].SQL_DATABASE_URL
        self.conn = psycopg2.connect(self.url)
        self.cur = self.conn.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
            