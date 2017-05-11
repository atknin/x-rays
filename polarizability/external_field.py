from __future__ import unicode_literals
from django.shortcuts import render
from django.core import serializers
from polarizability import models as polarizability_models
from diffraction import models as diffraction_models

from django.http import HttpResponse
import general.bot_inform as bot_inform
import sys, math, cmath, os, re#, scipy # re - для работы с регулярными выражениями
# import numpy as np
from django.http import JsonResponse
import numpy as np
import time
import os


def compute(request):

	# bot_inform.sent_to_atknin_bot('ok', 'v') # проинформируем в telegramm bot
	d14 = 4.7*math.pow(10,-12)
	d11 =  6.5*math.pow(10,-12)
	V_volt = float(request.POST['volt'])
	D_pl = float(request.POST['sample_width'])*math.pow(10,-3)
	message = {}
	message['status'] = ''
	path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/polarizability/'
	cromer_man_file = open(path+'files_for_compute/f0_CromerMann.dat')
	f1f2 = open(path+'files_for_compute/f1f2_Chantler.dat')
	hkl = request.POST['h'],request.POST['k'],request.POST['l']
	crystal_id = request.POST['crystal_id']
	crystal = polarizability_models.crystals.objects.get(pk = crystal_id)


	a_element= set() # множесто названий элементов
	a_element_dict= {}
	wavelength = float(request.POST['wavelength']) # длина волны падающего излучения в Ангстремах

	aprmtr = float(crystal.a) * (1+d11*V_volt/D_pl)# параметр решетки a
	bprmtr = float(crystal.b)* (1-2*d11*V_volt/D_pl) # параметр решетки b
	cprmtr = float(crystal.c) # параметр .cрешетки c
	rho = float(crystal.density)*math.pow(10,6)# плотночть соединения в г/м3
	hInd = int(request.POST['h'], 10) # индекс миллера h
	kInd = int(request.POST['k'], 10) # индекс миллера k
	lInd = int(request.POST['l'], 10) # индекс миллера l
	assym = int(request.POST['assym_alfa_then_beta'])


	hInd_surface = int(request.POST['h_surface'], 10) # индекс миллера h
	kInd_surface = int(request.POST['k_surface'], 10) # индекс миллера k
	lInd_surface = int(request.POST['l_surface'], 10) # индекс миллера l



	alfaprmtr = math.radians(float(crystal.alfa)) # угол альфа решетки в радианах
	betaprmtr = math.radians(float(crystal.beta)) # угол бета решетки
	gammaprmtr = math.radians(float(crystal.gamma)) - math.atan(d14*V_volt/D_pl) # угол гамма решетки
	V = aprmtr*bprmtr*cprmtr*math.sqrt(1-math.pow(math.cos(alfaprmtr),2)-math.pow(math.cos(betaprmtr),2)-math.pow(math.cos(gammaprmtr),2)+2*math.cos(alfaprmtr)*math.cos(betaprmtr)*math.cos(gammaprmtr))

	# расчет межплоскостного расстояния ––––––––––––––––––
	aprmtr_ = bprmtr*cprmtr*math.sin(alfaprmtr)/V
	bprmtr_ = cprmtr*aprmtr*math.sin(betaprmtr)/V
	cprmtr_ = aprmtr*bprmtr*math.sin(gammaprmtr)/V

	COSalfaprmtr_ =  ( math.cos(betaprmtr)*math.cos(gammaprmtr)-math.cos(alfaprmtr) )/( math.sin(betaprmtr)*math.sin(gammaprmtr) )
	COSbetaprmtr_ =  ( math.cos(gammaprmtr)*math.cos(alfaprmtr)-math.cos(betaprmtr) )/( math.sin(gammaprmtr)*math.sin(alfaprmtr) )
	COSgammaprmtr_ = ( math.cos(alfaprmtr)*math.cos(betaprmtr)-math.cos(gammaprmtr) )/( math.sin(alfaprmtr)*math.sin(betaprmtr)  )
	s1 = math.pow( ( hInd * aprmtr_) ,2) + math.pow( ( kInd * bprmtr_) ,2) + math.pow( ( lInd * cprmtr_) ,2)
	s2 = 2*hInd*kInd*aprmtr_*bprmtr_*COSgammaprmtr_
	s3 = 2*kInd*lInd*COSalfaprmtr_
	s4 = 2*hInd*lInd*aprmtr_*cprmtr_*COSbetaprmtr_
	dprmtr = math.sqrt(1/(s1+s2+s3+s4)) # *10^-10

	C=1 # в случае сигма поляризации, в случае пи()=cos(2*Тета_breg)

	StructFactorReal = 0
	StructFactorImag=0 # обнуляем структурный фактор
	StructFactor0 = 0
	SumOcupAtomWeight = 0

	try:
		crystalGeom = open(path+"structure/"+crystal.name+'.dat').readlines() # открыл файл с геометрие элементарной ячейки
	except Exception as e:
		message['error'] = "структура не найдена"
		return JsonResponse(message)

	#––––––––––––––––––––объем элементарной ячейки* 10^-30–––––––––––––––––––––
	V = aprmtr*bprmtr*cprmtr*math.sqrt(1-math.pow(math.cos(alfaprmtr),2)-math.pow(math.cos(betaprmtr),2)-math.pow(math.cos(gammaprmtr),2)+2*math.cos(alfaprmtr)*math.cos(betaprmtr)*math.cos(gammaprmtr))

	# расчет межплоскостного расстояния ––––––––––––––––––
	aprmtr_ = bprmtr*cprmtr*math.sin(alfaprmtr)/V
	bprmtr_ = cprmtr*aprmtr*math.sin(betaprmtr)/V
	cprmtr_ = aprmtr*bprmtr*math.sin(gammaprmtr)/V

	COSalfaprmtr_ =  ( math.cos(betaprmtr)*math.cos(gammaprmtr)-math.cos(alfaprmtr) )/( math.sin(betaprmtr)*math.sin(gammaprmtr) )
	COSbetaprmtr_ =  ( math.cos(gammaprmtr)*math.cos(alfaprmtr)-math.cos(betaprmtr) )/( math.sin(gammaprmtr)*math.sin(alfaprmtr) )
	COSgammaprmtr_ = ( math.cos(alfaprmtr)*math.cos(betaprmtr)-math.cos(gammaprmtr) )/( math.sin(alfaprmtr)*math.sin(betaprmtr)  )
	s1 = math.pow( ( hInd * aprmtr_) ,2) + math.pow( ( kInd * bprmtr_) ,2) + math.pow( ( lInd * cprmtr_) ,2)
	s2 = 2*hInd*kInd*aprmtr_*bprmtr_*COSgammaprmtr_
	s3 = 2*kInd*lInd*COSalfaprmtr_
	s4 = 2*hInd*lInd*aprmtr_*cprmtr_*COSbetaprmtr_
	dprmtr = math.sqrt(1/(s1+s2+s3+s4)) # *10^-10

	predel_hkl = wavelength/2/dprmtr
	if predel_hkl>1:
		message['error'] = "Из условия Брегга, wavelength/2d > 1 ("+str(round(predel_hkl,4))+"): пробуйте меньшие hkl "
		return JsonResponse(message)
	# #––––––––––––––––––расчет Тета угла Брегга----–––––––––––––––––––––––
	tetaprmtr = math.asin(wavelength/2/dprmtr) # в радианах
	#-----------Угол между поверхностью и плоскостью---------

	s1_surface = math.pow( ( hInd_surface * aprmtr_) ,2) + math.pow( ( kInd_surface * bprmtr_) ,2) + math.pow( ( lInd_surface * cprmtr_) ,2)
	s2_surface = 2*hInd_surface*kInd_surface*aprmtr_*bprmtr_*COSgammaprmtr_
	s3_surface = 2*kInd_surface*lInd_surface*COSalfaprmtr_
	s4_surface = 2*hInd_surface*lInd_surface*aprmtr_*cprmtr_*COSbetaprmtr_
	dprmtr_surface = math.sqrt(1/(s1_surface+s2_surface+s3_surface+s4_surface)) # *10^-10


	s5_surface = hInd*hInd_surface*math.pow(aprmtr_,2)+kInd*kInd_surface*math.pow(bprmtr_,2)+lInd*lInd_surface*math.pow(cprmtr_,2)
	s6_surface = (kInd_surface*lInd+lInd_surface*kInd)*bprmtr_*cprmtr_*COSalfaprmtr_
	s7_surface = (hInd_surface*lInd+lInd_surface*hInd)*aprmtr_*cprmtr_*COSbetaprmtr_
	s8_surface = (hInd_surface*kInd+kInd_surface*hInd)*aprmtr_*bprmtr_*COSgammaprmtr_
	s9_surface = s5_surface+s6_surface+s7_surface+s8_surface
	s10_surface = dprmtr_surface * dprmtr * s9_surface
	if s10_surface > 1:
		s10_surface = 1

	try:
		fi = assym*abs(float(request.POST['fi_prmtr']))
	except Exception as e:
		fi = assym*math.degrees( math.acos( s10_surface ) ) #проверка

	if abs(math.radians(fi))>=tetaprmtr:
		fi = 0
		message['status'] += ' Угол асимметрии больше угла Брегга!\n'
	#-----------Гамма 0 и Гамма h - направляющие косинусы---------
	gamma_0 = math.sin(math.radians(fi) + tetaprmtr)
	gamma_h = math.sin(math.radians(fi) - tetaprmtr)
	b=gamma_0/abs(gamma_h) # коэффициент ассиметрии брэговского отражения

	# ---------фактор Дебая - Валлера, по идее должен вычисляться для разных атомов по разному
	B=8*math.pow((math.pi*0.08*math.pow(10,-10)), 2)
	DedayFactor = math.exp(-B*math.pow((math.sin(tetaprmtr)/(wavelength*math.pow(10,-10))),2))

	# #–––––––––––––––––––––––––#считаем структурный фактор––––––––––––––––––––––
	Natom = len(crystalGeom)# колличество эллементов в элементарной ячейке
	for i in range(Natom):
		if len(crystalGeom[i].split()) == 5:
			NXYZocup = crystalGeom[i].split() # в файле геометрии бежим по строкам
		else:
			continue
		f0=0# обнуляем коэффициен для следующего атома в ячейке
		#___найти строку с элементом в cromerMan__________________________________________________________________________________________________________________________
		while True:
			line = cromer_man_file.readline()
			if re.search(r'#S  '+NXYZocup[0], line): # нашли строку с элементом
				cromer_man_file.readline() # две строки отступили
				element_name = re.split(r'  ', line)[2]
				cromer_man_file.readline() # третья будет наша с коэффициентами
				line = cromer_man_file.readline() # строка в файле кромер мана с соответствующими индексами
				cromer_man_file.seek(0) # возвращаем каретку в началао файла
				abc = re.split(r'   ', line)
				break
		# __считаем f0________________________________________________________________________________________________________________
		for k in range(0, 4):

			f0 = f0+float(abc[k])*math.exp(-float(abc[k+5])*math.pow((math.sin(tetaprmtr)/wavelength),2))# длинна волны в ангстремах
		f0=f0+float(abc[4])


    	#___найти строку с элементом в f1f2_Chantler.dat__________________________________________________________________________________________________________________________
		while True:
			line = f1f2.readline()
			if re.search(r'#S  '+NXYZocup[0], line): # нашли строку с элементом
				while True: # переберем еще строки
					line = f1f2.readline() # первая строка в файле f1f2_Chantler.dat по энергии
					AtomicWeightLine = line
					if re.search(r'#UO  Atomic weight =', line):
						while True:
							line = f1f2.readline()
							if re.search(r'#UO   keV', line):
								while True:
									f1f2_1 = line # это первая линия для интерполяции, но она str
									line = f1f2.readline()
									f1f2_2 = line.split()   # это вторая линия но уже разделеная
									if float(f1f2_2[6]) < wavelength*math.pow(10,-1):
										break
								break
						break
				f1f2.seek(0) # возвращаем каретку в началао файла
				#abc = re.split(r'   ', line)
				break
		f1f2_1 = f1f2_1.split() # разделили 1 строку для интерполяции, вторая разделена в цикле для предварительного сравнения
		#_____________________________________________________________________________________________________________________________

		#------для f1---------
		f1_1 = float(f1f2_1[1])
		f1_2 = float(f1f2_2[1])
		#----------------------
		lambd1 = float(f1f2_1[6])
		lambd2 = float(f1f2_2[6])
		#------для f2---------
		f2_1 = float(f1f2_1[2])
		f2_2 = float(f1f2_2[2])
		#-----------------f1 and f2 -----
		f1 = f1_1 + (wavelength*math.pow(10,-1)-lambd1)*((f1_2-f1_1)/(lambd2-lambd1))
		f2 = f2_1 + (wavelength*math.pow(10,-1)-lambd1)*((f2_2-f2_1)/(lambd2-lambd1))
		# Атомный вес элемента--------------------------------------------
		AtomicWeight = float(AtomicWeightLine.split()[4]) # г/моль
		#------cтруктурный фактор для падающей волны, он другой ------

		StructFactor0 = StructFactor0 +float(NXYZocup[4])*(f1+f2*1j)
		StructFactorReal = StructFactorReal + float(NXYZocup[4])*(f0+f1-float(NXYZocup[0]))*cmath.exp(-2*1j*math.pi*(float(NXYZocup[1])*hInd+float(NXYZocup[2])*kInd+float(NXYZocup[3])*lInd))*DedayFactor
		StructFactorImag = StructFactorImag + float(NXYZocup[4])*f2*cmath.exp(-2*1j*math.pi*(float(NXYZocup[1])*hInd+float(NXYZocup[2])*kInd+float(NXYZocup[3])*lInd))*DedayFactor
		# --------стоит в знаменателе в поляризуемости падающей волны-------------
		SumOcupAtomWeight = SumOcupAtomWeight + float(NXYZocup[4])*AtomicWeight

	# Расчет поляризуемостей-------------------------------
	Relectron = 2.8179403267 * math.pow(10,-15) # радиус электрона в метрах
	Navogadro =  6.02214129 * math.pow(10,23)

	X0r = - Relectron*Navogadro*wavelength*math.pow(10,-10)*wavelength*math.pow(10,-10)*rho*StructFactor0/math.pi/SumOcupAtomWeight
	X0i =  Relectron*Navogadro*wavelength*math.pow(10,-10)*wavelength*math.pow(10,-10)*rho*StructFactor0/math.pi/SumOcupAtomWeight
	X0=X0r.real+X0i.imag*1j

	Xhr = Relectron*wavelength*math.pow(10,-10)*wavelength*math.pow(10,-10)*StructFactorReal/math.pi/V/math.pow(10, -30)
	Xhi = Relectron*wavelength*math.pow(10,-10)*wavelength*math.pow(10,-10)*StructFactorImag/math.pi/V/math.pow(10, -30)
	Xh=abs(Xhr)+abs(Xhi)*1j

	# сравнение коэффициенто для Х0 и Хh
	koef1=Navogadro*rho/SumOcupAtomWeight
	koef2=1/V/math.pow(10, -30)

	# Глубина экстинкции
	Ld = (wavelength*math.sqrt(abs(gamma_0)*abs(gamma_h)))/(math.pi*C*abs(Xh))

	# Полуширина кривой
	delta = 2*math.degrees(abs(C*cmath.sqrt(Xh.real*Xh.real+Xh.imag*Xh.imag)/(cmath.sqrt(b) * math.sin(2*tetaprmtr))))*3600

	# Смещение кривой
	sdvig = math.degrees(-X0.real*(1+b)/(2*b*math.sin(2*tetaprmtr)))*3600

# Собственная кривая кристалла -–––––––––––––––––––––––––––––––––––
	min_rasst_ot_centra = 100
	min_rasst_ot_centra_which_point = 100

	epslist = []
	x_epslist = []

	max_pow_R = 0
	for_downloading = ''

	point_for_curve = 100
	shag = (delta/point_for_curve)*math.pi/180/3600
	dTeta = sdvig*math.pi/180/3600 - 5*delta*math.pi/180/3600
	dTeta_end = sdvig*math.pi/180/3600 + 5*delta*math.pi/180/3600

	if Xh.real < 1e-12:
		message['status'] += "запрещенный рефлекс \n"
		message['forbidden'] = 1
	else:
		message['status'] += '; b = '+ str(bprmtr)+'; a = '+str(aprmtr)+'; d14 = '+str(d14)+ '; d11 = ' + 	str(d11) +"; V = "+ str(V_volt) + '; d = ' +	str(D_pl) + " \n"
		while dTeta<dTeta_end:
			dTeta+=shag
			alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr-dTeta)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
			prover = (1/4/gamma_0)*(X0*(1-b)-b*alfa+cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
			if prover.imag < 0:
				eps = (1/4/gamma_0)*(X0*(1-b)-b*alfa-cmath.sqrt(((X0*(1+b)+b*alfa)*(X0*(1+b)+b*alfa))-4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
			else:
				eps = prover
			R=(2*eps*gamma_0-X0)/Xh/C
			P = (abs(gamma_h)/gamma_0)*abs(R)*abs(R)
			epslist.append(P)
			x_epslist.append(dTeta*3600*180/math.pi)
			for_downloading+= str(dTeta*3600*180/math.pi)+'   '+str(P) + '\n'
			if max_pow_R<(P):
				max_pow_R = (P)
			if min_rasst_ot_centra > abs(sdvig*math.pi/180/3600 - dTeta):
				min_rasst_ot_centra = abs(sdvig*math.pi/180/3600 - dTeta)
				min_rasst_ot_centra_which_point = len(epslist)

		From_ = min_rasst_ot_centra_which_point - int(1.5*point_for_curve)
		To_ = min_rasst_ot_centra_which_point + int(1.5*point_for_curve)


		y = epslist[From_:To_:1]
		x = x_epslist[From_:To_:1]


		message['X0_real'] = str(round(X0.real*math.pow(10,7),4))
		message['X0_imag'] = str(round(X0.imag*math.pow(10,7),4))
		message['Xh_real'] = str(round(Xh.real*math.pow(10,7),4))
		message['Xh_imag'] = str(round(Xh.imag*math.pow(10,7),4))
		message['delta'] = str(round(delta,4))
		message['maximum'] = str(round(max_pow_R,4))
		message['x_darwin'] = x
		message['y_darwin'] = y
		message['for_downloading'] = for_downloading

	message['dprmtr'] = str(round(dprmtr, 4))
	message['extintion'] = str(round(Ld*1e-4, 3)) # микроны
	message['bragg'] = str(round(math.degrees(tetaprmtr), 4))
	message['sdvig'] = str(round(sdvig,4))
	message['fi'] = round(fi,1) # угол между плоскостью и поверхностью
	message['b'] =  round(b,3)
	message['bragg_precize'] = math.degrees(tetaprmtr)
	message['dprmtr_precize'] = dprmtr
	return message
