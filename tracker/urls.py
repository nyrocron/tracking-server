from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    url(r'^track/(?P<tracking_key>[a-z]+)/session/(?P<session_id>\d+)/$',
        views.track),
    url(r'^track/(?P<tracking_key>[a-z]+)/session/new/$',
        views.session_new, name='create_session'),
    url(r'^track/(?P<tracking_key>[a-z]+)/session/(?P<session_id>\d+)/finish/$',
        views.session_finish, name='finish_session'),

    url(r'^$', views.index, name='index'),

    url(r'^session/(?P<session_id>\d+)/data/viewkey/(?P<view_key>[a-z]+)/$',
        views.session_data, name='vk_session_data'),
    url(r'^session/(?P<session_id>\d+)/data/viewkey/(?P<view_key>[a-z]+)/since/(?P<since>\d+)/$',
        views.session_data),
    url(r'^session/(?P<session_id>\d+)/data/$',
        views.session_data, name='session_data'),
    url(r'^session/(?P<session_id>\d+)/data/since/(?P<since>\d+)/$',
        views.session_data),

    url(r'^session/(?P<session_id>\d+)/viewkey/(?P<view_key>[a-z]+)/$',
        views.session, name='vk_session'),
    url(r'^session/$', views.user_session_list, name='user_session_list'),
    url(r'^session/(?P<session_id>\d+)/$', views.session, name='user_session'),
    url(r'^session/(?P<session_id>\d+)/gpx/$',
        views.session_gpx, name='session_gpx'),
    url(r'^session/(?P<session_id>\d+)/clean/$',
        views.session_clean, name='session_clean'),
    url(r'^session/(?P<session_id>\d+)/delete/$',
        views.session_delete, name='session_delete'),

    url(r'^trackingkey/$', views.tracking_key, name='user_tracking_key'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^register/$', views.signup, name='signup'),
)
