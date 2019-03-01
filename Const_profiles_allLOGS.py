#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 17:02:11 2019

@author: janne
"""


import Cons_profiles_2 as cp2
import os

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
            #print(results)
#final
#results_final += [results]