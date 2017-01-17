# -*- coding: utf-8 -*-
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


# Create your views here.

def add_crystal(request):
	if request.is_ajax():
		message = {}
		try:
			path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/polarizability/'
			name = request.POST['id_name']
			if not polarizability_models.crystals.objects.filter(name=name).exists():	
				new = polarizability_models.crystals.objects.create(name=name)
				new.short_name = request.POST['id_short_name']
				new.crystal_system = request.POST['syngony']
				new.a = float(request.POST['id_a'])
				new.b = float(request.POST['id_b'])
				new.c = float(request.POST['id_c'])
				new.alfa = float(request.POST['id_alfa'])
				new.beta = float(request.POST['id_beta'])
				new.gamma = float(request.POST['id_gamma'])
				new.density = float(request.POST['id_density'])
				new.save()

				file = open(path+"structure/"+name+'.dat', 'w')
				geom = str(request.POST['id_geom']).split(' // ')
				for i in geom:
					file.write(str(i))
					file.write("\n")
				file.close()
				message['status'] = "Успешно добавлено в базу"
			else:
				message['status'] = "Такой кристалл уже существует"
			
		except Exception as e:
			message['status'] = e

		return JsonResponse(message)
	else:
		return render(
		 	request, 'polarizability/add_crystal.html'
		 	)

def compute(request):
	message = {}
	if request.is_ajax():
		path = os.path.realpath(os.path.dirname(sys.argv[0]))+'/polarizability/'
		cromer_man_file = open(path+'files_for_compute/f0_CromerMann.dat')
		f1f2 = open(path+'files_for_compute/f1f2_Chantler.dat')
		

		hkl = request.POST['h'],request.POST['k'],request.POST['l']
		crystal_id = request.POST['crystal_id']
		crystal = polarizability_models.crystals.objects.get(pk = crystal_id)

		
		a_element= set() # множесто названий элементов
		a_element_dict= {}
		wavelength = float(request.POST['wavelength']) # длина волны падающего излучения в Ангстремах

		aprmtr = float(crystal.a) # параметр решетки a
		bprmtr = float(crystal.b) # параметр решетки b
		cprmtr = float(crystal.c) # параметр .cрешетки c
		rho = float(crystal.density)*math.pow(10,6)# плотночть соединения в г/м3
		hInd = int(request.POST['h'], 10) # индекс миллера h
		kInd = int(request.POST['k'], 10) # индекс миллера k
		lInd = int(request.POST['l'], 10) # индекс миллера l

		hInd_surface = int(request.POST['h_surface'], 10) # индекс миллера h
		kInd_surface = int(request.POST['k_surface'], 10) # индекс миллера k
		lInd_surface = int(request.POST['l_surface'], 10) # индекс миллера l



		alfaprmtr = math.radians(float(crystal.alfa)) # угол альфа решетки в радианах
		betaprmtr = math.radians(float(crystal.beta)) # угол бета решетки
		gammaprmtr = math.radians(float(crystal.gamma)) # угол гамма решетки

		C=1 # в случае сигма поляризации, в случае пи()=cos(2*Тета_breg)
		
		StructFactorReal = 0
		StructFactorImag=0 # обнуляем структурный фактор
		StructFactor0 = 0
		SumOcupAtomWeight = 0
		crystalGeom = open(path+"structure/"+crystal.name+'.dat').readlines() # открыл файл с геометрие элементарной ячейки
		
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
		fi =  dprmtr_surface * dprmtr * s9_surface

		#-----------Гамма 0 и Гамма h - направляющие косинусы---------
		gamma_0 = math.cos(math.pi/2-tetaprmtr)
		gamma_h = math.cos(math.pi/2+tetaprmtr)
		b=-1 # коэффициент ассиметрии брэговского отражения
		#––––––––––––––––––––объем элементарной ячейки* 10^-30–––––––––––––––––––––

		V = aprmtr*bprmtr*cprmtr*math.sqrt(1-math.pow(math.cos(alfaprmtr),2)-math.pow(math.cos(betaprmtr),2)-math.pow(math.cos(gammaprmtr),2)+2*math.cos(alfaprmtr)*math.cos(betaprmtr)*math.cos(gammaprmtr))
		# ---------фактор Дебая - Валлера, по идее должен вычисляться для разных атомов по разному
		B=8*math.pow((math.pi*0.08*math.pow(10,-10)), 2)
		DedayFactor = math.exp(-B*math.pow((math.sin(tetaprmtr)/(wavelength*math.pow(10,-10))),2))

		# #–––––––––––––––––––––––––#считаем структурный фактор––––––––––––––––––––––
		
		Natom = len(crystalGeom)# колличество эллементов в элементарной ячейке
	

		for i in range(Natom):
			if len(crystalGeom[i].split()) == 5:
				NXYZocup = crystalGeom[i].split() # в файле геометрии бежим по строкам

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
			#_____________________________________________________________________________________________________________________________
			# #__считаем f0_raspredelenie  для определения зависимости от sin(teta)/lam_____________________________________________________
			# sin_by_lam = 0
			# X_f0_raspredelenie = []
			# Y_f0_raspredelenie = []
			# with  open(path+'saved/f0_'+element_name.replace('\n', '')+'.dat', 'w') as out1:
		# 		while sin_by_lam<=2*math.pi:
		# 			f0_raspredelenie=0# обнуляем коэффициен для следующего атома в ячейке для построения зависимоти 
		# 			for k in range(0, 4):
		# 				f0_raspredelenie += float(abc[k])*math.exp(-float(abc[k+5])*(math.sin(sin_by_lam)/wavelength)**2)# длинна волны в ангстремах
		# 			f0_raspredelenie=(f0_raspredelenie+float(abc[4]))
		# 			X_f0_raspredelenie.append(sin_by_lam)
		# 			Y_f0_raspredelenie.append(f0_raspredelenie)
		# 			out1.write('%14.8s'  % str(sin_by_lam))
		# 			out1.write('%14.8s' % str(f0_raspredelenie))
		# 			out1.write('\n')

		# 			sin_by_lam+=math.pi/100

		# 	# a_element = PolarizabilityClass.plot_for_sin_by_lam(X_f0_raspredelenie,Y_f0_raspredelenie, element_name,a_element)
		# 	if not element_name in a_element: 
		# 		ax.plot(X_f0_raspredelenie, Y_f0_raspredelenie,label=element_name.replace('\n', '')+' (N = ' + NXYZocup[0]+')')
		# 		a_element.add(element_name)

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
		delta = math.degrees(C*abs(Xh)/(math.sin(2*tetaprmtr)))*3600

		# Смещение кривой
		bb=1
		sdvig = math.degrees(-X0.real*(1+bb)/(2*bb*math.sin(2*tetaprmtr)))*3600


		# bot_inform.sent_to_atknin_bot('wavelenght: ' + str(wavelength), 'v') # проинформируем в telegramm bot
		# bot_inform.sent_to_atknin_bot('crystal: id-' + crystal_id+' name: '+crystal.name, 'v') # проинформируем в telegramm bot
		# bot_inform.sent_to_atknin_bot('hkl: '+str(hInd)+str(kInd)+str(lInd), 'v') # проинформируем в telegramm bot
		# bot_inform.sent_to_atknin_bot('path: '+ path, 'v') # проинформируем в telegramm bot
		# bot_inform.sent_to_atknin_bot('Bragg: '+ str(round(math.degrees(tetaprmtr), 4)), 'v') # проинформируем в telegramm bot
		# bot_inform.sent_to_atknin_bot('N_atom: '+ str(Natom), 'v') # проинформируем в telegramm bot

# Собственная кривая кристалла -–––––––––––––––––––––––––––––––––––
		schet=0
		schet1=0
		epslist = []
		max_pow_R = 0
		x_whole = []
		for_downloading = ''
		for i in range(0,10000):
			dTeta = (i/100-50)*math.pi/180/3600

			alfa = -4*math.sin(tetaprmtr)*(math.sin(tetaprmtr+dTeta)-math.sin(tetaprmtr)) # угловая отстройка падающего излучения от угла Брегга
			prover = (1/4)*(X0*(b+1)-b*alfa+cmath.sqrt(((X0*(b-1)-b*alfa)*(X0*(b-1)-b*alfa))+4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
			if prover.imag < 0:
				eps = (1/4)*(X0*(b+1)-b*alfa-cmath.sqrt(((X0*(b-1)-b*alfa)*(X0*(b-1)-b*alfa))+4*b*(C*C)*((Xh.real)*(Xh.real)-(Xh.imag)*(Xh.imag)-2j*Xh.real*Xh.imag)))
			else:
				eps = prover
			
			R=(2*eps-X0)/Xh/C
			epslist.append(abs(R)*abs(R))
			for_downloading+= str(i/100-50)+'   '+str(abs(R)*abs(R)) + '\n'

			if (abs(R)*abs(R)) > 0.05 and schet==0: schet = i 
			if (abs(R)*abs(R)) < 0.05 and schet > 0 and schet1 == 0: schet1 = i
			if max_pow_R<(abs(R)*abs(R)):
				max_pow_R = (abs(R)*abs(R))

		otstup = 10 # для того чтобы обрезать диапазон вывода графика
		y = epslist[schet-otstup:schet1+otstup:1]	
		x = np.linspace((schet-otstup)/100-50,(schet1+otstup)/100-50,len(y)).tolist()
		
		message['status'] = "ok"
		message['bragg'] = str(round(math.degrees(tetaprmtr), 4))
		message['X0_real'] = str(round(X0.real*math.pow(10,7),4))
		message['X0_imag'] = str(round(X0.imag*math.pow(10,7),4))
		message['Xh_real'] = str(round(Xh.real*math.pow(10,7),4))
		message['Xh_imag'] = str(round(Xh.imag*math.pow(10,7),4))
		message['delta'] = str(round(delta,4))
		message['dprmtr'] = str(round(dprmtr, 4))
		message['extintion'] = str(round(Ld*1e-4, 3)) # микроны
		message['maximum'] = str(round(max_pow_R,4))
		message['x_darwin'] = x
		message['y_darwin'] = y
		message['for_downloading'] = for_downloading
		message['fi'] = round(fi,1) # угол между плоскостью и поверхностью

		

	else:
		message['status'] = "error"
	return JsonResponse(message)

	

def polarizability(request):
	args = {}
	args['crystals'] = polarizability_models.crystals.objects.all()
	args['lab_source'] = diffraction_models.wavelength.objects.all()

	return render(
	 	request, 'polarizability/polarizability.html', args
	 	)