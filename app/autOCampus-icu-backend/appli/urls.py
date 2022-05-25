from django.urls import re_path
from appli.views import home


urlpatterns = [
    re_path(r'^', home, name='index'),
]
