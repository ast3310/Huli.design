from app import db, bot
from permission_list import isCustomer, isAdmin, hasForwards
import models
from vk_api import exceptions as vk_exc
from vk_api import keyboard as vk_key
from config import VkConfig
from core.messages_handler import MessageBaseHandler

class NewOrderHandler(MessageBaseHandler):
    permissions = [isCustomer]

    def check(self, message):
        if 'market' in message.attachments:
            if message.attachments['market'][0]['owner_id'] == VkConfig.GROUP_ID:
                return True
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


class AddOrderHandler(MessageBaseHandler):
    permissions = [isAdmin, hasForwards]

    def check(self, message):
        command, _ = self.parse_command(message.text)
        if '!addOrder' in command:
            return True
        return False
    
    def handle(self, message):
        command, args = self.parse_command(message.text)
        text = ''

        if args is not None and len(args) == 2:
            try:
                domain = args[1].split('/')[-1]
                customer = bot.method('users.get', {'user_ids': domain})[0]
            
                customer_id = customer['id']
                role = args[0]

                ts = message.forwards[0]['text']
            
                order_db = models.Orders(customer_id = customer_id, ts=ts, status='searching')
                db.session.add(order_db)
                db.session.commit()

                order_id = order_db.id

                text = 'Заказ добавлен'
                
                executors = db.session.query(models.Users)\
                    .filter(models.Users.role == role)
        
                for executor in executors:
                    bot.method('messages.send', {'peer_id': executor.user_id, \
                        'message': 'К вам пришел новый заказ', \
                        'keyboard': self.get_keyboard(order_id), \
                        'random_id': 0})

                    bot.method('messages.send', {'peer_id': executor.user_id, \
                        'message': 'Техническое задание:\n{}'.format(ts), \
                        'random_id': 0})

            except vk_exc.ApiError:
                text = 'Пользователя c таким адресом не существует'
        else:
            text = 'Команда неправильно написана'
        
        bot.method('messages.send', {'peer_id': message.chat_id, \
            'message': text, \
            'random_id': 0})
                    

    def get_keyboard(self, order_id):
        keyboard = vk_key.VkKeyboard(inline=True)

        keyboard.add_button('Взять заказ', \
            vk_key.VkKeyboardColor.POSITIVE,\
            payload = { 'type': 'acceptOrders', 'order_id': order_id},
        )

        return keyboard.get_keyboard()