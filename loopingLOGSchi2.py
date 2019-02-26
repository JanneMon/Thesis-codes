#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 19:08:40 2019

@author: janne
"""

import chi2_allLOGS as chall
import os

a = '/home/janne/Gunter_project/gunther_project/LOGS_44_tau_testrun/'
b = '/home/janne/Gunter_project/44_tau/example_zs/LOGS-2.0-0.020-0.29-1.5'


#results = chis(b)

results_final = []

for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_zs/')):
        for dire in dirs:
            dires = os.path.join(root,dire)
            #print(dires)
            results = chall.chis(dires)
            #print(results)
            
results_final += [results]
#print('Results:=')
#print(results_final)