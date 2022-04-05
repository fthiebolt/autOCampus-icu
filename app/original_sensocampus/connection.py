#!/usr/bin/env python3
import os

# [oct.17] no more useful since we launch this app in the django runscript
# context.
#import django
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sensOCampus.settings")
#django.setup()

from devices.tasks.broker import broker_connect
broker_connect()
