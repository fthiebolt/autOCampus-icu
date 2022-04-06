from django.shortcuts import render

from devices.models.device import Device

def homepage(req):
    return render(req, 'homepage.html', {"device_count": Device.objects.count()})
