# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse
from inform import models as inform_models
import datetime
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
import time
from inform.smsc_api import *
import datetime
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
                # bot_inform.sent_to_atknin_bot(str(e), 'v') # проинформируем в telegramm bot
                otv_bd.save()
        # bot_inform.sent_to_atknin_bot(str(otvet), 'v') # проинформируем в telegramm bot
        argv['time'] = timezone.localtime(timezone.now())
        return render(
            request, 'inform/bye.html',argv
            )
    else:
        today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
        today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
        argv['questions'] = inform_models.questions.objects.filter(DateTime__range=(today_min, today_max))
        return render(
            request, 'inform/questions.html',argv
            )

def questions_results(request):
    argv = {}
    today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
    today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
    result = inform_models.answers.objects.filter(DateTime__range=(today_min, today_max))
    argv['total_answers'] = len(result)
    argv['results'] = {}
    for i in result:
        if str(i.questions.types.text) == 'number':
            if i.questions in argv['results']:
                argv['results'][i.questions]['result'] += i.number
                argv['results'][i.questions]['N'] += 1
            else:
                argv['results'][i.questions] = {}
                argv['results'][i.questions]['result'] = i.number
                argv['results'][i.questions]['N'] = 1
        else:
            if i.questions in argv['results']:
                if i.question_choose in argv['results'][i.questions]:
                    argv['results'][i.questions][i.question_choose] += 1
                else:
                    argv['results'][i.questions][i.question_choose] = 1
            else:
                argv['results'][i.questions] = {}

    # bot_inform.sent_to_atknin_bot(str(argv['results']), 'v') # проинформируем в telegramm bot
    if request.is_ajax():
        return JsonResponse(argv)
        bot_inform.sent_to_atknin_bot('ds', 'v') # проинформируем в telegramm bot
    else:
        return render(
            request, 'inform/questions_results.html',argv
            )

def manage(request):
    if request.is_ajax():
        try:
            if 'email' in request.POST:
                today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
                today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
                users = inform_models.participants.objects.filter(DateTime__range=(today_min, today_max))
                for user in users:
                    topic = 'СМУ ФНИЦ КиФ: {}:)'.format(user.Name)
                    body = '''Привет {}, 18 августа состоиться СОБРАНИЕ молодых ученых института. До начала 10 дней.
                     УБЕДИТЕЛЬНАЯ ПРОСЬБА к молодым сотрудникам - не игнорировать данный курс лекций и
                     уважать труд лекторов!!! С Уважением, Наша Команда'''.format(user.Name)
                    try:
                        html_message = loader.render_to_string('inform/email.html',
                                                               {'user_name': user.Name})
                        send_mail(topic, body, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
                        bot_inform.sent_to_atknin_bot('Успешно ' + user.email , 'v') # проинформируем в telegramm bot
                    except Exception as e:
                        bot_inform.sent_to_atknin_bot('Ошибка: '+user.email+'. '+str(e), 'v') # проинформируем в telegramm bot
                    time.sleep(0.5)
            elif 'sms' in request.POST:
                today_min = datetime.datetime.combine(timezone.now().date(), datetime.time.min)
                today_max = datetime.datetime.combine(timezone.now().date(), datetime.time.max)
                users = inform_models.participants.objects.filter(DateTime__range=(today_min, today_max))
                for user in users:
                    try:
                        smsc = SMSC()
                        r = smsc.send_sms('+'+user.phone, "{}, завтра состоится мероприятие в 506 к. в 16:00. Ваш СМУ".format(user.Name))
                        balance = smsc.get_balance()
                        bot_inform.sent_to_atknin_bot("Успешно для "+user.Name+'. Баланс: ' + str(balance), 'v') # проинформируем в telegramm bot
                    except Exception as e:
                        bot_inform.sent_to_atknin_bot('Ошибка sms('+user.Name+'). ' + str(e), 'v') # проинформируем в telegramm bot
                    time.sleep(1)
        except Exception as e:
            bot_inform.sent_to_atknin_bot(str(e), 'v') # проинформируем в telegramm bot
    argv = {}
    return render(
        request, 'inform/manage.html',argv
        )
