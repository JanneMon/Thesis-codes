#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:13:24 2019

@author: janne
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 14:42:06 2019

@author: janne
"""

import gyre_output_read as gar
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_pdf import PdfPages
#import seaborn as sns
#from pylab import *
import os, sys
import re
plt.close("all")


def chis(fname, profname):
    finalarray = []
    bm_array2 = []
    models = 'profile{}-freqs.dat'.format(profname)
 
    for root, dirs, files in sorted(os.walk(fname)):
        for file in files:
            if not file.startswith(models): #and os.path.exists(file)==True:
                continue 
            
            names = []
            dires = os.path.join(root,file)
            
            data = gar.readmesa(dires)
         
            harm_degree = data['l']
            radial_order= data['n_pg']
            re_freq_theo = data['Refreq'] # these are the frequencies that will be compared to Lenz and observations. 
            #im_freq = data['Imfreq'] #imaginary part of frequencies are not observable. 
            #print(re_freq_theo)
    
            re_freq_obs = [6.8980, 8.9607, 11.20, 13.48]
            re_freq_obs_unc     = [2.762223525*10**(-7), 8.454940424*10**(-7),  1*10**(-7), 1*10**(-7)]
            #print(len(np.atleast_1d(re_freq_theo)))
            #re_freq_obs_unc = np.ones(len(re_freq_obs)) * 0.1
            remaining_obs = re_freq_obs 
            #remaining_obs_unc = freq_obs_uncertainties
            remaining_theo = np.atleast_1d(re_freq_theo)
            remaining_ells = np.atleast_1d(harm_degree)
            remaining_radial = np.atleast_1d(radial_order)
    
            best_matching = []
            #names = []
    
            for ii in range(min(len(np.atleast_1d(re_freq_theo)), len(re_freq_obs))): #default: freq_obs, but depends if freq_obs is longer than re_freq
                best = np.inf
                bestjj = -1
                bestkk = -1
        
                #print(len(remaining_obs))
        
                for jj in range(len(np.atleast_1d(remaining_theo))):
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
        
            bm_array = np.asarray(best_matching)
                    
            bm_array2 += [bm_array]
            finalarray += [[bm_array, file]]
            
    #print(finalarray)
    #print(bm_array2)
    
    temp = []
    
    for i in range(len(bm_array2)):    
        if len(bm_array2[i]) >= 2:
            
            #farr += finalarray.pop(i)
            temp.append(finalarray[i])
        #else:
            #print(finalarray[i][1])
    
    finalarray = temp
    
    chi2 = np.zeros(len(finalarray))
    modelnos = np.zeros(len(finalarray))
    #print(len(finalarray))
    #number = []
    for i, (array, modelno) in enumerate(finalarray):
        array = np.asarray(array)
        if len(array) == 4:
            
            m = re.search('profile(.+?)-freqs.dat', modelno)
          
            if m:
                modelnos[i] = m.group(1)
                #print(modelnos)
                 
            delta = array[:, 2] - array[:, 3]
            chi2[i] = np.sum((delta ** 2) / (np.asarray(re_freq_obs_unc) ** 2))
            
            chi2[i] /= len(delta)
            #test_result.append(modelnos + chi2)
            
            test_result = np.zeros((len(chi2),2))
            #rint(test_result)
            for i in range(0,len(modelnos)):
                test_result[i][0] = modelnos[i]
                test_result[i][1] = chi2[i]
                
    print(modelnos)
    print(chi2)
    
    

    #print(test_result)
    #print(results)
    return test_result, finalarray
#c = '/home/janne/Gunter_project/44_tau/example_zs/LOGS-2.0-0.022-0.29-1.5'
#a = '/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/'
#b = '/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1'
#
#results = chis(b, '14')