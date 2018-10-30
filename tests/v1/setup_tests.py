import os
from app import create_app
from manage import DatabaseSetup


config = "testing"
app = create_app(config)

url = os.getenv('DATABASE_URL_TEST')
db = DatabaseSetup(url)


db.create_tables()
db.create_default_admin_user()