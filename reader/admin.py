from django.contrib import admin
from reader.models import Feed, Story, User

class FeedAdmin (admin.ModelAdmin):
    list_display = ('url', 'title', 'subtitle', 'date_created')

class StoryAdmin (admin.ModelAdmin):
    list_display = ('title', 'feed', 'author', 'link', 'date_published')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(User)
