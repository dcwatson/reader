from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from reader.feeds.models import Feed
from reader.feeds.utils import get_story_identifier, get_story_content, get_story_date
import feedparser

class Command (BaseCommand):
    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            print 'Loading', feed.url
            feed_info = feedparser.parse(feed.url)
            feed.title = feed_info['feed'].get('title', '').strip()
            feed.subtitle = feed_info['feed'].get('subtitle', '').strip()
            feed.save()
            for e in feed_info.entries:
                ident = get_story_identifier(feed, e)
                story, created = feed.stories.get_or_create(ident=ident)
                story.title = e.get('title', '').strip()
                story.author = e.get('author', '').strip()
                story.content = get_story_content(e)
                story.link = e.get('link', '').strip()
                story.date_published = get_story_date(e)
                story.save()
