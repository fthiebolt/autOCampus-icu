#
# neOCampus operation
#
# Thiebolt.F    [oct.17]    added MQTT server and port to credentials
# T.Bueno       [may.16]    initial release
#
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

import json
from io import StringIO
from wsgiref.util import FileWrapper

from devices.models.device import Device
from devices.models.log_message import LogMessage
from devices.forms import DeviceForm, DeviceIDForm, LogMessageForm, LoggerForm
from devices.utils import format_mac
from devices.api import device_auth


@require_http_methods(["GET", "POST"])
@login_required
def register(req):
    if req.user.has_perm("device.add"):

        if req.method == 'POST':
            form = DeviceForm(req.POST)
        else:
            if req.method == 'GET' and 'mac' in req.GET:
                form = DeviceForm(req.GET)
            else:
                form = DeviceForm()

        if form.is_valid():
            try:
                dev = form.save()
            except:
                return HttpResponseServerError("Can't create device")
            else:
                return redirect('devices:registered')

        return render(req, 'devices/register.html', {'form': form})

    else:
        return HttpResponseForbidden("You can't register a new device")


@require_http_methods(["GET", "POST"])
@login_required
def logs(req):
    if req.user.has_perm("logmessage.change"):

        if req.method == 'POST':
            form = LoggerForm(req.POST)
        else:
            if req.method == 'GET' and 'device' in req.GET:
                form = LoggerForm(req.GET)
            else:
                form = LoggerForm()

        if form.is_valid():
            try:
                dev = form.cleaned_data['device']

                render_log = StringIO()

                for log in LogMessage.objects.filter(device=dev).order_by('date'):
                    dict = log.formattable_dict()
                    render_log.write(settings.LOGS_FORMAT % dict)
                    render_log.write("\n")

                render_log.flush()
                render_log.seek(0)
            except Exception as ex:
                print("exception while generating logs: " + str(ex))
                return HttpResponseServerError("Can't create logs")

            else:
                response = HttpResponse(FileWrapper(render_log), content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename=log-' + dev.mac + '.txt'
                return response

        return render(req, 'devices/logs.html', {'form': form})

    else:
        return HttpResponseForbidden("You can't get logs")


def registered(req):
    return render(req, 'devices/registered.html')


def credentials(req):
    if req.method == 'POST':
        form = DeviceIDForm(req.POST)
    else:
        if req.method == 'GET':
            form = DeviceIDForm(req.GET)
        else:
            form = DeviceIDForm()

    if form.is_valid():
        try:
            mac_addr = format_mac(form.cleaned_data['mac'])
            dev = Device.objects.get(mac=mac_addr)

        except ObjectDoesNotExist:
            return HttpResponseForbidden()

        else:
            conf = dict()
            conf['login'] = dev.login

            # already delivered password ?
            if not dev.credentials_delivered:
                dev.credentials_delivered = True
                dev.save()
                conf['password'] = dev.password

            # defauly MQTT broker and port ?
            if not dev.mqtt_defaults:
                # server, check it is not None nor ""
                # check port is integer
                if dev.mqtt_server and isinstance(dev.mqtt_port, int):
                    conf['server']  = dev.mqtt_server
                    conf['port']    = dev.mqtt_port

            conf_json = json.dumps(conf)

            return HttpResponse(conf_json, content_type='application/json')

    return HttpResponseForbidden()


@csrf_exempt
@require_POST
@device_auth
def logger(req, device=None):
    if not device or (device and not device.enabled):
        return HttpResponseForbidden()

    form = LogMessageForm(req, device)

    if form.is_valid():
        form.save()
        return HttpResponse()
    else:
        return HttpResponseForbidden()


@csrf_exempt
@device_auth
def config(req, device=None):
    if not device or (device and not device.enabled):
        return HttpResponseForbidden()

    topics = list()
    topics.extend(device.locations.all())
    topics = list(map(lambda t: t.topic, topics))

    conf = dict()
    conf['topics'] = topics
    conf['zones'] = json.loads(device.modules)

    conf_json = json.dumps(conf)

    return HttpResponse(conf_json, content_type='application/json')
