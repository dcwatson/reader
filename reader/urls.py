from django.contrib import admin
from django.urls import include, path

from . import views


admin.autodiscover()

urlpatterns = (
    path('', views.index, name='index'),

    path('login/', views.login, name='login'),
    path('login/<int:user_id>/<token>/', views.email_login, name='email-login'),
    path('logout/', views.logout, name='logout'),

    path('feeds/', views.feeds, name='feeds'),
    path('feed/<int:feed_id>/', views.feed, name='feed'),
    path('feed/<int:feed_id>/settings/', views.feed_settings, name='feed-settings'),
    path('story/<ident>/', views.story, name='story'),

    path('smart/<int:feed_id>/', views.smart_feed, name='smart-feed'),

    path('stories/unread/', views.unread, name='unread'),
    path('stories/starred/', views.starred, name='starred'),

    path('search/', views.search, name='search'),

    path('admin/', admin.site.urls),
)
