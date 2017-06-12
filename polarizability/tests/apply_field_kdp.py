
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests
import time
import sys, os
import sys, os
sys.path.append('/home/atknin/env/xrays')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
from django.test import Client

data = {}
data['d11'], data['d12'], data['d13'], data['d14'], data['d15'], data['d16'] =  0,0,0,1.5,0,0
data['d21'], data['d22'], data['d23'], data['d24'], data['d25'], data['d26'] =  0,0,0,0,0,0
data['d31'], data['d32'], data['d33'], data['d34'], data['d35'], data['d36'] =  0,0,0,0,0,0

data['wavelength'] = 0.709300
data['assym_alfa_then_beta'] = 1
data['crystal_id'] =  16
data['field_direction'] = 1
data['fi_prmtr'] = 0
data['sample_width'] = 0.5
data['external_field'] = 'yes'

data['h_surface'] = data['h'] = 2
data['k_surface'] = data['k'] = 2
data['l_surface'] = data['l'] = 0

def cli_progress_test(end_val, bar_length=20):
	percent = end_val
	hashes = '#' * int(round(percent * bar_length)/100)
	spaces = ' ' * (bar_length - len(hashes))
	sys.stdout.write("\rPercent: [{0}] {1}%".format(
			hashes + spaces, int(round(percent))))
	sys.stdout.flush()

def my_request(data):

	c = Client()
	r = c.post('/polarizability/api/', data)
	status = r.status_code
	js = r.json()
	real_struct = complex(js['StructFactorReal'])
	imag_struct = complex(js['StructFactorImag'])
	squared = real_struct.real**2 + imag_struct.imag**2
	if status == 200:
		return squared
	else:
		print('status: ',status)
		my_request(data)

# print(my_request(data))
# r = requests.post('http://xrayd.ru/polarizability/api/', data = data).json()
# try:
#     del r['y_darwin']
# except Exception as e:
#     print('can"t del y_darwin')
# try:
#     del r['x_darwin']
# except Exception as e:
#     print('can"t del x_darwin')
# try:
#     del r['for_downloading']
# except Exception as e:
#     print('can"t del for_downloading')
#
# print(squared)
v = 0
while v<=10000:
    f = open('data/{}'.format(v),'w')
    cli_progress_test(v/100)
    for h in range(9):
        cli_progress_test(h/9*100)
        for k in range(9):
            for l in range(9):
                if (h==0 and k==0 and l==0):
                    print('.',v)
                    # print(h,k,l)
                else:
                    # time.sleep(0.01)
                    data['h_surface'] = data['h'] = h
                    data['k_surface'] = data['k'] = k
                    data['l_surface'] = data['l'] = l
                    data['volt'] = v
                    txt = '{}   {}  {}  {:10.4f}\n'.format(h,k,l, my_request(data))
                    f.write(txt)
    v+=100
    f.close()
