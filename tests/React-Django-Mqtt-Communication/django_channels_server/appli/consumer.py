from time import sleep
from appli.views import Publisher
from .views import iteration, size

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
        self.accept()
   

    def receive(self, text_data):
        message = text_data
        print(message)

    def location(self, event):
        message = event['text']

        self.send(message)
    
    def disconnect(self, close_code):
        print("close")
        async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)

