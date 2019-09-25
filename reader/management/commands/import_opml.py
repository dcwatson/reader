from django.core.management.base import BaseCommand
import drill

from reader.utils import create_feed


class Command (BaseCommand):
    def handle(self, *args, **options):
        for filename in args:
            root = drill.parse(filename)
            for e in root.find('//outline'):
                feed = create_feed(e['xmlUrl'].strip())
                print('Imported %s' % feed.url)
