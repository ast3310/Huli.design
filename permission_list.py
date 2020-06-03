from core.permissions import BasePеrmission
from app import db
import models


class isAdmin(BasePеrmission):
    @staticmethod
    def check(message):
        user = db.session.query(models.Users)\
            .filter(models.Users.user_id == message.user_id)\
            .filter(models.Users.is_admin == True)\
            .first()
        
        if user is None:
            return False
        else:
            return True


class isCustomer(BasePеrmission):
    @staticmethod
    def check(message):
        user = db.session.query(models.Users)\
            .filter(models.Users.user_id == message.user_id)\
            .first()

        if user is not None:
            return False
        else:
            return True


class isManager(BasePеrmission):
    @staticmethod
    def check(message):
        user = db.session.query(models.Users)\
            .filter(models.Users.user_id == message.user_id)\
            .filter(models.Users.role == 'manager')\
            .first()

        if user is None:
            return False
        else:
            return True


class isExecutor(BasePеrmission):
    @staticmethod
    def check(message):
        return not isManager.check(message)\
            and not isCustomer.check(message)


class hasPayload(BasePеrmission):
    @staticmethod
    def check(message):
        if message.payload is None:
            return False
        else:
            return True


class hasForwards(BasePеrmission):
    @staticmethod
    def check(message):
        return message.has_forwards
