from models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D 
from django.core import serializers
import sys
import simplejson

def home(request):
    return render_to_response("search.html", locals())



def search(request):
    #Parse request
    concept = request.GET["q"] if "q" in request.GET else "No query specified"
    pntwkt  = request.GET["location"] if "location" in request.GET else 'POINT(0.0 0.0)'    
    
    #Create GEOS Geometry object to future usage in GIS queries 
    pnt = fromstr(pntwkt)
    
    json = "{}"
    try:
        messages = Message.objects.filter(location__distance_lte=(pnt, D(km=10))).filter(concepts__concept__name=concept)
                      
        results = []
        for msg in messages:
            for c in msg.concepts.filter(concept__name=concept):
                results.append({ "person_username": c.person.name, "concept": c.concept.name, "message": msg.contents, "x": msg.get_x(), "y": msg.get_y() })
            
        
        json = simplejson.dumps(results)
    except:
        print sys.exc_info()
    #Return the response back
    return HttpResponse(json, mimetype='application/json')


