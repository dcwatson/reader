from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'reader.views.index', name='index'),
    url(r'^feeds/$', 'reader.views.feeds', name='feeds'),
    url(r'^feed/(?P<feed_id>\d+)/$', 'reader.views.feed', name='feed'),
    url(r'^feed/(?P<feed_id>\d+)/(?P<story_id>\d+)/$', 'reader.views.story', name='story'),
    url(r'^admin/', include(admin.site.urls)),
)
