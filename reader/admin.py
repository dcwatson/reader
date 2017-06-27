from django.contrib import admin

from reader.models import Feed, ReadStory, SmartFeed, Story, Subscription


class FeedAdmin (admin.ModelAdmin):
    list_display = ('url', 'title', 'subtitle', 'status', 'date_created', 'date_updated')
    list_filter = ('status',)


class StoryAdmin (admin.ModelAdmin):
    list_display = ('title', 'feed', 'author', 'link', 'date_published')


class SubscriptionAdmin (admin.ModelAdmin):
    list_display = ('feed', 'user', 'show_read', 'date_subscribed')
    list_filter = ('feed', 'user')


class ReadStoryAdmin (admin.ModelAdmin):
    list_display = ('story', 'user', 'is_read', 'is_starred', 'notes', 'date_read')
    list_filter = ('user', 'is_read', 'is_starred')


class SmartFeedAdmin (admin.ModelAdmin):
    list_display = ('title', 'user', 'query', 'read', 'starred', 'limit')
    list_filter = ('user',)


admin.site.register(Feed, FeedAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ReadStory, ReadStoryAdmin)
admin.site.register(SmartFeed, SmartFeedAdmin)
