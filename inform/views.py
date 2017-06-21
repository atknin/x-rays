from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    if request.is_ajax():
        Name = request.POST['Name']
        LastName = request.POST['LastName']
        email = request.POST['email']
        phone = request.POST['phone']
    else:
     	return render(
    	 	request, 'inform/index.html',
    	 	)
