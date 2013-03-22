from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

class UserManager (BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(name=name.strip(), email=UserManager.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        _admin = extra_fields.pop('is_admin', True)
        return self.create_user(email, name, password=password, is_admin=True, **extra_fields)

class User (AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    objects = UserManager()

    def __unicode__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class NaturalKeyManager (models.Manager):

    def __init__(self, key_field):
        super(NaturalKeyManager, self).__init__()
        self.key_field = str(key_field)

    def get_by_natural_key(self, key):
        return self.get(**{self.key_field: key})

class Feed (models.Model):
    url = models.CharField(max_length=300, unique=True)
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    objects = NaturalKeyManager('url')

    def __unicode__(self):
        return self.title or self.url

    def natural_key(self):
        return (self.url,)

class Story (models.Model):
    feed = models.ForeignKey(Feed, related_name='stories')
    ident = models.CharField(max_length=40, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True)
    date_published = models.DateTimeField(default=timezone.now)

    objects = NaturalKeyManager('ident')

    def __unicode__(self):
        return self.title

    def natural_key(self):
        return (self.ident,)

class Subscription (models.Model):
    user = models.ForeignKey(User, related_name='subscriptions')
    feed = models.ForeignKey(Feed, related_name='subscriptions')
    date_subscribed = models.DateTimeField(default=timezone.now)

class ReadStory (models.Model):
    user = models.ForeignKey(User, related_name='read_stories')
    story = models.ForeignKey(Story, related_name='read_stories')
    is_read = models.BooleanField(default=True)
    is_starred = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    date_read = models.DateTimeField(default=timezone.now)
