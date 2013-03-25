from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'reader.views.index', name='index'),

    url(r'^login/$', 'reader.views.login', name='login'),
    url(r'^login/(?P<user_id>\d+)/(?P<token>\w+)/$', 'reader.views.email_login', name='email-login'),
    url(r'^logout/$', 'reader.views.logout', name='logout'),

    url(r'^feeds/$', 'reader.views.feeds', name='feeds'),
    url(r'^feed/(?P<feed_id>\d+)/$', 'reader.views.feed', name='feed'),
    url(r'^story/(?P<ident>\w+)/$', 'reader.views.story', name='story'),

    url(r'^stories/unread/$', 'reader.views.unread', name='unread'),
    url(r'^stories/starred/$', 'reader.views.starred', name='starred'),

    url(r'^admin/', include(admin.site.urls)),
)
