from django.shortcuts import render
from library import models as library_models

# Create your views here.
def index(request):
    arg = {}
    arg['library'] = library_models.labrary.objects.all()
 	return render(
	 	request, 'library/index.html',
	 	)

def add(request):
 	return render(
	 	request, 'general/about.html',
	 	)
