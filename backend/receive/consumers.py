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
        
        #this is highlight as user doesnt needed to know if he is connected to webscoket 
        # but has to know about if it is connected to peerconnection
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'join_message',
        #         'message': {
        #             'event':"status",
        #             "user_name":self.user_name
        #         }
        #     }
        # )
        self.accept()

    def disconnect(self, close_code):
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'disconnect_message',
        #         'message': {
        #             'event':"status",
        #             "user_name":self.user_name
        #         }
        #     }
        # )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data)
        action=text_data_json['action']
        if action=="new-peer":
            receive_channel_name=self.channel_name
            text_data_json['message']['reciver_channel_name']=receive_channel_name

            # Send message to room group
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': text_data_json
                }
            )
            
        elif action=='new-offer':
            
            
            reciver_channel_name=text_data_json['message']['reciver_channel_name']
            text_data_json['message']['reciver_channel_name']=self.channel_name
            async_to_sync(self.channel_layer.send)(
                reciver_channel_name,
                {
                    'type':'chat_message',
                    'message':text_data_json
                }
                
            )
             
        elif action=="new-answer":
            reciver_channel_name=text_data_json['message']['reciver_channel_name']
            text_data_json['message']['reciver_channel_name']=self.channel_name
            async_to_sync(self.channel_layer.send)(
                reciver_channel_name,
                {
                    'type':'chat_message',
                    'message':text_data_json
                }
                
            )
            
        

    
    # Receive message from room group
    def chat_message(self, event):
        
        message = event['message']
        
        self.send(text_data=json.dumps(message))