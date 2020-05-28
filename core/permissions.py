from abc import ABCMeta, abstractmethod, abstractproperty

class PermisionsChecker():
    @staticmethod
    def check(permissions, message):
        for permission in permissions:
            return permission.check(message)
        return True


class BasePеrmission():
    @staticmethod
    def check(message):
        pass
