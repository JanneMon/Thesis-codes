#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 19:08:40 2019

@author: janne
"""

import chi2_allLOGS as chall
#import Const_profiles_allLOGS as constp
import os
import numpy as np

a = '/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/'
b = '/home/janne/Gunter_project/44_tau/example_zs/LOGS-2.0-0.020-0.29-1.5'


#results = chis(b)

results_final = []

for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_postms_3ms/')):
        for dire in dirs:
            dires = os.path.join(root,dire)
            #print(dires)
            results = chall.chis(dires)
            results.append(results + dires)
            #print(results)
            
results
#print('Results:=')
#print(results_final)




#a = '/home/janne/Gunter_project/44_tau/example_3ms/LOGS-3'



#results = chis(b)

result = []
directory = []


for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_3ms')):
        for dire in dirs:
            dires = os.path.join(root,dire)
            #print(dires)
            profiles = cp2.useful_profiles(dires)
            #directory += [dires]
            dires = [dires]
            result.append(profiles + dires)
            
result  
final = np.array(result)