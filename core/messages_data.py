import json

class MessageData():
    def __init__(self, id, date, text, chat_id, user_id, is_chat, has_replay, has_forwards, replay, attachments, payload, forwards):
        self.id = id
        self.date = date
        self.text = text
        self.chat_id = chat_id
        self.user_id = user_id
        self.is_chat = is_chat
        self.has_replay = has_replay
        self.has_forwards = has_forwards
        self.attachments = attachments
        self.replay = replay
        self.payload = payload
        self.forwards = forwards


class MessageDataAdapter():
    @staticmethod
    def from_dict(data):
        data = data['object']

        id = data['id']
        date = data['date']
        text = data['text']
        chat_id = data['peer_id']
        user_id = data['from_id']
        is_chat = True if chat_id != user_id else False
        has_replay = True if 'reply_message' in data.keys() else False
        has_forwards = True if 'fwd_messages' in data.keys() else False
        replay = data['reply_message'] if 'reply_message' in data.keys() else None
        forwards = data['fwd_messages'] if 'fwd_messages' in data.keys() else None
        payload = json.loads(data['payload']) if 'payload' in data.keys() else None

        attachments = {}

        for attachment in data['attachments']:
            attachments.update({attachment['type']: []})
            attachments[attachment['type']].append({'id': attachment[attachment['type']]['id'], 'owner_id': attachment[attachment['type']]['owner_id']})
        
        return MessageData(id, date, text, chat_id, user_id, is_chat, has_replay, has_forwards, replay, attachments, payload, forwards)
