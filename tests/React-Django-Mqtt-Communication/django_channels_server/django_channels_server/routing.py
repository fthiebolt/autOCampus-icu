from django.urls import path
from appli.consumer import Consumer

channel_routing = [
    path('',Consumer.as_asgi())
]