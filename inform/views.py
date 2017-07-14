from django.shortcuts import render
from django.http import JsonResponse
from inform import models as inform_models
import datetime
# Create your views here.
def index(request):
    if request.is_ajax():
        out_data = {}
        try:
            participant = inform_models.participants.objects.create(Name = request.POST['Name'],
                                                                    LastName = request.POST['LastName'],
                                                                    email = request.POST['email'],
                                                                    phone = request.POST['phone'])
            try:
                participant.ip = request.META['REMOTE_ADDR']
                participant.save()
            except Exception as e:
                participant.save()
            out_data['status'] = 'успешно'
            return JsonResponse(out_data)
        except Exception as e:
            out_data['status'] = 'безуспешно'
            return JsonResponse(out_data)

    else:
     	return render(
    	 	request, 'inform/index.html',
    	 	)
def questions(request):
    argv = {}
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    argv['questions'] = inform_models.questions.objects.objects.filter(DateTime__gt=yesterday)
    return render(
        request, 'inform/questions.html',argv
        )
