from django.conf import settings
from django.utils import timezone

from devices.models.device import Device

from celery import task
from paho.mqtt.publish import single
import json
import datetime

# TODO: validate status messages

@task
def handle_device_message(dev_id=None, loc=None, topic=None, payload=None):
    print('handle_device_message: ' + dev_id + ', ' + loc + ', ' + topic + ', ' + payload)

    try:
        payload = json.loads(payload)
    except Exception as ex:
        print('handle_device_message: payload is no valid json')
        return

    if 'unitID' not in payload or 'status' not in payload:
        print('handle_device_message: invalid status report')
        return

    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("handle_device_message: invalid device id " + dev_id)
    else:
        if dev.mac.lower() == payload['unitID'].lower():
            dev.last_status = payload['status']
            dev.last_update = timezone.now()
            dev.save()


@task
def reset_device(dev_id):
    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("reload_device: invalid device id " + dev_id)
    else:
        msg = dict()
        msg['dest'] = dev.mac
        msg['order'] = "reset"

        send_message_device.delay(dev_id, msg)


@task
def restart_device(dev_id):
    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("reload_device: invalid device id " + dev_id)
    else:
        msg = dict()
        msg['dest'] = dev.mac
        msg['order'] = "restart"

        send_message_device.delay(dev_id, msg)


@task
def reboot_device(dev_id):
    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("reload_device: invalid device id " + dev_id)
    else:
        msg = dict()
        msg['dest'] = dev.mac
        msg['order'] = "reboot"

        send_message_device.delay(dev_id, msg)


@task
def update_device(dev_id):
    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("reload_device: invalid device id " + dev_id)
    else:
        msg = dict()
        msg['dest'] = dev.mac
        msg['order'] = "update"

        send_message_device.delay(dev_id, msg)


@task
def status_device(dev_id):
    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("reload_device: invalid device id " + dev_id)
    else:
        msg = dict()
        msg['dest'] = dev.mac
        msg['order'] = "status"

        send_message_device.delay(dev_id, msg)


@task
def send_message_device(dev_id, msg):
    try:
        dev = Device.objects.get(id=dev_id)
    except Exception as ex:
        print("send_message_device: invalid device id " + dev_id)
    else:
        topic = dev.locations.all()[0].topic + '/device/command'
        print("publishing to " + topic)

        #[sep.17] TODO: replace 'single' with real publish message
        single(topic=topic, payload=json.dumps(msg), qos=0, retain=False, hostname=settings.MQTT_HOST,
               port=settings.MQTT_PORT, client_id="", keepalive=60, will=None,
               auth={'username': settings.MQTT_LOGIN, 'password': settings.MQTT_PASSWORD})

