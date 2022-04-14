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
        publisher = Publisher(self)
        publishers[self] = publisher
        publisher.start()

    def location(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'data',
            'message':message
        }))
    
    def disconnect(self, close_code):
        print("close")
        publisher = publishers[self]
        publisher.stop()
        del publishers[self]
        async_to_sync(self.channel_layer.group_discard)(self.group, self.channel_name)

