from django.contrib import admin
from reader.feeds.models import Feed, Story

class FeedAdmin (admin.ModelAdmin):
    list_display = ('url', 'title', 'subtitle', 'author', 'date_created')

class StoryAdmin (admin.ModelAdmin):
    list_display = ('title', 'feed', 'author', 'link', 'date_published')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Story, StoryAdmin)
