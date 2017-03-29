import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    VERSION = '2.0.2'

class Development(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Digio123'

class Testing(Config):
    TESTING = True

class Production(Config):
    pass

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
