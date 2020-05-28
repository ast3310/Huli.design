from flask import Flask
from config import BaseConfig, VkConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from vk_api import VkApi


app = Flask(__name__)
app.config.from_object(BaseConfig)

bot = VkApi(token=VkConfig.TOKEN)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
