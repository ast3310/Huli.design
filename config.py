import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app_dir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(app_dir, 'bot_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class VkConfig:
    TOKEN = '' # токен от группы
    RETURN_STR = '' # строка 
    GROUP_ID = -172913364 # id группы
