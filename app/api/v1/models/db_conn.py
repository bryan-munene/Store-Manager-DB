import os
from instance.config import app_config
from manage import DatabaseSetup

config = os.getenv('ENV')
print(config)
if config:        
    db = DatabaseSetup(config)

    conn = db.conn
    cur = db.cur
else:
    config = os.getenv('ENV')