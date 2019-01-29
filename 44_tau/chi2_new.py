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


#list_number = [s for s in os.listdir('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/') if s.endswith('.dat')]
#for filename in os.listdir('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/'):
#    if filename.endswith(".dat"):
#        data = gar.readmesa(filename)

list_number = [os.path.join('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/', file) for file in os.listdir('/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/') if file.endswith('.dat')]
finalarray = []

for file in range(len(list_number)):
    if file == 4 or file == 6:
        continue 
    
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

    remaining_obs = re_freq_obs 
    #remaining_obs_unc = freq_obs_uncertainties
    remaining_theo = re_freq_theo
    remaining_ells = harm_degree
    remaining_radial = radial_order
    
    best_matching = []
    

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
        best_matching += [[remaining_ells[bestjj], remaining_radial[bestjj], 
                           remaining_theo[bestjj], remaining_obs[bestkk]]]
        
        remaining_theo = np.delete(remaining_theo, bestjj)
        remaining_ells = np.delete(remaining_ells, bestjj)
        remaining_obs = np.delete(remaining_obs, bestkk)
        #remaining_obs_unc = np.delete(remaining_obs_unc, bestkk)
        remaining_radial = np.delete(remaining_radial,bestjj)
        
        #diff = np.asarray(diff)
        #final = np.append(bm_array,diff)
    
    bm_array = np.asarray(best_matching)
    
    
    finalarray += [bm_array]
    
farr = []   
for i in range(len(finalarray)):    
    if len(finalarray[i]) < 4:
        farr = np.delete(finalarray,finalarray[i])
    #else: 
    #    farr += finalarray[i]
        
finalarray2 = np.concatenate(farr, axis=0)
    #diff = np.abs(bm_array[:,2]-bm_array[:,3])

x2 = []
step = 4
#for j in range(len(finalarray)):
for i in range(0,len(finalarray2),4):
    #step == 4
    #if i % step == 0:
    x2 += [[sum(np.abs(finalarray2[i,2]-finalarray2[i,3])**2/4)]]
    #else:
     #  i + 4
       
x2 += [x2]


#sample = "This is a string"
#n = 3 # I want to iterate over every third element
#for i,x in enumerate(sample):
#    if i % n == 0:
 #       print("do something with x "+x)
 #   else:
#        print("do something else with x "+x)
#k = number of observed osc. modes
#chi2 = 1/k*sum(vi_obs-vi_theo)2