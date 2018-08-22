from django.urls import path, include
from SMAApp import views
from django.conf.urls import url

# handler404 = 'SMAApp.views.view_404'
urlpatterns = [
    # Pages
    url(r'^$', views.home, name='index'),
    url(r'^diagnostics/$', views.open_diagnostics, name='diagnostics'),
    url(r'^influencers/$', views.open_influencers, name='influencers'),
    url(r'^influentialposts/$', views.open_influentialposts, name='influentialposts'),
    url(r'^topics/$', views.open_topics, name='topics'),
    url(r'^sentiments/$', views.open_sentiments, name='sentiments'),
    url(r'^register/$', views.open_registration, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),

    # Snapshots
    url(r'^loadsnapshot/$', views.load_snapshot, name='loadsnapshot'),
    
    url(r'^ajax/login_user/$', views.ajax_login_user, name='ajax_login_user'),
    url(r'^ajax/logout_user/$', views.logout_user, name='logout_user'),

    # Ajax Response
    url(r'^ajax/get_geocodes/$', views.return_geocode, name='get_geocodes'),
    url(r'^ajax/get_wordcloud_image/$', views.generate_wordcloud_image, name='get_wordcloud_image'),
    url(r'^ajax/get_lda_page/$', views.generate_lda_page, name='get_lda_page'),
    url(r'^ajax/get_lda_data/$', views.start_generate_lda, name='get_lda_data'),

    # Checks the lda status everytime.
    url(r'^ajax/check_lda_status/$', views.check_lda_status, name='check_lda_status'),

    url(r'^ajax/start_background_tasks/$', views.start_background_tasks, name='start_background_tasks'),

    #url(r'^ajax/get_wordcloud/$', views.return_wordcloud, name='get_wordcloud'),
    # Save snapshot
    url(r'^ajax/save_snapshot/$', views.save_snapshot, name='save_snapshot'),

    # Used for getting lda data from snapshot
    url(r'^ajax/get_snapshot_lda/', views.get_snapshot_lda, name='get_snapshot_lda'),
    
    # Username exists checker
    url(r'^ajax/validate_registration_email/', views.validate_registration_email, name='validate_registration_email'),
]