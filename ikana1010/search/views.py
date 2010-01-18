from models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator


def home(request):
    return render_to_response("search.html", locals())



def search(request):
    concept = request.GET["q"] if "q" in request.GET else "No query specified"
    return HttpResponse("{ 'concept': '%s' }" % concept, mimetype='application/json')