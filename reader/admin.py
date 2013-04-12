from django.contrib import admin
from reader.models import Feed, Story, User, Subscription, ReadStory

class FeedAdmin (admin.ModelAdmin):
    list_display = ('url', 'title', 'subtitle', 'status', 'date_created', 'date_updated')
    list_filter = ('status',)

class StoryAdmin (admin.ModelAdmin):
    list_display = ('title', 'feed', 'author', 'link', 'date_published')

class UserAdmin (admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'is_admin', 'last_login')
    list_filter = ('is_active', 'is_admin')

class SubscriptionAdmin (admin.ModelAdmin):
    list_display = ('feed', 'user', 'show_read', 'date_subscribed')
    list_filter = ('feed', 'user')

class ReadStoryAdmin (admin.ModelAdmin):
    list_display = ('story', 'user', 'is_read', 'is_starred', 'notes', 'date_read')
    list_filter = ('user', 'is_read', 'is_starred')

admin.site.register(Feed, FeedAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(ReadStory, ReadStoryAdmin)
