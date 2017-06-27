from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import smart_text

from .forms import SettingsForm
from .models import Feed, LoginToken, ReadStory, SmartFeed, Story
from .utils import ajaxify, create_feed, get_stories, mark_all_read

import datetime
import itertools
import json
import operator


@login_required
def index(request):
    template_name = 'index_2panel.html' if '2panel' in request.GET else 'index.html'
    return render(request, 'reader/%s' % template_name, {
        'is_2panel': '2panel' in request.GET,
    })


def login(request):
    User = auth.get_user_model()
    sent = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        user, created = User.objects.get_or_create(email=email)
        if User.objects.count() == 1:
            user.is_admin = True
            user.save()
        token = user.create_token()
        message = render_to_string('reader/email/login.txt', {
            'user': user,
            'created': created,
            'token': token,
            'site': Site.objects.get_current(),
            'expire_hours': settings.READER_TOKEN_EXPIRE,
            'login_url': request.build_absolute_uri(token.get_absolute_url()),
        })
        user.send_email('Reader Login', message)
        sent = user.email
    return render(request, 'reader/login.html', {
        'sent': sent,
    })


def email_login(request, user_id, token):
    # Wipe out any login tokens older than 2 hours.
    expire_date = timezone.now() - datetime.timedelta(hours=settings.READER_TOKEN_EXPIRE)
    LoginToken.objects.filter(date_created__lt=expire_date).delete()
    user = auth.authenticate(user_id=user_id, token=token)
    if user and user.is_active:
        auth.login(request, user)
    return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')


@login_required
def feeds(request):
    if request.method == 'POST':
        url = request.POST.get('url', '').strip()
        if url and not url.endswith('://'):
            feed = create_feed(url)
            feed.subscriptions.create(user=request.user)
        return redirect('index')
    false_value = 0 if 'sqlite' in settings.DATABASES['default']['ENGINE'] else 'false'
    count_sql = """
        SELECT count(s.id)
        FROM reader_story s
        LEFT OUTER JOIN reader_readstory rs ON rs.story_id = s.id AND rs.user_id = %(user_id)s
        WHERE s.feed_id = reader_feed.id AND (rs.is_read = %(false)s OR rs.is_read IS NULL)
    """ % {'user_id': request.user.pk, 'false': false_value}
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/feeds.html' % f, {
        'smart_feeds': request.user.smart_feeds.all(),
        'feeds': Feed.objects.filter(subscriptions__user=request.user).extra(select={
            'unread_count': count_sql,
            'title_lower': 'lower(reader_feed.title)',
        }, order_by=('title_lower',)),
    })


@login_required
def feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    subscription = get_object_or_404(feed.subscriptions, user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        action = data.get('action', '').strip().lower()
        if action == 'read':
            mark_all_read([feed], request.user)
        elif action == 'unsubscribe':
            feed.subscriptions.filter(user=request.user).delete()
            ReadStory.objects.filter(user=request.user, story__feed=feed).delete()
        return HttpResponse(json.dumps({'action': action}), content_type='applcation/json')
    unread = get_stories([feed], request.user, read=False)
    if subscription.show_read > 0:
        since = datetime.date.today() - datetime.timedelta(days=subscription.show_read)
        last_read = get_stories([feed], request.user, read=True, since=since)
    elif subscription.show_read < 0:
        last_read = get_stories([feed], request.user, read=True, limit=abs(subscription.show_read))
    else:
        last_read = []
    stories = sorted(itertools.chain(unread, last_read), key=operator.attrgetter('date_published'), reverse=True)
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/stories.html' % f, {
        'title': smart_text(feed),
        'feed': feed,
        'stories': stories,
    })


@login_required
def feed_settings(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    subscription = feed.subscriptions.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('action', '').strip().lower() == 'unsubscribe':
            subscription.delete()
            ReadStory.objects.filter(user=request.user, story__feed=feed).delete()
        else:
            form = SettingsForm(request.POST, instance=subscription)
            if form.is_valid():
                form.save()
        return redirect('index')
    else:
        form = SettingsForm(instance=subscription)
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/settings.html' % f, {
        'feed': feed,
        'form': form,
    })


@login_required
def story(request, ident):
    story = get_object_or_404(Story, ident=ident)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        action = data.get('action', '').strip().lower()
        if action in ('star', 'unstar'):
            status, created = ReadStory.objects.get_or_create(story=story, user=request.user)
            status.is_starred = action == 'star'
            status.save()
        elif action in ('read', 'unread'):
            status, created = ReadStory.objects.get_or_create(story=story, user=request.user)
            status.is_read = action == 'read'
            status.save()
        return HttpResponse(json.dumps({'story': story.ident, 'action': action}), content_type='applcation/json')
    status, created = ReadStory.objects.get_or_create(story=story, user=request.user)
    status.is_read = True
    status.save()
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/story.html' % f, {
        'story': story,
        'status': status,
        'first_read': created,
    })


@login_required
def unread(request):
    feeds = Feed.objects.filter(subscriptions__user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        action = data.get('action', '').strip().lower()
        if action == 'read':
            mark_all_read(feeds, request.user)
        return HttpResponse(json.dumps({'action': action}), content_type='applcation/json')
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/stories.html' % f, {
        'title': 'Unread Stories',
        'stories': get_stories(feeds, request.user, read=False),
        'extra_info': True,
    })


@login_required
def starred(request):
    feeds = Feed.objects.filter(subscriptions__user=request.user)
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        action = data.get('action', '').strip().lower()
        if action == 'read':
            mark_all_read(feeds, request.user)
        return HttpResponse(json.dumps({'action': action}), content_type='applcation/json')
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/stories.html' % f, {
        'title': 'Starred',
        'stories': get_stories(feeds, request.user, starred=True),
        'extra_info': True,
    })


@login_required
def search(request):
    feeds = Feed.objects.filter(subscriptions__user=request.user)
    query = request.GET.get('q', '').strip()
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/stories.html' % f, {
        'title': query,
        'stories': get_stories(feeds, request.user, query=query) if query else None,
        'extra_info': True,
        'search': True,
    })


@login_required
def smart_feed(request, feed_id):
    feed = get_object_or_404(SmartFeed, pk=feed_id, user=request.user)
    search_feeds = Feed.objects.filter(subscriptions__user=request.user)
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/stories.html' % f, {
        'title': smart_text(feed),
        'feed': feed,
        'stories': get_stories(search_feeds, request.user, query=feed.query),
        'extra_info': True,
    })
