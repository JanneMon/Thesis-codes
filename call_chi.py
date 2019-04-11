#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:30:32 2019

@author: janne

Call for all rsults
"""
import os
import matplotlib.pyplot as plt
import make_table_initparams as init
import make_table_fundfirst as fund
import calculate_chis_ff1 as chi
import numpy as np
plt.close('all')


allinfo = []
list_of_masses = []
list_of_zs = []
list_of_ys = []
list_of_mlts = []

def firstpart():
    list_of_names = []
    list_of_minimums = []
    runonce = 0
    for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_postms_3ms/')):#output_test_mlt_freqs/output_test_mlt/')):
        dirs.sort(key=lambda x: '{0:0>20}'.format(x))    
        for dire in dirs:
            if runonce > 0:
                break
            
                #plt.figure(dire)
            directories = os.path.join(root,dire)
    
            fund.getfundfreqs(directories)
            init.getinitparams(directories)
            #print(directories)
            name = directories.strip(root)
            names = 'final_'+ name + '.txt'
            total_chi, minimum = chi.getchis(names)
            list_of_names += [names]
            list_of_minimums += [minimum]
            runonce +=1
            #print(list_of_names)
    return total_chi, list_of_minimums, list_of_names
        
#total_chi, list_of_minimums, list_of_names = firstpart()
liste = []
for j in list_of_names:
    allinfo = []
    with open(j) as f:
        for line in f:
            inner = [elt.strip() for elt in line.split(',')]
            allinfo.append(inner)
            every = np.asarray(allinfo)
        liste.append(every)
        f.close()
        
        mass = allinfo[0][2]
        z    = allinfo[0][3]
        y    = allinfo[0][4]
        mlt  = allinfo[0][5]
        
        list_of_masses += [mass]
        list_of_zs     += [z]
        list_of_ys     += [y]
        list_of_mlts   += [mlt]

minima = np.asarray(list_of_minimums)
chi2 = minima[:,0]
redchi = minima[:,1]

plt.xlabel(r'Mass $[M_{\odot}]$')
plt.ylabel(r'$\chi^{2}$')
plt.rcParams.update({'font.size': 20})
plt.plot(list_of_masses, chi2,'.', MarkerSize = 15)
#plt.plot(list_of_zs, chi2,'.', MarkerSize = 15)

#def plotmass(input_name):
    