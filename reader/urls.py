from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reader.views.home', name='home'),
    # url(r'^reader/', include('reader.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
