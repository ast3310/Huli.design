import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(12).hex()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(app_dir, 'bot_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class VkConfig:
    TOKEN = os.environ.get('TOKEN')
    RETURN_STR = os.environ.get('RETURN_STR')
    GROUP_ID = int(os.environ.get('GROUP_ID'))
