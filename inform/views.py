from django.shortcuts import render
from django.http import JsonResponse
from inform import models as inform_models
from datetime import date
from django.utils import timezone
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
    today = date.today()
    today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
    today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
    argv['questions'] = inform_models..objects.get(DateTime__range=(today_min, today_max))
    return render(
        request, 'inform/questions.html',argv
        )
