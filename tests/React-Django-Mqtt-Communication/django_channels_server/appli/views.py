from email import message
from time import sleep
from django.shortcuts import render
from numpy import array, size
import threading
import json
from asgiref.sync import async_to_sync

def user_list(request):
    return render(request, "carte/index.html")
iteration = array([[1.4656, 43.5617],
            [1.4657, 43.5616],
            [1.4658, 43.5614],
            [1.466, 43.5613],
            [1.4661, 43.5612],
            [1.4661, 43.5611],
            [1.4662, 43.561],
            [1.4663, 43.5609],
            [1.4664, 43.5609],
            [1.4667 , 43.5606],
            [1.4668 , 43.5605],
            [1.4669 , 43.5604],
            [1.467 , 43.5603],
            [1.4671 , 43.5601]])
size = size(iteration, 0) - 1
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class Publisher(threading.Thread):
    def __init__(self, frequency=0.5):
        super(Publisher, self).__init__()
        self._running = True
        self._publish_interval = 1.0 / frequency
    
    def run(self):
        i = 0
        while (i < size and self._running):
           mail = json.dumps({"id": "R1","Lag":iteration[i][0],"Lat":iteration[i][1]})
           print("server >>")
           async_to_sync(channel_layer.group_send)('users', {
               'type':'location',
               'text':mail})
           i+=1
           sleep(self._publish_interval)
    
    def stop(self):
        self._running = False

