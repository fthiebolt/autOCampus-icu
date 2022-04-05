from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth', views.get_user),
    url(r'^superuser$', views.superuser),
    url(r'^acl', views.acl_check),
]