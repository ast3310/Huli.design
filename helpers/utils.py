from vk_api import keyboard as vk_key

def get_main_keyboard():
    keyboard = vk_key.VkKeyboard()

    keyboard.add_button('Список пользователей', \
        vk_key.VkKeyboardColor.POSITIVE,\
        payload = { 'type': 'getUsers'},
    )

    return keyboard.get_keyboard()