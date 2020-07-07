import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from django.db.models import Q

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self, data):
        messages= Message.objects.filter((Q(sender_name=data['username'])&Q(reciever_name=data['friend_name'])) | (Q(sender_name=data['friend_name'])&Q(reciever_name=data['username'])))
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        print(data)
        author = data['from']
        reciever = data['friend_name']
        # author_user = User.objects.filter(username=author)[0]
        # print(author_user)
        print('hi')
        last_id=Message.objects.all().order_by('auto_id').last().auto_id
        print(last_id)
        if not last_id:
            last_id=1
        else:
            last_id=last_id+1
        message = Message.objects.create(auto_id=last_id,sender_name=author, reciever_name=reciever, content=data['message'])
        content = {
            # 'command': 'new_message',
            'messages':  self.message_to_json(message)
        }
        return self.send_chat_message(content)
    
    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id':message.auto_id,
            'sender_name': message.sender_name,
            'reciever_name': message.reciever_name,
            'content': message.content,
            'timestamp':str(message.timestamp)
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('connected wit websocket')
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        print('recieve method called')
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))