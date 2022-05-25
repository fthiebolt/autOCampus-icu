from time import sleep

publishers = {}

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class Consumer(WebsocketConsumer):
    def connect(self):
        self.group = 'users'

        async_to_sync(self.channel_layer.group_add)(
            self.group,
            self.channel_name
        )
        publishers[self] = self
        self.accept()
   

    def receive(self, text_data):
        message = text_data
        print(message)

    def location(self, event):
        message = event['text']

        self.send(message)
    
    def disconnect(self, close_code):
        print("close")
        del publishers[self]
        async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)

