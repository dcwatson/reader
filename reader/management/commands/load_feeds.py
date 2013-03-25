from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from reader.utils import update_feed

class Command (BaseCommand):
    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            try:
                update_feed(feed)
                print 'Updated', feed.url
            except:
                pass
