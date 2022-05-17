from django.urls import re_path
from appli.views import home, map


urlpatterns = [
    re_path(r'^', home, name='index'),
    re_path(r'^map/', map, name='map'),
]
