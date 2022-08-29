import imp
import json
import re
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        #print(self.scope)
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.user_name=self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'lobby_%s' % self.room_name
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'join_message',
                'message': {
                    'event':"status",
                    "user_name":self.user_name
                }
            }
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'disconnect_message',
                'message': {
                    'event':"status",
                    "user_name":self.user_name
                }
            }
        )
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # sending initial message to the group that the user have been joined;
    def join_message(self,event):
        #print(event)
        res={
            "event":"join",
            "user_name":event['message']['user_name']
        }
        # send the message to websocket
        self.send(text_data=json.dumps(res))
    def disconnect_message(self,event):
        #print(event)
        res={
            "event":"disconnect",
            "user_name":event['message']['user_name']
        }
        # send the message to websocket
        self.send(text_data=json.dumps(res))

    # Receive message from room group
    def chat_message(self, event):
        
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))