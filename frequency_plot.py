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

dire = '/home/janne/Gunter_project/44_tau/example_3ms/LOGS-3'
l = mr.MesaLogDir('/home/janne/Gunter_project/44_tau/example_3ms/LOGS-3')
time_age = []
fund_freqs = []
modelno = []
for root, dirs, files in sorted(os.walk(dire)):    
    files.sort(key=lambda x: '{0:0>20}'.format(x))
    #natsorted(files, key=lambda y: y.lower())
    for file in files:
            if file.endswith('freqs.dat'): #and os.path.exists(file)==True:
                        
                dires = os.path.join(root,file)
                #print(dires)
                #print(dires)
                data = gar.readmesa(dires)
                re_freq_theo = data['Refreq']
                
                
                radial_order= data['n_pg']
                
                if radial_order[0] == 1:
                    
                    re_freq_fund = re_freq_theo[1]
                    
                #print(re_freq_fund)
                
                
                
                    m = re.search('profile(.+?)-freqs.dat', file)
          
                    if m:
                        modelnos = m.group(1)
                        #print(modelno)
                    #print(modelnos)
                    
                    modelno += [modelnos]
                    fund_freqs += [re_freq_fund]   #plt.plot(modelnos, re_freq_fund, '*', linestyle='None')

            #elif file.endswith('.data') and not file.startswith('history'):  

for i in range(0,len(modelno)):             #   for i in range(1,len(modelno)):
    print(i)
    pdirs = os.path.join(root,file)
    p = l.profile_data(profile_number=modelno[i])
                    
    time = p.star_age
                
    time_age += [time]
    #time_age = time_age/10**9
#time_array = np.asarray(time_age)
#fundfreqs_array = np.asarray(fund_freqs)          
#filt = time_array > 0.5*10**9
#time_age_filtered = time_array[filt]
#fund_freq_filtered = fundfreqs_array[filt]
#time_filtered = time[modelno]             
plt.plot(time_age, fund_freqs, '*', linestyle='None')
plt.plot(time_age, fund_freqs, 'rp', markersize=14)
plt.rcParams.update({'font.size': 20})
plt.xlabel('Star age [yr]')
plt.ylabel('Fundamental frequency [Cyc/Day]')
            
            
            
