from django.utils import timezone
from django.contrib.sites.models import Site
from reader.models import Feed, Story
from BeautifulSoup import BeautifulSoup
import feedparser
import requests
import urlparse
import datetime
import logging
import hashlib
import time

logger = logging.getLogger(__name__)

# Parts taken from https://gist.github.com/ksamuel/1308133
FEED_LINK_ATTRIBUTES = (
    (('type', 'application/rss+xml'),),
    (('type', 'application/atom+xml'),),
    (('type', 'application/rss'),),
    (('type', 'application/atom'),),
    (('type', 'application/rdf+xml'),),
    (('type', 'application/rdf'),),
    (('type', 'text/rss+xml'),),
    (('type', 'text/atom+xml'),),
    (('type', 'text/rss'),),
    (('type', 'text/atom'),),
    (('type', 'text/rdf+xml'),),
    (('type', 'text/rdf'),),
    (('rel', 'alternate'), ('type', 'text/xml')),
    (('rel', 'alternate'), ('type', 'application/xml')),
)

def reader_context(request):
    return {
        'site': Site.objects.get_current(),
        'request_path': request.path,
    }

def get_story_content(data):
    if 'content' in data:
        return data['content'][0]['value'].strip()
    elif 'summary' in data:
        return data['summary'].strip()
    return u''

def get_story_date(data):
    if 'published_parsed' in data:
        return datetime.datetime.fromtimestamp(time.mktime(data['published_parsed'])).replace(tzinfo=timezone.utc)
    elif 'updated_parsed' in data:
        return datetime.datetime.fromtimestamp(time.mktime(data['updated_parsed'])).replace(tzinfo=timezone.utc)
    return datetime.datetime.utcnow().replace(tzinfo=timezone.utc)

def get_story_identifier(feed, data):
    bits = [
        feed.url,
        get_story_date(data).strftime('%Y-%m-%d %H:%M:%S'),
    ]
    if 'link' in data:
        bits.append(data['link'])
    if 'id' in data:
        bits.append(data['id'])
    return hashlib.sha1('\n'.join(bits)).hexdigest()

def get_stories(feeds, user, read=None, starred=None):
    sql = """
        SELECT
            s.*,
            coalesce(rs.is_read, 0) AS "is_read",
            coalesce(rs.is_starred, 0) AS "is_starred",
            coalesce(rs.notes, '') AS "notes"
        FROM
            reader_story s
            LEFT OUTER JOIN reader_readstory rs ON rs.story_id = s.id AND rs.user_id = %(user_id)s
        WHERE
            s.feed_id IN (%(feed_ids)s)
            %(where)s
        ORDER BY s.date_published DESC
    """
    where = []
    if read is not None:
        if read:
            where.append('rs.is_read = 1')
        else:
            where.append('(rs.is_read = 0 OR rs.is_read IS NULL)')
    if starred is not None:
        if starred:
            where.append('rs.is_starred = 1')
        else:
            where.append('(rs.is_starred = 0 OR rs.is_starred IS NULL)')
    params = {
        'user_id': user.pk,
        'feed_ids': ', '.join([str(f.pk) for f in feeds]),
        'where': 'AND %s' % ' AND '.join(where) if where else '',
    }
    return Story.objects.raw(sql % params)

def ajaxify(model, fields=None, extra=None):
    if fields is None:
        fields = [f.name for f in model._meta.fields]
    if extra:
        fields = list(fields) + list(extra)
    data = {}
    for field_name in fields:
        obj = getattr(model, field_name, None)
        if hasattr(obj, 'pk'):
            data[field_name] = obj.pk
        elif isinstance(obj, datetime.datetime):
            data[field_name] = obj.isoformat()
        elif callable(obj):
            data[field_name] = obj()
        else:
            data[field_name] = obj
    if hasattr(model, 'get_absolute_url'):
        data['reader_url'] = model.get_absolute_url()
    return data

def normalize_url(url):
    scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
    return urlparse.urlunsplit((scheme.lower(), netloc.lower(), path, query, fragment)).strip()

def valid_feed(feed):
    if not feed.bozo:
        return True
    if isinstance(feed.bozo_exception, feedparser.CharacterEncodingOverride):
        return True
    return False

def fetch_feed(url):
    try:
        feed = feedparser.parse(url)
        if valid_feed(feed):
            # The provided link was a feed link, we're done.
            return feed
        # Otherwise, fetch the page and look for <link> elements.
        r = requests.get(url)
        head = BeautifulSoup(r.text).find('head')
        for attrs in FEED_LINK_ATTRIBUTES:
            for link in head.findAll('link', dict(attrs)):
                href = dict(link.attrs).get('href', '')
                if href:
                    if '://' not in href:
                        # Use the response URL to build the full feed URL, in case there were redirects.
                        href = urlparse.urljoin(r.url, href)
                    feed = feedparser.parse(href)
                    if valid_feed(feed):
                        return feed
    except:
        logger.exception('Error finding feed link for "%s"', url)
        return None

def update_feed(feed, info=None):
    if info is None:
        info = fetch_feed(feed.url)
    if info:
        feed.status = 'valid'
        if info.status in (200, 301):
            # For successful fetches or permanent redirects, record the "resolved" URL (after redirects).
            new_url = normalize_url(info.href)
            if not Feed.objects.filter(url=new_url).exists():
                feed.url = new_url
        elif info.status in (410,):
            feed.status = 'gone'
        feed.title = info['feed'].get('title', '').strip()
        feed.subtitle = info['feed'].get('subtitle', '').strip()
        for e in info.entries:
            ident = get_story_identifier(feed, e)
            story, created = Story.objects.get_or_create(feed=feed, ident=ident)
            story.title = e.get('title', '').strip()
            story.author = e.get('author', '').strip()
            story.content = get_story_content(e)
            story.link = e.get('link', '').strip()
            story.date_published = get_story_date(e)
            story.save()
    else:
        feed.status = 'error'
    feed.date_updated = timezone.now()
    feed.save()

def create_feed(url):
    url = normalize_url(url)
    try:
        # If the Feed already exists, return it (without updating).
        return Feed.objects.get(url=url)
    except Feed.DoesNotExist:
        # Otherwise, try to download it to get the "resolved" URL.
        info = fetch_feed(url)
        if info:
            url = normalize_url(info.href)
            feed, created = Feed.objects.get_or_create(url=url)
            # Since we alredy downloaded the feed data, we may as well update it.
            update_feed(feed, info=info)
            return feed
        else:
            return Feed.objects.create(url=url, status='error')
