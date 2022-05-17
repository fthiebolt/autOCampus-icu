from django.apps import AppConfig
from threading import Thread
import paho.mqtt.client as mqtt
import json
from appli.views import iteration, size, Publisher
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from appli.consumer import publishers
from threading import Thread
import queue
import os

channel_layer = get_channel_layer()
taskQueue = queue.Queue()

def worker() : 
    while True:
        message = taskQueue.get()
        message_send = {}
        message_send['Type'] = "VARB" #Moving Object
        message_send['id'] = message['unitID']
        for i in range(0, len(message['Value'])):
            message_send[message['Value-Units'][i]] = message['Value'][i]

        print(str(message_send) + "Total: {}".format(MqttClient.total_messages))
        # client.publish("TestTopic/myTest", json.dumps(message_send))
        if len(publishers)!=0 :
            async_to_sync(channel_layer.group_send)('users', {
               'type':'location',
               'text':json.dumps(message_send)})
        taskQueue.task_done()

class MqttClient(Thread):
    total_messages = 0
    def __init__(self, broker, port, timeout, topics):
        super(MqttClient, self).__init__()
        self.client = mqtt.Client(os.environ["MQTT_USER"])
        self.broker = broker
        self.port = port
        self.timeout = timeout
        self.topics = topics

    #  run method override from Thread class
    def run(self):
        self.connect_to_broker()

    def connect_to_broker(self): #if you want to process data using a queue
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(os.environ["MQTT_USER"], os.environ["MQTT_PASSWD"])
        self.client.connect(self.broker, self.port, self.timeout)
        self.client.loop_forever()

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        MqttClient.total_messages = MqttClient.total_messages + 1
        message = json.loads(str(msg.payload.decode("utf-8")))
        #taskQueue.put(message)
        message_send = {}
        message_send['Type'] = "VARB" #Moving Object
        message_send['id'] = message['unitID']
        for i in range(0, len(message['Value'])):
            message_send[message['Value-Units'][i]] = message['Value'][i]

        print(str(message_send) + "Total: {}".format(MqttClient.total_messages))
        if len(publishers)!=0 :
            async_to_sync(channel_layer.group_send)('users', {
               'type':'location',
               'text':json.dumps(message_send)})
        


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        #  Subscribe to a list of topics using a lock to guarantee that a topic is only subscribed once
        for topic in self.topics:
            client.subscribe(topic)


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appliMqtt'

    def ready(self):
        #Thread(target=worker, daemon=True).start()
        topics_data=json.loads(os.environ["MQTT_TOPICS"])
        topics = []
        for key, value in topics_data.items():
            topics.append(value)
        MqttClient(os.environ["MQTT_SERVER"],int(os.environ["MQTT_PORT"]), int(os.environ["MQTT_TIMEOUT"]
), topics).start()
        print("ready")
