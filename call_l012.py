#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:30:32 2019

@author: janne

Call for all rsults
"""
import os
import matplotlib.pyplot as plt
import make_table_initparamsonly as init
import make_table_obsparams_l012 as obs
import getl1l2_second_version as l1l2
import finalchi_l012 as fin
#import calculate_chis_ff1 as chi
import numpy as np
plt.close('all')


allinfo = []

list_of_masses = []
list_of_zs = []
list_of_ys = []
list_of_mlts = []


def firstpart():
    list_of_names_l012 = []
    list_of_minimums_l012 = []
    for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_postms_3ms/')):#output_test_mlt_freqs/output_test_mlt/')):
        dirs.sort(key=lambda x: '{0:0>20}'.format(x))    
        for dire in dirs:

            directories = os.path.join(root,dire)
            #print(directories)
            output_filename = directories.strip(root)
            names = 'final_l0123_'+ output_filename + '.txt'
            print(names)
            
            init.getmodelparams(directories)
            obs.getobsparams(directories)
            kolonne = l1l2.to_get_chi2(directories)
            total_chi, minimum = fin.getchis(names)
            
            list_of_names_l012 += [names]
            list_of_minimums_l012 += [minimum]
            #print(list_of_names)
    return list_of_names_l012, list_of_minimums_l012

#list_of_names_l012, list_of_minimums_l012 = firstpart()
liste = []

for j in list_of_names_l012:
    allinfo = []
    with open(j) as f:
        for line in f:
            inner = [elt.strip() for elt in line.split(',')]
            allinfo.append(inner)
            every = np.asarray(allinfo)
        liste.append(every)
        f.close()
        
    #for k in range(len(liste)):
        mass = every[0][0]
        z    = every[0][1]
        y    = every[0][2]
        mlt  = every[0][3]
    
        list_of_masses += [mass]
        list_of_zs     += [z]
        list_of_ys     += [y]
        list_of_mlts   += [mlt]

minima = np.asarray(list_of_minimums_l012)
chi2 = minima[:,0]
redchi = minima[:,1]

plt.xlabel(r'Mass $[M_{\odot}]$')
#xlabel(r'Z $[]$')
plt.ylabel(r'$\chi^{2}$')
plt.rcParams.update({'font.size': 20})
plt.plot(list_of_masses, chi2,'.', MarkerSize = 15)
#plt.plot(list_of_zs, chi2,'.', MarkerSize = 15)

#def plotmass(input_name):

