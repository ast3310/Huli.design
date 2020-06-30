from app import db, bot
from permission_list import isCustomer, isAdmin, hasPayload
from vk_api import keyboard as vk_key
from helpers.utils import get_main_keyboard

import models
from config import VkConfig
from core.messages_handler import MessageBaseHandler


class StartHandler(MessageBaseHandler):
    permissions = [hasPayload, isCustomer]

    def check(self, message):
        print(message.payload)
        if 'command' in message.payload:
            if message.payload['command'] == 'start':
                return True
        return False
    
    def handle(self, message):
        user_vk = bot.method('users.get', {'user_ids': message.user_id})[0]

        bot.method('messages.send', {'peer_id': message.user_id, \
            'message': 'Привет, {}! Для того, чтобы сделать заказ или узнать информацию о товаре, нужно зайти в раздел товары и нажать на кнопку "Написать продавцу"'\
            .format(user_vk['first_name']), \
            'random_id': 0})
    

class StartAdminHandler(MessageBaseHandler):
    permissions = [isAdmin]
    
    def check(self, message):
        if '!adminStart' in message.text:
            return True
        return False

    def handle(self, message):
        bot.method('messages.send', {'peer_id': message.user_id, \
            'message': 'Вы активировали режим управления', \
            'keyboard': get_main_keyboard(), \
            'random_id': 0})
