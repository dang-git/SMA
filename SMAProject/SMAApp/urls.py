from django.urls import path, include
from SMAApp import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.home, name='index'),
]