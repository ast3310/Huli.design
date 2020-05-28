from abc import ABCMeta, abstractmethod, abstractproperty

class MessageBaseHandler():
    __metaclass__ = ABCMeta

    @abstractmethod
    def check(self, message):
        pass

    @abstractmethod
    def handle(self, message):
        pass
    

