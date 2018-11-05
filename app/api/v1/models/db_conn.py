import os
from flask import current_app
from instance.config import app_config
from manage import DatabaseSetup

config = os.getenv('ENV')
print(config)
        
db = DatabaseSetup(config)

conn = db.conn
cur = db.cur
