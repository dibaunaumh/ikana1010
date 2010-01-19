from models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D 


def home(request):
    return render_to_response("search.html", locals())



def search(request):
    #Parse request
    concept = request.GET["q"] if "q" in request.GET else "No query specified"
    pntwkt  = request.GET["location"] if "location" in request.GET else 'POINT(0.0 0.0)'    
    
    #Create GEOS Geometry object to future usage in GIS queries 
    pnt = GEOSGeometry(pntwkt)
    
    #Return the response back
    return HttpResponse("{ 'concept': '%s', WKT: %s}" % (concept, pntwkt), mimetype='application/json')