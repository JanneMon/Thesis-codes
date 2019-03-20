#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:11:16 2019

@author: janne

"""


import chi2_allLOGS as chall
import only_some_chis as chsome
#import Const_profiles_allLOGS as constp
import Cons_profiles_2 as cp2
import numpy as np
import os

a = '/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/'
b = '/home/janne/Gunter_project/44_tau/example_zs/LOGS-2.0-0.020-0.29-1.5'


#results = chis(b)


results_profiles = []
#result = []
directory = []

"""
First call the routine that calculates relevant profiles based on observational constraints Teff, logL and 
log g. 
"""
for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_3ms')):
        for dire in dirs:
            dires = os.path.join(root,dire)
            print(dires)
            profiles = cp2.useful_profiles(dires)
            if len(profiles) == 0:
                print("no profiles found for this directory")
            elif len(profiles) != 0:
            #directory += [dires]
                print("Successfull")
                dires = [dires]
                results_profiles.append(profiles + dires)
            
results_profiles  
final_profiles = np.array(results_profiles) 



"""
Second call takes the profiles calculated from above and calls a routine to calculate the chi2 for them. 
The output is an array with profile number, chi2, and LOGS directory. 
"""

#new = []
dirs_chi = []
results_chi = []
results_finalarray = []

for i in range(0,len(final_profiles)):
    dires = final_profiles[i][-1]
    models = final_profiles[i][:-1]
    for j in models:
        results, finalarray = chsome.chis(dires, j)
        results_finalarray.append(finalarray)
        results_chi.append(results)
        dirs_chi.append(dires)
        #new += [results_chi, dirs_chi]
        
newchi = np.concatenate(results_chi)
newdirs = np.array(dirs_chi)

test_result = np.zeros((len(results_chi),3), dtype=object)
            #rint(test_result)
for i in range(0,len(newchi)):
    test_result[i][:-1] = newchi[i]
    test_result[i][-1] = newdirs[i]

#final_chis = np.concatenate(np.array(results_chi))
#plt.figure()
#plt.plot(modelnos, np.log(chi2), '*', linestyle='None')
#plt.xlabel('profile/model')
#plt.ylabel('log(chi2)')
    
"""
This follpowing call calculates chi2s for ALL profiles in a directory. 

for i in range(0,len(final_profiles)):
    dires = final_profiles[i][-1]
    results = chall.chis(dires)
    results_chi.append(results)

final_chis = np.concatenate(np.array(results_chi))


"""
