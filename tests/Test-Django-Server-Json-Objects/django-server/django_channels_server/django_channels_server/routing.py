from channels.routing import route
from appli.consumer import ws_connect, ws_disconnect, ws_receive

channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),
]