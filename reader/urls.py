from django.conf.urls import include, url
from django.contrib import admin

from . import views


admin.autodiscover()

urlpatterns = (
    url(r'^$', views.index, name='index'),

    url(r'^login/$', views.login, name='login'),
    url(r'^login/(?P<user_id>\d+)/(?P<token>\w+)/$', views.email_login, name='email-login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^feeds/$', views.feeds, name='feeds'),
    url(r'^feed/(?P<feed_id>\d+)/$', views.feed, name='feed'),
    url(r'^feed/(?P<feed_id>\d+)/settings/$', views.feed_settings, name='feed-settings'),
    url(r'^story/(?P<ident>\w+)/$', views.story, name='story'),

    url(r'^smart/(?P<feed_id>\d+)/$', views.smart_feed, name='smart-feed'),

    url(r'^stories/unread/$', views.unread, name='unread'),
    url(r'^stories/starred/$', views.starred, name='starred'),

    url(r'^search/$', views.search, name='search'),

    url(r'^admin/', include(admin.site.urls)),
)
