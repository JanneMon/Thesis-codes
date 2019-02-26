#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 20:54:10 2019

@author: janne
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 13:47:05 2019

@author: janne
"""

import gyre_output_read as gar
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
import numpy as np
import re
from natsort import natsorted, ns
plt.close("all")

dire = '/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1'
l = mr.MesaLogDir('/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1')
time_age = []
fund_freqs = []
#modelno = []
profilno = []
gyreno = []

for root, dirs, files in sorted(os.walk(dire)):    
    #files.sort(key=lambda x: '{0:0>20}'.format(x))
    #natsorted(files, key=lambda y: y.lower())
    for file in files:
        print(file)
        if file.endswith('.data'):
            
            pnum = re.search('profile(.+?).data', file)
            gnum = re.search('profile(.+?)-freqs.dat', file)
            
            print(root,file)
            if gnum: 
                gnums = gnum.group(1)
            elif pnum:
                pnums = pnum.group(1)
                
            profilno += [pnums]
            gyreno += [gnums]
            








"""
for root, dirs, files in sorted(os.walk(dire)):    
    files.sort(key=lambda x: '{0:0>20}'.format(x))
    #natsorted(files, key=lambda y: y.lower())
    for file in files:
            if file.endswith('freqs.dat'): #and os.path.exists(file)==True:
                        
                dires = os.path.join(root,file)
                #print(dires)
                data = gar.readmesa(dires)
                re_freq_theo = data['Refreq']
                radial_order= data['n_pg']
                re_freq_fund = re_freq_theo[1]
                #print(re_freq_fund)
                
                m = re.search('profile(.+?)-freqs.dat', file)
          
                if m:
                    modelnos = m.group(1)
                    #print(modelnos)
                    
                    modelno += [modelnos]
                fund_freqs += [re_freq_fund]   #plt.plot(modelnos, re_freq_fund, '*', linestyle='None')
                
                for i in range(1,len(modelno)):
                    print(i)
                    pdirs = os.path.join(root,file)
                    p = l.profile_data(profile_number=modelno[i])
                    
                time = p.star_age
                
                time_age += [time]
                
  #fund_freqs += [re_freq_fund]
                
#time_filtered = time[modelno]             
#plt.plot(time_age, fund_freqs, '*', linestyle='None')
                
#plt.xlabel('profile/model')
#plt.ylabel('Fundamental frequency')"""