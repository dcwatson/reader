from django.conf import settings
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import re


try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

FEED_STATUS_CHOICES = (
    ('new', 'New'),
    ('valid', 'Valid'),
    ('error', 'Error'),
    ('gone', 'Gone'),
)

SHOW_READ_CHOICES = (
    (0, 'Do not show read stories'),
    (1, '1 day'),
    (2, '2 days'),
    (3, '3 days'),
    (4, '4 days'),
    (5, '5 days'),
    (6, '6 days'),
    (7, '7 days (1 week)'),
    (14, '14 days (2 weeks)'),
    (28, '28 days (4 weeks)'),
    (-10, '10 stories'),
    (-25, '25 stories'),
    (-50, '50 stories'),
)

TAG_PATTERN = re.compile(r'<([a-z0-9]+)([^>]*)>', re.I)
SRC_PATTERN = re.compile(r'(src|srcset|href)=["\']([^"\']+)["\']', re.I)


class NaturalKeyManager (models.Manager):

    def __init__(self, key_field='pk'):
        super(NaturalKeyManager, self).__init__()
        self.key_field = str(key_field)

    def get_by_natural_key(self, key):
        return self.get(**{self.key_field: key})


class LoginToken (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='login_tokens', on_delete=models.CASCADE)
    token = models.CharField(max_length=40)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'token')

    def get_absolute_url(self):
        return '/login/%s/%s/' % (self.user_id, self.token)


class Feed (models.Model):
    url = models.CharField(max_length=300, unique=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=FEED_STATUS_CHOICES, default='new')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(null=True, blank=True)

    story_count = models.IntegerField(default=0)

    objects = NaturalKeyManager('url')

    def __str__(self):
        return self.title or self.url

    def natural_key(self):
        return (self.url,)

    def get_absolute_url(self):
        return reverse('feed', kwargs={'feed_id': self.pk})

    def update_story_count(self):
        qs = Feed.objects.filter(pk=self.pk).select_for_update()
        self.story_count = self.stories.count()
        qs.update(story_count=self.story_count)


class SmartFeed (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='smart_feeds', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    query = models.CharField(max_length=100, blank=True)
    read = models.NullBooleanField()
    starred = models.NullBooleanField()
    limit = models.IntegerField(default=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('smart-feed', kwargs={'feed_id': self.pk})


class Story (models.Model):
    feed = models.ForeignKey(Feed, related_name='stories', on_delete=models.CASCADE)
    ident = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True)
    date_published = models.DateTimeField(default=timezone.now, db_index=True)

    search = SearchVectorField(null=True)

    objects = NaturalKeyManager('ident')

    class Meta:
        verbose_name_plural = _('stories')

    def __str__(self):
        return self.title

    def natural_key(self):
        return (self.ident,)

    def get_absolute_url(self):
        return reverse('story', kwargs={'ident': self.ident})

    def fixed_content(self):
        def src_fixer(match):
            name, value = match.groups()
            if name.lower() == 'srcset':
                parts = []
                for v in value.split(','):
                    # For each URL (and optional density) in the srcset, fix the URL part (and keep the density part).
                    ss = v.strip().rsplit(None, 1)
                    ss[0] = urlparse.urljoin(self.feed.url, ss[0])
                    parts.append(' '.join(ss))
                value = ', '.join(parts)
            elif value.startswith('#'):
                # Ideally anchors would work inline, but this is better than before.
                value = urlparse.urljoin(self.link, value)
            elif '://' not in value:
                value = urlparse.urljoin(self.feed.url, value)
            return '%s="%s"' % (name, value)

        def tag_fixer(match):
            tag, attrs = match.groups()
            attrs = SRC_PATTERN.sub(src_fixer, attrs)
            return '<%s%s>' % (tag, attrs)
        return mark_safe(TAG_PATTERN.sub(tag_fixer, self.content))


class Subscription (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions', on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, related_name='subscriptions', on_delete=models.CASCADE)
    show_read = models.IntegerField(_('show read stories back'), choices=SHOW_READ_CHOICES, default=7)
    date_subscribed = models.DateTimeField(default=timezone.now)

    read_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'feed')

    def update_read_count(self):
        qs = Subscription.objects.filter(pk=self.pk).select_for_update()
        self.read_count = ReadStory.objects.filter(user=self.user, feed=self.feed, is_read=True).count()
        qs.update(read_count=self.read_count)


class ReadStory (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='read_stories', on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, related_name='read_stories', on_delete=models.CASCADE)
    story = models.ForeignKey(Story, related_name='read_stories', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=True)
    is_starred = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    date_read = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = _('read stories')
        unique_together = ('user', 'story')
