from django.http import HttpResponse
from models import *
import twitter
import sys
from django.conf import settings
from django.core import serializers
import httplib, urllib
import time
import simplejson



def fetch_messages(request):
    message_count = 0
    new_persons_count = 0

    #try:
        #client = twitter.Api(username=request.GET['user'], password=request.GET['password'])
    client = twitter.Api()
    latest_posts = client.GetPublicTimeline()
    #except:
    #    return HttpResponse(str(sys.exc_info()[1]))
    
    for post in latest_posts:
        query = Person.objects.filter(username=post.user.screen_name)
        if len(query) == 0:
            person = Person()
            new_persons_count = new_persons_count + 1
        else:
            person = query[0]
        person.name = post.user.name
        person.external_id = post.user.id
        person.username = post.user.screen_name
        person.link = post.user.url
        person.profile = post.user.description
        person.picture = post.user.profile_image_url
        person.location_string = post.user.location
        person.save()
        
        message = Message()
        message.contents = post.text
        message.person = person
        message.external_url = 'http://twitter.com/%s/status/%s' % (post.user.screen_name, post.id)
        if hasattr(post, "geo"):
            message.location_wkt = post.geo
        message.posted_at = post.created_at
        message.save()
        message_count = message_count + 1

    return HttpResponse("%d messages created by %d new persons." % (message_count, new_persons_count))


def push_messages(request):
    batch_size = settings.BATCH_SIZE
    messages = Message.objects.filter(pushed=False)
    nmessages = messages.count()
    nbatches = nmessages / batch_size
    actual_messages_sent = 0
    actual_batches_sent = 0
    conn = httplib.HTTPConnection(settings.MATCH_ENGINE)
    headers = {"Content-type": "application/json", "Accept": "text/html"}
    #for i in range(nbatches):
    for i in range(10):
        batch = messages[i * batch_size:(i+1) * batch_size]
        ids = [msg.person.id for msg in batch]
        messages_json = serializers.serialize("json", batch)
        persons = Person.objects.filter(id__in=ids)
        persons_json = serializers.serialize("json", persons)
        json = '{"persons": %s, "messages": %s}' % (persons_json, messages_json)
        params = urllib.urlencode({"json": json})
        conn.request("POST", "/receive_messages/", params, headers)
        response = conn.getresponse()
        if response.status == 200:
            print "Successfully pushed %d messages." % batch_size
            actual_batches_sent = actual_batches_sent + 1
            actual_messages_sent = actual_messages_sent + len(batch)
            for msg in batch:
                msg.pushed = True
                msg.save()
        else:
            print "Error in pushing messages (HTTP status code %d)" % response.status
            print response.read()
        time.sleep(0.2)

        # send the json by HTTP POST
        
    return HttpResponse("%d messages sent, in %d batches" % (actual_messages_sent, actual_batches_sent))

