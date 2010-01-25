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


