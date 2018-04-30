from django.urls import path, include
from SMAApp import views
from django.conf.urls import url


urlpatterns = [
    # Pages
    url(r'^$', views.home, name='index'),
    url(r'^diagnostics/$', views.open_diagnostics, name='diagnostics'),
    url(r'^influencers/$', views.open_influencers, name='influencers'),
    url(r'^influentialposts/$', views.open_influentialposts, name='influentialposts'),
    url(r'^topics/$', views.open_topics, name='topics'),
    url(r'^sentiments/$', views.open_sentiments, name='sentiments'),

    # Ajax Response
    url(r'^ajax/get_geocodes/$', views.return_geocode, name='get_geocodes'),
    #url(r'^ajax/get_wordcloud/$', views.return_wordcloud, name='get_wordcloud'),
]