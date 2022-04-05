from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^registered', views.registered, name="registered"),
    url(r'^register', views.register, name="register"),
    url(r'^credentials', views.credentials, name="credentials"),
    url(r'^logger', views.logger, name="logger"),
    url(r'^config', views.config, name="config"),
    url(r'^logs', views.logs, name="logs"),
]