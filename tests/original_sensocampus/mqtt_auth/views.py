from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .forms import GetUser, SuperUser, ACLCheck
from devices.models.device import Device
from devices.models.permission import Permission
from .topic import topic_match


@csrf_exempt
@require_POST
def get_user(req):
    form = GetUser(req.POST)
    if form.is_valid():

        try:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            dev = Device.objects.get(login=username, password=password)
        except ObjectDoesNotExist:

            return HttpResponseServerError()
        else:
            return HttpResponse()

    return HttpResponseServerError()


@csrf_exempt
@require_POST
def superuser(req):
    form = SuperUser(req.POST)

    if form.is_valid():
        try:
            username = form.cleaned_data['username']
            dev = Device.objects.get(login=username)
        except ObjectDoesNotExist:
            return HttpResponseForbidden()
        else:
            return HttpResponseForbidden()  # no superusers for now

    return HttpResponseServerError()


@csrf_exempt
@require_POST
def acl_check(req):
    form = ACLCheck(req.POST)

    if form.is_valid():
        try:
            username = form.cleaned_data['username']
            topic = form.cleaned_data['topic']
            # [oct.18] new MQTT code for SUBSCRIBE --> 4 but we also keep 1 for compatibility
            # MOSC_ACl_READ --> 1
            # MOSC_ACl_WRITE--> 2
            # MOSC_ACl_RW   --> 3
            # MOSC_ACl_SUB  --> 4
            acc = 'SUB' if( form.cleaned_data['acc'] == '1' or form.cleaned_data['acc'] == '4') else 'PUB' if form.cleaned_data['acc'] == '2' else None

            if acc is None:
                return HttpResponseServerError()

            cid = form.cleaned_data['clientid']

            dev = Device.objects.get(login=username)
            perms = Permission.objects.all().filter(device=dev)

        except ObjectDoesNotExist as ex:
            return HttpResponseServerError()
        else:
            for perm in perms:
                if perm.match_type(acc) and topic_match(perm.topic, topic):
                    return HttpResponse()

            return HttpResponseForbidden()

    return HttpResponseServerError()
