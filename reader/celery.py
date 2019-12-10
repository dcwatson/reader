from celery import Celery, group

import datetime
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reader.settings")

app = Celery('reader', broker='redis://localhost:6379/0')

app.conf.beat_schedule = {
    'load_feeds': {
        'task': 'reader.load_feeds',
        'schedule': datetime.timedelta(minutes=30),
    },
}


@app.task(name='reader.load_feeds')
def load_feeds():
    from reader.models import Feed
    group(load_feed.s(feed_id) for feed_id in Feed.objects.values_list('pk', flat=True))()


@app.task(name='reader.load_feed')
def load_feed(feed_id):
    from reader.models import Feed
    from reader.utils import update_feed
    update_feed(Feed.objects.get(pk=feed_id))
