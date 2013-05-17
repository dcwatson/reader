from django.core.management.base import BaseCommand, CommandError
from reader.models import Feed
from reader.utils import update_feed

class Command (BaseCommand):
    def handle(self, *args, **options):
        update_feed(Feed.objects.get(pk=args[0]))
