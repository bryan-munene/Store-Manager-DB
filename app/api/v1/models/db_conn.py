import os
from manage import DatabaseSetup

config = os.getenv('ENV')


       
class ModelSetup(object):
    '''Sets up db connection'''
    def __init__(self):
        '''initialize connection and cursor'''
        self.db = DatabaseSetup(config)
        self.conn = self.db.conn
        self.cur = self.db.cur