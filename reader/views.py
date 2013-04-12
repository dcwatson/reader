from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpResponse
from django.conf import settings
from reader.models import Feed, Story, User, UserManager, LoginToken, ReadStory
from reader.utils import get_stories, ajaxify, create_feed, mark_all_read
from reader.forms import SettingsForm
import itertools
import operator
import datetime
import json

@login_required
def index(request):
    return render(request, 'reader/index.html', {
    })

def login(request):
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
    count_sql = """
        SELECT count(s.id)
        FROM reader_story s
        LEFT OUTER JOIN reader_readstory rs ON rs.story_id = s.id AND rs.user_id = %(user_id)s
        WHERE s.feed_id = reader_feed.id AND (rs.is_read = 0 OR rs.is_read IS NULL)
    """ % {'user_id': request.user.pk}
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/feeds.html' % f, {
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
        data = json.loads(request.body)
        action = data.get('action', '').strip().lower()
        if action == 'read':
            mark_all_read([feed], request.user)
        elif action == 'unsubscribe':
            feed.subscriptions.filter(user=request.user).delete()
            ReadStory.objects.filter(user=request.user, story__feed=feed).delete()
        return HttpResponse(json.dumps({'action': action}), content_type='applcation/json')
    since = datetime.date.today() - datetime.timedelta(days=subscription.show_read)
    unread = get_stories([feed], request.user, read=False)
    last_read = get_stories([feed], request.user, read=True, since=since)
    stories = sorted(itertools.chain(unread, last_read), key=operator.attrgetter('date_published'), reverse=True)
    f = 'parts' if request.is_ajax() else 'mobile'
    return render(request, 'reader/%s/stories.html' % f, {
        'title': unicode(feed),
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
        data = json.loads(request.body)
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
        data = json.loads(request.body)
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
        data = json.loads(request.body)
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
