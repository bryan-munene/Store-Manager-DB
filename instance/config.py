import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET')
    JWT_BLACKLIST_ENABLED = True
    

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    SQL_DATABASE_URL = "dbname='store_manager' host='127.0.0.1' port='5432' user='postgres' password='root'"

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    SQL_DATABASE_URL = "dbname='store_manager_test' host='127.0.0.1' port='5432' user='postgres' password='root'"
    TESTING = True
    DEBUG = True


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True
    SQL_DATABASE_URL = os.getenv('DATABASE_URL')
    

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "DATABASE_URL_TEST": "dbname='store_manager_test' host='127.0.0.1' port='5432' user='postgres' password='root'",
    "DATABASE_URL_LOCAL": "dbname='store_manager' host='127.0.0.1' port='5432' user='postgres' password='root'"
}
