import datetime
import hashlib
import time

def get_story_content(data):
    if 'content' in data:
        return data['content'][0]['value'].strip()
    elif 'summary' in data:
        return data['summary'].strip()
    return u''

def get_story_date(data):
    if 'published_parsed' in data:
        return datetime.datetime.fromtimestamp(time.mktime(data['published_parsed']))
    elif 'updated_parsed' in data:
        return datetime.datetime.fromtimestamp(time.mktime(data['updated_parsed']))
    return datetime.datetime.now()

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
