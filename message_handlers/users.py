from core.messages_handler import MessageBaseHandler
from config import VkConfig

from app import db, bot
from vk_api import keyboard as vk_key
from vk_api import exceptions as vk_exc

from permission_list import isAdmin

import models
import json

from helpers.carousel import Carousel

class AddUserHandler(MessageBaseHandler):
    permissions = [isAdmin]

    def check(self, message):
        if '!addUser' in message.text:
            return True
        else:
            return False
    
    def handle(self, message):
        command = message.text.split()
        if len(command) == 3:
            try:
                domain = command[2].split('/')[-1]
                user = bot.method('users.get', {'user_ids': domain})[0]
            
                user_id = user['id']
                role = command[1]
            
                users_count = db.session.query(models.Users)\
                    .filter(models.Users.user_id == user_id).count()

                if users_count == 0:
                    user_db = models.Users(user_id = user_id, role=role, is_admin=0)
                    db.session.add(user_db)
                    db.session.commit()

                    bot.method('messages.send', {'peer_id': message.chat_id, \
                        'message': 'Пользователь {} добавлен'.format(user['first_name']), \
                        'random_id': 0})
                else:
                    bot.method('messages.send', {'peer_id': message.chat_id, \
                        'message': 'Пользователь {} уже  был добавлен'.format(user['first_name']), \
                        'random_id': 0})
                
            except vk_exc.ApiError:
                bot.method('messages.send', {'peer_id': message.chat_id, \
                        'message': 'Пользователя c таким адресом не существует', \
                        'random_id': 0})
        else:
            bot.method('messages.send', {'peer_id': message.chat_id, \
                'message': 'Команда неправильно написана', \
                'random_id': 0})


class GetUsersHandler(MessageBaseHandler):
    permissions = [isAdmin]

    def check(self, message):
        if '!getUsers' in message.text:
            return True
        elif message.payload != None:
            if message.payload['type'] == 'nextUsers' or\
            message.payload['type'] == 'сancelUsers':
                return True
        
        return False
    
    def handle(self, message):
        if '!getUsers' in message.text:
            users = self.get_list(message.user_id)
            template = self.get_carousel(users[0])
            users_count = users[1]
            keyboard = self.get_keyboard(users_count, 10)
            
        elif message.payload['type'] == 'nextUsers':
            payload = message.payload['type']
            offset = payload['offset']
            users = self.get_list(message.user_id, offset)
            template = self.get_carousel(users[0])
            users_count = users[1]
            keyboard = self.get_keyboard(users_count, offset+10)

        elif message.payload['type'] == 'сancelUsers':
            keyboard = vk_key.VkKeyboard.get_empty_keyboard()
            
            bot.method('messages.send', {'peer_id': message.chat_id, \
                'message': 'Вы вышли', \
                'keyboard': keyboard, 
                'random_id': 0})
            
            return
        
        bot.method('messages.send', {'peer_id': message.chat_id, \
            'message': 'Вот список пользователей', \
            'keyboard': keyboard, 
            'random_id': 0})

        bot.method('messages.send', {'peer_id': message.chat_id, \
            'message': '{} из {}'.format(str(users[2]), str(users_count)), \
            'template': template,\
            'random_id': 0})


    def get_list(self, user_id, offset=0):
        users = db.session.query(models.Users)\
            .filter(models.Users.user_id != user_id)
        users_count = users.count()
        users = users.limit(10)

        if offset > 0:
            users.offset(offset)
        
        return (users, users_count, users.count())
    
    def get_carousel(self, users):
        carousel = Carousel()

        for user in users:
            user_vk = bot.method('users.get', {'user_ids': user.user_id, 'fields': 'photo_id'})[0]
            keyboard = vk_key.VkKeyboard()

            if user.is_admin == 0:
                keyboard.add_button('Назначить', \
                    vk_key.VkKeyboardColor.POSITIVE,\
                    payload = { 'type': 'toAdminUp', 'user_id': user.id },
                )
            else:
                keyboard.add_button('Разжаловать', \
                    vk_key.VkKeyboardColor.DEFAULT,\
                    payload = { 'type': 'toAdminDown', 'user_id': user.id },
                )
            
            keyboard.add_button('Удалить', \
                vk_key.VkKeyboardColor.NEGATIVE,\
                payload = { 'type': 'deleteUser', 'user_id': user.id },
            )

            buttons = json.loads(keyboard.get_keyboard())['buttons'][0]

            carousel.add_element(title=user_vk['first_name'],\
                description=user.role,\
                buttons=buttons,\
                action={'type': 'open_link', 'link': 'https://vk.com/id{}'.format(user.user_id)}
            )

        return carousel.get_json()
    
    def get_keyboard(self, users_count, offset):
        keyboard = vk_key.VkKeyboard()

        if users_count / 10 > 1:
            keyboard.add_button('Следующие пользователи', \
                vk_key.VkKeyboardColor.POSITIVE,\
                payload = { 'type': 'nextUsers', 'offset': offset},
            )
            keyboard.add_line()
            keyboard.add_button('Выйти из списка', \
                vk_key.VkKeyboardColor.NEGATIVE,\
                payload = { 'type': 'сancelUsers'},
            )

            return keyboard.get_keyboard()
        else:
            return keyboard.get_empty_keyboard()


class DeleteUserHandler(MessageBaseHandler):
    permissions = [isAdmin]

    def check(self, message):
        if message.payload != None:
            if message.payload['type'] == 'deleteUser':
                return True
        return False
    
    def handle(self, message):
        user_id = message.payload['user_id']
        users = db.session.query(models.Users)\
            .filter(models.Users.id == user_id)
        users_count = users.count()
        user = users.first()
        
        text = ''

        if users_count != 0:
            user_vk = bot.method('users.get', {'user_ids': user.user_id, })[0]
            db.session.delete(user)
            db.session.commit()

            text = 'Пользователь {} удален'.format(user_vk['first_name'])
            
        else:
            text = 'Произошла ошибка'
        
        bot.method('messages.send', {'peer_id': message.chat_id, \
                    'message': text, \
                    'random_id': 0})


class AdminChangeUserHandler(MessageBaseHandler):
    permissions = [isAdmin]

    def check(self, message):
        if message.payload != None:
            if message.payload['type'] == 'toAdminUp' or\
                message.payload['type'] == 'toAdminDown':
                return True
        return False
    
    def handle(self, message):
        user_id = message.payload['user_id']
        users = db.session.query(models.Users)\
            .filter(models.Users.id == user_id)
        users_count = users.count()
        user = users.first()

        text = ''

        if users_count != 0:
            user_vk = bot.method('users.get', {'user_ids': user.user_id, })[0]
            
            if message.payload['type'] == 'toAdminUp':
                user.is_admin = 1

                text = 'Пользователь {} стал администратором'.format(user_vk['first_name'])

            elif message.payload['type'] == 'toAdminDown':
                user.is_admin = 0

                text = 'Пользователь {} более не является администратором'.format(user_vk['first_name'])
            
            db.session.commit()
        else:
            text = 'Произошла ошибка'
        
        bot.method('messages.send', {'peer_id': message.chat_id, \
            'message': text, \
            'random_id': 0})
        
