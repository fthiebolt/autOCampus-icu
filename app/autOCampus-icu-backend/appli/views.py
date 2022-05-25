from email import message
from django.contrib import messages
from time import sleep
from django.shortcuts import render
from numpy import array, size
from django.http import HttpResponseRedirect
import threading
import json
from asgiref.sync import async_to_sync
import os

def home(request):
    if request.method == 'POST':
        print("Requested authentification by " + request.POST['username'])
        if (request.POST['username'] != os.environ['APPLICATION_USERNAME'] or request.POST['password'] != os.environ['APPLICATION_PASSWORD']) :
            messages.success(request, 'Wrong Username or Password!')
            return render(request, 'authentification.html')
        else :
            request.session['member_id'] = request.POST['username']
            return HttpResponseRedirect(os.environ['APPLICATION_SERVER']+"/carte")
    else:
        if request.session.get('member_id', False) :
            return HttpResponseRedirect(os.environ['APPLICATION_SERVER']+"/carte")
        else :
            return render(request, 'authentification.html')
def front(request):
    context = { }
    if request.session.get('member_id', False) :
        return render(request, "index.html", context)
    else :
        return HttpResponseRedirect(os.environ['APPLICATION_SERVER'])
