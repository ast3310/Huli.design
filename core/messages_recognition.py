from abc import ABCMeta, abstractmethod, abstractproperty
import json

from core.permissions import PermisionsChecker
from plugins import COMMANDS_LIST


class MessageRecognition():
    def __init__(self):
        self.messages_handlers = COMMANDS_LIST
    
    def recognition(self, message):
        for message_handler in self.messages_handlers:
            if  PermisionsChecker.check(message_handler.permissions, message)\
                and message_handler.check(message):
                message_handler.handle(message)
                break
