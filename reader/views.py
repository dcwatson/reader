from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from reader.models import Feed, Story
from reader.utils import get_stories
import datetime
import json

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

def index(request):
    return render(request, 'reader/index.html', {
        'feeds': Feed.objects.filter(subscriptions__user=request.user),
    })

def feeds(request):
    pass

def feed(request, feed_id):
    feed = get_object_or_404(Feed, pk=feed_id)
    if not feed.subscriptions.filter(user=request.user).exists():
        print request.user, 'is not subscribed to', feed
    response = ajaxify(feed)
    response['stories'] = [ajaxify(s, extra=('is_read', 'is_starred', 'notes')) for s in get_stories([feed], request.user)]
    return HttpResponse(json.dumps(response, indent=4), content_type='application/json')

def story(request, feed_id, story_id):
    story = get_object_or_404(Story, pk=story_id, feed__pk=feed_id)
