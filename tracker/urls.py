from django.conf.urls import patterns, url, include

from tracker import views

urlpatterns = patterns('',
    url(r'^track/(?P<tracking_key>[a-z]+)/session/(?P<session_id>\d+)/$',
        views.track),
    url(r'^track/(?P<tracking_key>[a-z]+)/session/new/$',
        views.session_new, name='create_session'),

    url(r'^$', views.index, name='index'),

    url(r'^session/(?P<session_id>\d+)/data/$', views.session_data, name='session_data'),
    url(r'^session/viewkey/(?P<view_key>[a-z]+)/$', views.viewkey_session_list, name='vk_session_list'),
    url(r'^session/(?P<session_id>\d+)/viewkey/(?P<view_key>[a-z]+)/$',
        views.session, name='vk_session'),
    url(r'^session/$', views.user_session_list, name='user_session_list'),
    url(r'^session/(?P<session_id>\d+)/$', views.session, name='user_session'),

    url(r'^user/trackingkey/$', views.tracking_keys, name='user_tracking_key'),
    url(r'^user/trackingkey/new/$', views.tracking_keys, {'action': 'new'}, name='user_tracking_key_new'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.signup, name='signup'),
)
