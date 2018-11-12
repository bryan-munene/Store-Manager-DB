import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = " \87b\0ha\j&^\*kd\fg4\ugy\8gq\4tt\0nj\bga\g$%\^&*\()d\l*7\*&^\&$%\bjd\bnj\bns\236\7$%\^&*\()i\nkn\fgs\dgj\n4k\*&6\%gb\hbj\fgh\}|p\POI\IUP\dhf\jhb\&*(\!@#\@#l\LMk\ "
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
    "production": ProductionConfig
}
