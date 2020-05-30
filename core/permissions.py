from abc import ABCMeta, abstractmethod, abstractproperty

class PermisionsChecker():
    @staticmethod
    def check(permissions, message):
        for permission in permissions:
            if permission.check(message) == False:
                return False
        return True


class BasePеrmission():
    @staticmethod
    def check(message):
        pass
