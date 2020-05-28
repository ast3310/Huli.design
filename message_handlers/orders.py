from app import db, bot
from permission_list import isCustomer
import models
from config import VkConfig
from core.messages_handler import MessageBaseHandler

class NewOrderHandler(MessageBaseHandler):
    permissions = [isCustomer]

    def check(self, message):
        if 'market' in message.attachments:
            if message.attachments['market'][0]['owner_id'] == VkConfig.GROUP_ID:
                return True
            else:
                return False
        else:
            return False
    
    def handle(self, message):
        bot.method('messages.send', {'peer_id': message.chat_id, 'message': 'Ваш заказ принят, ждите менеджера', 'random_id': 0})
        managers = db.session.query(models.Users)\
                .filter(models.Users.role == 'manager')
        
        for manager in managers:
            bot.method('messages.send', {'peer_id': manager.user_id, \
                'message': 'К вам пришел новый клиент: @id{}'.format(str(manager.user_id)), \
                'forward_messages': message.id, \
                'random_id': 0})