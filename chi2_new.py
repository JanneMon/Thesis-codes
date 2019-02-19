#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 14:42:06 2019

@author: janne
"""

import gyre_output_read as gar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from pylab import *
import os, sys
plt.close("all")

#list_number = [s for s in os.listdir('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/') if s.endswith('.dat')]
#for filename in os.listdir('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/'):
#    if filename.endswith(".dat"):
#        data = gar.readmesa(filename)

list_number = [os.path.join('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/', file) for file in os.listdir('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/') if file.endswith('.dat')]
finalarray = []
names = []
bm_array2 = []
for file in range(len(list_number)):
    if file == 4 or file == 6:
        continue 
    
    #if os.path.exists(file)==False:
    #    continue
    #print(file)
    
    data = gar.readmesa(list_number[file])

    harm_degree = data['l']
    radial_order= data['n_pg']
    #acou_num = data['n_p']
    #grav_num = data['n_g']
    #re_omega = data['Re(omega)']
    #im_omega = data['Im(omega)']
    #re_omega_int = data['Re(omega_int)']
    #m_omega_int = data['Im(omega_int)']
    re_freq_theo = data['Refreq'] # these are the frequencies that will be compared to Lenz and observations. 
    #im_freq = data['Imfreq'] #imaginary part of frequencies are not observable. 

    #print(re_freq_theo)

    re_freq_obs = [6.8980, 8.9607, 11.20, 13.48]
    re_freq_obs_unc     = [2.762223525*10**(-7), 8.454940424*10**(-7),  1*10**(-7), 1*10**(-7)]
    #re_freq_obs_unc = np.ones(len(re_freq_obs)) * 0.1
    remaining_obs = re_freq_obs 
    #remaining_obs_unc = freq_obs_uncertainties
    remaining_theo = re_freq_theo
    remaining_ells = harm_degree
    remaining_radial = radial_order
    
    best_matching = []
    #names = []

    for ii in range(min(len(re_freq_theo), len(re_freq_obs))): #default: freq_obs, but depends if freq_obs is longer than re_freq
        best = np.inf
        bestjj = -1
        bestkk = -1
    
        #print(len(remaining_obs))
    
        for jj in range(len(remaining_theo)):
            for kk in range(len(remaining_obs)):
                val = (remaining_theo[jj] - remaining_obs[kk])**2 / 4 #put uncertainty here  
                if (val < best):
                    best = val
                    bestjj = jj
                    bestkk = kk
        
        # print(best, bestjj, bestkk)
        best_matching += [[remaining_ells[bestjj], remaining_radial[bestjj], remaining_theo[bestjj], remaining_obs[bestkk]]]
        
        remaining_theo = np.delete(remaining_theo, bestjj)
        remaining_ells = np.delete(remaining_ells, bestjj)
        remaining_obs = np.delete(remaining_obs, bestkk)
        #remaining_obs_unc = np.delete(remaining_obs_unc, bestkk)
        remaining_radial = np.delete(remaining_radial,bestjj)
        
        #diff = np.asarray(diff)
        #final = np.append(bm_array,diff)
    
    bm_array = np.asarray(best_matching)
    
    bm_array2 += [bm_array]
    finalarray += [[bm_array, file]]
    
    #names += [bm_array, file]

#farr2 = []
farr = [] 
finalarray2 = []
#np.concatenate(names[:],axis=0)

for i in range(len(bm_array2)):    
    if len(bm_array2[i]) < 4:
        farr += finalarray.pop(i)
  
    #finalarray2 += farr
#farr2 += [farr]
    
#finalarray2 = np.concatenate(finalarray, axis=0)

#names += [finalarray2, file]

#x2 = []

#for i in range(0,len(finalarray),4):
#    x2 += [[sum(np.abs(finalarray[i,2]-finalarray[i,3])**2/4)]]
       
#x2 += [x2]


#sample = "This is a string"
#n = 3 # I want to iterate over every third element
#for i,x in enumerate(sample):
#    if i % n == 0:
 #       print("do something with x "+x)
 #   else:
#        print("do something else with x "+x)
#k = number of observed osc. modes
#chi2 = 1/k*sum(vi_obs-vi_theo)2
 
#print(finalarray)
chi2 = np.empty(len(finalarray))
modelnos = np.empty(len(finalarray))
for i, (array, modelno) in enumerate(finalarray):
    array = np.asarray(array)
    if len(array) == 4:
        #print('i', i)
        #print('modelno', modelno)
        #print('array', array)
        #print(array[:, 2])
        delta = array[:, 2] - array[:, 3]
        #print('delta', delta)
        #print('uncertainties', re_freq_obs_unc)
        chi2[i] = np.sum((delta ** 2) / (np.asarray(re_freq_obs_unc) ** 2))
        chi2[i] /= len(delta)
        print('chi2', chi2[i])
        modelnos[i] = modelno
    #for i in range(len(array)):
    #    print('single model', array[i])
    
print('every chi2', chi2)
plt.figure()
plt.plot(modelnos, log(chi2), '*', linestyle='None')
plt.xlabel('profile/model')
plt.ylabel('log(chi2)')

    