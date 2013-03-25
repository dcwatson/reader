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
        'site': Site.objects.get_current(),
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
        'site': Site.objects.get_current(),
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
    if not feed.subscriptions.filter(user=request.user).exists():
        print request.user, 'is not subscribed to', feed
#    response = ajaxify(feed)
#    response['stories'] = [ajaxify(s, extra=('is_read', 'is_starred', 'notes')) for s in get_stories([feed], request.user)]
#    return HttpResponse(json.dumps(response, indent=4), content_type='application/json')
    return render(request, 'reader/parts/stories.html', {
        'feed': feed,
        'stories': get_stories([feed], request.user),
    })

@login_required
def story(request, feed_id, story_id):
    story = get_object_or_404(Story, pk=story_id, feed__pk=feed_id)
    status, created = ReadStory.objects.get_or_create(story=story, user=request.user)
    return render(request, 'reader/parts/story.html', {
        'story': story,
        'status': status,
    })
