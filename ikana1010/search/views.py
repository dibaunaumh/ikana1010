from models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator


def home(request):
    return render_to_response("search.html", locals())



def search(request):
    concept = request.GET["q"] if "q" in request.GET else "No query specified"
    x = float(request.GET["location_x"]) if "location_x" in request.GET else 0.0  
    y = float(request.GET["location_y"]) if "location_y" in request.GET else 0.0
    
    return HttpResponse("{ 'concept': '%s', x: %f; y: %f }" % (concept, x, y), mimetype='application/json')