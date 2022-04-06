from django.forms import ModelForm, TextInput, SelectMultiple, Select, CharField, Form, ModelChoiceField
from django.utils import timezone
import datetime

from devices.models.device import Device
from devices.models.log_message import LogMessage
from devices.utils import validate_mac


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ['mac', 'type', 'description', 'locations']

        widgets = {
            'mac': TextInput(attrs={'class': "form-control"}),
            'type': Select(attrs={'class': "form-control"}),
            'description': TextInput(attrs={'class': "form-control"}),
            'locations': SelectMultiple(attrs={'class': "form-control"}),
        }


class DeviceIDForm(Form):
    mac = CharField(max_length=17, validators=[validate_mac])


class LogMessageForm(ModelForm):
    class Meta:
        model = LogMessage
        exclude = ('device', 'date', 'remote_ip', 'remote_host',)

    def __init__(self, request, device):
        self.request = request
        self.device = device
        super(LogMessageForm, self).__init__(request.POST)

    def save(self, commit=True):
        instance = super(LogMessageForm, self).save(commit=False)
        instance.device = self.device
        instance.date = timezone.now()
        instance.remote_ip = self.request.META['REMOTE_ADDR']
        if 'REMOTE_HOST' in self.request.META:
            instance.remote_host = self.request.META['REMOTE_HOST']

        # replace the string 'None' with None in the follow fields:
        for field in ('exc_info', 'exc_text', 'args'):
            if getattr(instance, field) == 'None':
                setattr(instance, field, None)

        if commit:
            instance.save()

        return instance


class LoggerForm(Form):

    device = ModelChoiceField(queryset=Device.objects.all(), widget=Select(attrs={'class': "form-control"}))
    format = CharField(required=False, help_text="Leave blank for system default. Python string format, fields specified <a target=\"_blank\" href=\"https://docs.python.org/3/library/logging.html#logrecord-attributes\">here</a>",
                       widget=TextInput(attrs={'class': "form-control"}))
