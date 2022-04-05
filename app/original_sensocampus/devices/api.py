from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden

from functools import wraps
from base64 import b64decode

from devices.models.device import Device


def device_auth(func):
    @wraps(func)
    def _decorator(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            method, auth = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
            if method.lower() == 'basic':
                auth = b64decode(auth.strip()).decode('utf-8')
                login, password = auth.split(':', 1)

                try:
                    dev = Device.objects.get(login=login, password=password)
                except ObjectDoesNotExist:
                    return HttpResponseForbidden()
                else:
                    kwargs['device'] = dev

                if not dev.enabled:
                    return HttpResponseForbidden()

        return func(request, *args, **kwargs)
    return _decorator
