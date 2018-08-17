import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    VERSION = '1.0.0'
    UPLOAD_PATH = 'uploads/'

class Development(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'

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
