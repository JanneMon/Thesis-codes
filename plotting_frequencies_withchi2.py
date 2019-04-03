#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 15:09:18 2019

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



radial_funda = 6.8980
radial_first = 8.9606
differences_radial = []
allmodels = []
everything = []


#test_results = []
#all_frequencies_array = []
def allfreqs(fname):
    alldata = []
    alle = []
    for root, dirs, files in sorted(os.walk(fname)):
        for file in files:
            if not file.endswith('freqs.dat'): #and os.path.exists(file)==True:
                continue 
            dires = os.path.join(root,file)
            #data = gar.readmesa(list_number[file])
            data = gar.readmesa(dires)
            #print(data)
            
            if data[0][1] == 1 and data[1][1] == 2:
                alle += [data, dires]
                #print(alldata)
                #dataset += []
        #print(file, len(dataset))
            alldata  += [alle]
    return alldata

def calculate_chis_l0(data_1, minValueRadial):
    #print('jhoeol')
    #print(data_1)
    for j in range(0,len(data_1)):
    
        delta1 = np.abs(data_1[j][0][4] - radial_funda)
        delta2 = np.abs(data_1[j][1][4] - radial_first)
        
        """directory = data_1[j][i][1]
        
        m = re.search('profile(.+?)-freqs.dat', directory)
  
        if m:
            modelnos = m.group(1)
            allmodels.append(modelnos)
                
        currentValueRadial = delta1
    
        if minValueRadial == None:
            minValueRadial = currentValueRadial
        else:
            minValueRadial = min(minValueRadial, currentValueRadial)

        differs = [delta1, j]
        differences_radial.append(differs)
        #both_frequencies = [dataset[i][0][0][4], dataset[i][0][1][4]]
        #mode_degree = np.ones(len(both_frequencies))
        
        #plt.plot(both_frequencies,mode_degree, 'y.')
        #delta = array[:, 2] - array[:, 3]
        #chi2 = np.sum((delta ** 2) / (np.asarray(re_freq_obs_unc) ** 2))

    minimum_radial = differences_radial.index(minValueRadial)
    #minimum_profile_radial = diffsndirs_radial[minimum_radial]
    print(minValueRadial)"""
    return 


def calculate_chis(data,dires):
    bm_array2 = []
    finalarray = []
    
    harm_degree = data['l']
    radial_order= data['n_pg']
    
    re_freq_theo = data['Refreq']

    re_freq_obs = [6.8980, 8.9607]
    re_freq_obs_unc = [2.762223525*10**(-7), 8.454940424*10**(-7)]
    
    remaining_obs = re_freq_obs 
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

        #diff = np.asarray(diff)
        #final = np.append(bm_array,diff)

    bm_array = np.asarray(best_matching)
            
    bm_array2 += [bm_array]
    finalarray += [[bm_array, dires]]
    #print(finalarray)
    
    return finalarray

#data = allfreqs('/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2')

datas = []
for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_postms_3ms/')):#output_test_mlt_freqs/output_test_mlt/')):
    dirs.sort(key=lambda x: '{0:0>20}'.format(x))    
    for dire in dirs:
            #plt.figure(dire)
            directories = os.path.join(root,dire)
            #print(dires)
            data_1 = allfreqs(directories)
            #print(len(data_1))
            #everything.append(data_1.copy()) 
            #print(len(data_1))
            calculate_chis_l0(data_1, None)
            
            #datas.append(allbest)
            #do_something = calculate_l0(data,dires)
            #best_initially = calculate_chis(data, dires)
           
            
            
