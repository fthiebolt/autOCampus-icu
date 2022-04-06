from django import forms


class GetUser(forms.Form):
    username = forms.CharField(max_length=512)
    password = forms.CharField(max_length=512)


class SuperUser(forms.Form):
    username = forms.CharField(max_length=512)


class ACLCheck(forms.Form):
    username = forms.CharField(max_length=512)
    topic = forms.CharField(max_length=512)
    clientid = forms.CharField(max_length=512)
    acc = forms.CharField(max_length=512)
