from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from reader.api import FeedResource, SubscriptionResource

admin.autodiscover()

api_v1 = Api(api_name='v1')
api_v1.register(FeedResource())
api_v1.register(SubscriptionResource())

urlpatterns = patterns('',
    url(r'^$', 'reader.views.index', name='index'),

    url(r'^login/$', 'reader.views.login', name='login'),
    url(r'^login/(?P<user_id>\d+)/(?P<token>\w+)/$', 'reader.views.email_login', name='email-login'),
    url(r'^logout/$', 'reader.views.logout', name='logout'),

    url(r'^feeds/$', 'reader.views.feeds', name='feeds'),
    url(r'^feed/(?P<feed_id>\d+)/$', 'reader.views.feed', name='feed'),
    url(r'^feed/(?P<feed_id>\d+)/settings/$', 'reader.views.feed_settings', name='feed-settings'),
    url(r'^story/(?P<ident>\w+)/$', 'reader.views.story', name='story'),

    url(r'^smart/(?P<feed_id>\d+)/$', 'reader.views.smart_feed', name='smart-feed'),

    url(r'^stories/unread/$', 'reader.views.unread', name='unread'),
    url(r'^stories/starred/$', 'reader.views.starred', name='starred'),

    url(r'^search/$', 'reader.views.search', name='search'),

    url(r'^api/', include(api_v1.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
