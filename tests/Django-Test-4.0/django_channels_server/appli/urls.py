from django.urls import re_path
from appli.views import user_list


urlpatterns = [
    re_path(r'^$', user_list, name='user_list'),
]
