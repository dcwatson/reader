from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.conf import settings
import hashlib
import random

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

class UserManager (BaseUserManager):

    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=email.strip().lower(), **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields.pop('is_admin', True)
        return self.create_user(email, is_admin=True, **extra_fields)

class User (AbstractBaseUser):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __unicode__(self):
        return self.name or self.email

    def get_full_name(self):
        return self.name or self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def create_token(self):
        max_tries = 10
        while max_tries:
            try:
                s = str(timezone.now()) + str(random.random())
                token = hashlib.sha1(s.encode('utf-8')).hexdigest()
                return self.login_tokens.create(token=token)
            except:
                max_tries -= 1

    def send_email(self, subject, message, from_email=None):
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email])

class NaturalKeyManager (models.Manager):

    def __init__(self, key_field):
        super(NaturalKeyManager, self).__init__()
        self.key_field = str(key_field)

    def get_by_natural_key(self, key):
        return self.get(**{self.key_field: key})

class LoginToken (models.Model):
    user = models.ForeignKey(User, related_name='login_tokens')
    token = models.CharField(max_length=40)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'token')

    def get_absolute_url(self):
        return '/login/%s/%s/' % (self.user_id, self.token)

class Feed (models.Model):
    url = models.CharField(max_length=300, unique=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=FEED_STATUS_CHOICES, default='new')
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(null=True, blank=True)

    objects = NaturalKeyManager('url')

    def __unicode__(self):
        return self.title or self.url

    def natural_key(self):
        return (self.url,)

    def get_absolute_url(self):
        return reverse('feed', kwargs={'feed_id': self.pk})

class SmartFeed (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='smart_feeds')
    title = models.CharField(max_length=100, blank=True)
    query = models.CharField(max_length=100, blank=True)
    read = models.NullBooleanField()
    starred = models.NullBooleanField()
    limit = models.IntegerField(default=50)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('smart-feed', kwargs={'feed_id': self.pk})

class Story (models.Model):
    feed = models.ForeignKey(Feed, related_name='stories')
    ident = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True)
    date_published = models.DateTimeField(default=timezone.now)

    objects = NaturalKeyManager('ident')

    class Meta:
        verbose_name_plural = _('stories')

    def __unicode__(self):
        return self.title

    def natural_key(self):
        return (self.ident,)

    def get_absolute_url(self):
        return reverse('story', kwargs={'ident': self.ident})

class Subscription (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscriptions')
    feed = models.ForeignKey(Feed, related_name='subscriptions')
    show_read = models.IntegerField(_('show read stories back'), choices=SHOW_READ_CHOICES, default=7)
    date_subscribed = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'feed')

class ReadStory (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='read_stories')
    story = models.ForeignKey(Story, related_name='read_stories')
    is_read = models.BooleanField(default=True)
    is_starred = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    date_read = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = _('read stories')
        unique_together = ('user', 'story')
