from django.http import HttpResponse
import simplejson as json
from models import *
import twitter
import sys

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


