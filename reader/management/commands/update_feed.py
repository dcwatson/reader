from django.core.management.base import BaseCommand

from reader.models import Feed
from reader.utils import update_feed


class Command (BaseCommand):
    def handle(self, *args, **options):
        update_feed(Feed.objects.get(pk=args[0]))
