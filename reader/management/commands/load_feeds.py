from django.conf import settings
from django.core.management.base import BaseCommand

from reader.models import Feed
from reader.utils import update_feed

import multiprocessing


def update(feed_id):
    """
    Worker function to fetch and update the feeds in a separate process.
    """
    try:
        import django
        django.setup()
        update_feed(Feed.objects.get(pk=feed_id))
    except Exception:
        # multiprocessing doesn't seem to like exceptions in workers
        pass


class Command (BaseCommand):
    def handle(self, *args, **options):
        pool = multiprocessing.Pool(processes=settings.READER_UPDATE_PROCESSES)
        for feed_id in Feed.objects.values_list('pk', flat=True):
            pool.apply_async(update, (feed_id,))
        pool.close()
        pool.join()
