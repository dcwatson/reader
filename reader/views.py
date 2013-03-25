from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.models import Site
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from reader.models import Feed, Story, User, UserManager, LoginToken, ReadStory
from reader.utils import get_stories, ajaxify, create_feed
import json

@login_required
def index(request):
    return render(request, 'reader/index.html', {
    })

def login(request):
    if request.method == 'POST':
        email = UserManager.normalize_email(request.POST.get('email', '').strip())
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
        })
        user.send_email('Reader Login', message)
    return render(request, 'reader/login.html', {
    })

def email_login(request, user_id, token):
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
    return render(request, 'reader/parts/feeds.html', {
        'feeds': Feed.objects.filter(subscriptions__user=request.user).extra(select={
            'unread_count': count_sql,
        }),
    })

@login_required
def feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action', '').strip().lower()
        if action == 'read':
            for s in get_stories([feed], request.user, read=False):
                status, created = ReadStory.objects.get_or_create(story=s, user=request.user)
                status.is_read = True
                status.save()
        return HttpResponse(json.dumps({'action': action}), content_type='applcation/json')
    if not feed.subscriptions.filter(user=request.user).exists():
        print request.user, 'is not subscribed to', feed
    return render(request, 'reader/parts/stories.html', {
        'title': unicode(feed),
        'feed': feed,
        'stories': get_stories([feed], request.user),
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
    return render(request, 'reader/parts/story.html', {
        'story': story,
        'status': status,
        'first_read': created,
    })

@login_required
def unread(request):
    return render(request, 'reader/parts/stories.html', {
        'title': 'Unread Stories',
        'stories': get_stories(Feed.objects.filter(subscriptions__user=request.user), request.user, read=False),
    })

@login_required
def starred(request):
    return render(request, 'reader/parts/stories.html', {
        'title': 'Starred',
        'stories': get_stories(Feed.objects.filter(subscriptions__user=request.user), request.user, starred=True),
    })
