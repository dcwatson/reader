from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models, IntegrityError
import hashlib
import random

class UserManager (BaseUserManager):

    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=email.strip().lower(), last_login=timezone.now(), **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields.pop('is_admin', True)
        return self.create_user(email, is_admin=True, last_login=timezone.now(), **extra_fields)

class User (AbstractBaseUser):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
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
            except IntegrityError:
                max_tries -= 1

    def send_email(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
