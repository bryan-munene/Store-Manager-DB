import os
from manage import DatabaseSetup


       
class ModelSetup(DatabaseSetup):
    '''Sets up db connection'''
    def __init__(self):
        '''initialize connection and cursor'''
        self.db = DatabaseSetup()
        self.conn = self.db.conn
        self.cur = self.db.cur