from django.shortcuts import render
from django.http import JsonResponse
from inform import models as inform_models
import datetime
from django.utils import timezone
# Create your views here.
import general.bot_inform as bot_inform
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
    if request.method == 'POST':
        otvet = dict(request.POST)
        bot_inform.sent_to_atknin_bot(str(otvet), 'v') # проинформируем в telegramm bot
        del otvet['csrfmiddlewaretoken']
        for key in otvet:
            num_vopros = int(str(key).split('_')[1])
            question = inform_models.questions.objects.get(id=num_vopros)
            if str(key).split('_')[0]=='voprosnum':
                num_otvet = str(otvet[key][0])
                otv_bd = inform_models.answers.objects.create(questions = question,
                                                              number = float(num_otvet))
            else:
                num_otvet = int(str(otvet[key][0]).split('_')[1])
                question_choose = inform_models.question_choose.objects.get(id=num_otvet)
                otv_bd = inform_models.answers.objects.create(questions = question,
                                                              question_choose = question_choose)
            try:
                user = inform_models.participants.objects.filter(ip=request.META['REMOTE_ADDR']).reverse()[0]
                otv_bd.user = user
                otv_bd.save()
            except Exception as e:
                bot_inform.sent_to_atknin_bot(str(e), 'v') # проинформируем в telegramm bot
                otv_bd.save()
        bot_inform.sent_to_atknin_bot(str(otvet), 'v') # проинформируем в telegramm bot
        return render(
            request, 'inform/questions.html',argv
            )
    else:
        today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
        today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
        argv['questions'] = inform_models.questions.objects.filter(DateTime__range=(today_min, today_max))
        return render(
            request, 'inform/questions.html',argv
            )
