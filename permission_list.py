from core.permissions import BasePеrmission
from app import db
import models

class isAdmin(BasePеrmission):
    @staticmethod
    def check(message):
        users_count = db.session.query(models.Users)\
            .filter(models.Users.user_id == message.user_id)\
            .filter(models.Users.is_admin == 1)\
            .count()

        if users_count == 0:
            return False
        else:
            return True

class isCustomer(BasePеrmission):
    @staticmethod
    def check(message):
        users_count = db.session.query(models.Users)\
            .filter(models.Users.user_id == message.user_id)\
            .count()

        if users_count == 0:
            return True
        else:
            return False