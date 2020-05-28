from app import app
from flask import request
import json
import config
from core.messages_data import MessageDataAdapter
from core.messages_recognition import MessageRecognition

@app.route('/', methods=['GET', 'POST'])
def index():
    data = json.loads(request.data.decode("utf-8"))

    if data['type'] == 'confirmation':
        return config.VkConfig.RETURN_STR
    elif data['type'] == 'message_new':
        message = MessageDataAdapter.from_dict(data)
        message_recognition = MessageRecognition()
        message_recognition.recognition(message)

        return 'ok'
