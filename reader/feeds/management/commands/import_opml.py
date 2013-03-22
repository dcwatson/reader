from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from reader.feeds.models import Feed
import drill

class Command (BaseCommand):
    def handle(self, *args, **options):
        for filename in args:
            root = drill.parse(filename)
            for e in root.find('//outline'):
                try:
                    feed = Feed.objects.create(url=e['xmlUrl'].strip())
                    print 'Imported', feed.url
                except:
                    pass
