from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import paho.mqtt.client as mqtt
from celery import task

import json
import validictory

from devices.models.device import Device
from devices.models.location import Location
from devices.tasks.device import handle_device_message

@task
def broker_on_message(userdata, topic, payload):
    print('broker_handle_message: from ' + topic + ', ' + payload)

    if topic.endswith('/device'):
        topic = topic[:-7]
    else:
        # that message should not be related to device management, sensocampus is not concerned
        return

    # that is a hack: removes simple quotes enclosing json message
    # fixes a bug introduced by celery serialization of paho payloads
    if payload.startswith("b'") and payload.endswith("'"):
        payload = payload[2:]
        payload = payload[:-1]

    try:
        payload_data = json.loads(payload)
    except Exception as ex:
        print('error while loading json: ' + str(ex))
    else:

        if 'unitID' not in payload_data:
            print('missing unitID field in device management message')
            return

        try:
            loc = Location.objects.get(topic=topic)
        except ObjectDoesNotExist:
            print('received a device management message with an unregistered location: ' + topic)
            return

        except Exception as ex:
            print('exception while getting location related to topic ' + topic + ', ' + str(ex))
            return

        else:
            try:
                for dev in Device.objects.filter(locations=loc):
                    handle_device_message.delay(str(dev.id), str(loc.id), topic, payload)

            except Exception as ex:
                print('exception thrown while getting devices related to location: ' + str(ex))
                return


def broker_on_connect(client, userdata, flags, rc):
    #TODO: [sep.17] maybe just subscribe to #/device ?
    #       client.subscribe("#" + "/device") ?
    for dev in Device.objects.all():
        for loc in dev.locations.all():
            print("subscribing to " + loc.topic + "/device")
            client.subscribe(loc.topic + "/device")


# [sep.17] useless since call has been deleted from device.py
# TODO: remove it!
@task
def broker_reload():
    from paho.mqtt.publish import single

    # force reconnecting, thus subscribing to locks, by connecting with the same client ID as the main mqtt client inst.
    single(topic="/", payload="", qos=0, retain=False, hostname=settings.MQTT_HOST,
           port=settings.MQTT_PORT, client_id=settings.MQTT_CLIENT_ID, keepalive=5, will=None,
           auth={'username': settings.MQTT_LOGIN, 'password': settings.MQTT_PASSWORD})


# _must_ be run from a separate, persistent thread (ie: python shell)
# NOT a celery task
def broker_connect():
    client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID, clean_session=False)
    client.username_pw_set(settings.MQTT_LOGIN, settings.MQTT_PASSWORD)

    client.on_connect = broker_on_connect
    client.on_message = (lambda client, userdata, message: broker_on_message.delay(userdata, message.topic, str(message.payload)))

    print("[broker] connecting to MQTT broker %s:%d ..." % (settings.MQTT_HOST,settings.MQTT_PORT) )
    client.connect(settings.MQTT_HOST, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
    print("[broker] ... and start forever loop ...")
    client.loop_forever()

