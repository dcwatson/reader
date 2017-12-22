from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from reader.utils import create_feed


class Command (BaseCommand):
    def handle(self, *args, **options):
        for url in args:
            feed = create_feed(url)
            print('Added %s' % feed.url)
