from channels import Group
from appli.views import send_coord

def ws_connect(message):
    Group('users').add(message.reply_channel)
    message.reply_channel.send({"accept": True})

def ws_receive(message):
    text = message.content.get('text')
    print(text)
    send_coord()

def ws_disconnect(message):
    Group('users').discard(message.reply_channel)