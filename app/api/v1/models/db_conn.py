import os
from instance.config import app_config
from manage import DatabaseSetup

url = os.getenv('DATABASE_URL')
db = DatabaseSetup(url)

