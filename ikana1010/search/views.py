from models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D 
from django.core import serializers
import sys
import simplejson
import logging
import urllib, urllib2


def home(request):
    #Retrieve TOP 10 Matches
    top_matches = Match.objects.all().order_by('-id')[:10]
    
    messges = []
    persons = set()
    for match in top_matches:
        if match.person1 in persons:
            persons.add(match.person1)
            
            res = match.person1.messages.order_by('-last_update')
            if len(res) > 0: 
                messges.append(res[0])
        
        if not match.person2 in persons:
            persons.add(match.person2)
            
            res = match.person2.messages.order_by('-last_update')
            if len(res) > 0: 
                messges.append(res[0])
        
    print "Found messges: ", len(messges)
    print "Found matches: ", len(top_matches)
    
    return render_to_response("index.html", locals())

def get_last_user_message(person):
    try:
        return person.messages.order_by('-last_update')
    except:
        pass
    
def search(request):
    #Parse request
    concept = request.GET["q"] if "q" in request.GET else "No query specified"
    distance = int(request.GET["d"]) if "d" in request.GET else 5
    pntwkt  = request.GET["location"] if "location" in request.GET else 'POINT(0.0 0.0)'    
    
    #Create GEOS Geometry object to future usage in GIS queries 
    pnt = fromstr(pntwkt)
    
    json = "{}"
    try:
        messages = Message.objects.filter(location__distance_lte=(pnt, D(km=distance)))
        print "before: ", messages.count()
        
        messages = messages.filter(concepts__concept__name=concept)
        print "after: ", messages.count()
                       
        results = []
        for msg in messages:
            for c in msg.concepts.filter(concept__name=concept):
                results.append({ "person_username": c.person.name, "concept": c.concept.name, "message": msg.contents, "x": msg.get_x(), "y": msg.get_y() })
            
        
        json = simplejson.dumps(results)
    except:
        print sys.exc_info()
    #Return the response back
    return HttpResponse(json, mimetype='application/json')



def receive_messages(request):
    json = request.POST["json"]
    try:
        data = simplejson.loads(json)
        # add if needed the persons
        persons = {}
        for p in data['persons']:
            person = create_person(p['fields'])
            persons[p['pk']] = person   # map persons by their primary key in the injector, which will be the reference in the messages
        # add if needed the messages
        messages = []
        for m in data['messages']:
            message = create_message(m['fields'], persons)
            messages.append(message)
        # extract & add the concepts
        
    except:
        print sys.exc_info()
    return HttpResponse("Received messages in JSON format:<br/>%s" % json)



def create_person(p):
    query = Person.objects.filter(username=parse_unicode(p['username']))
    if len(query) == 0:
        person = Person()
    else:
        person = query[0]
    person.username = parse_unicode(p['username'])
    person.external_id = parse_unicode(p['external_id'])
    person.name = parse_unicode(p['name'])
    person.profile = parse_unicode(p['profile'])
    person.link = parse_unicode(p['link'])
    person.picture = parse_unicode(p['picture'])
    person.source = create_data_source(parse_unicode(p['data_source']))
    person.save()
    person.location_string = parse_unicode(p['location_string'])
    person.location_wkt = parse_unicode(p['location_wkt'])
    return person


def create_message(m, persons):
    message = Message()
    message.external_url = m['external_url']
    message.contents = parse_unicode(m['contents'])
    person = persons[m['person']]
    message.user = person
    message.source = create_data_source(parse_unicode(m['data_source']))
    location_string = parse_unicode(m['location_string']) or person.location_string
    location_wkt = parse_unicode(m['location_wkt']) or person.location_wkt
    message.created_at = m['posted_at']
    if location_wkt:
        message.location = fromstr(location_wkt)
    else:
        message.location = geocode(location_string)
    message.save()
    return message


def parse_unicode(u):
    if u:
        return u.encode("utf-8")
    else:
        return None


def create_data_source(source):
    query = DataSource.objects.filter(name=source)
    if len(query) == 0:
        ds = DataSource()
        ds.name = source
        ds.save()
    else:
        ds = query[0]
    return ds


def geocode(str):
    service_url = "http://maps.google.com/maps/geo?"
    key = "ABQIAAAANcexVU-PTYxrvhlhfETtrRSviK87wC1D4ZXd6SUwo7wtUQVNOxQHWkEN8vWrkqYxypQwuLMe_prApQ"
    
    wkt = 'POINT(0.0 0.0)'
    if str != None and len(str) > 0:
        try:
            service_url = service_url + "q=%s" % str.replace(" ", "+")
            service_url = service_url + "&key=%s" % key
            service_url = service_url + "&output=json"
            service_url = service_url + "&sensor=false"
            result = "{}"
            response = urllib2.urlopen(service_url)
            result = response.read()
            json = simplejson.loads(result)
            coords = json['Placemark'][0]['Point']['coordinates']
            wkt = 'POINT(%s %s)' % (coords[0], coords[1])
        except:
            print sys.exc_info()
    return fromstr(wkt) 
    