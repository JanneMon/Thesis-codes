#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 17:09:22 2019

@author: janne
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:18:04 2019

@author: janne

Thius code is meant to put constraints on the standard mesa input files to recognize which profiles 
lies within a three sigma uncertainty of the observed parameters. This codes assumes that 
hist interval and profile number is not the same. 

It returns the profiles that are relevant for calculating chi2 for for further constraints. 
Called in allresults_constrains. 
"""

import mesa_reader as mr
import os, re
import numpy as np
#Observed parameters are from Lenz et al.: Study of the delta Scuti Star 44 tau
Log_Teff_obs = 3.839
Log_L_obs = 1.340
Log_g_obs = 3.6


Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.0065 
Log_g_obs_unc = 0.1

n = 10
#Three sigma intervals
Log_Teff_ns = n*Log_Teff_obs_unc
Log_L_ns = n*Log_L_obs_unc
Log_g_ns = n*Log_g_obs_unc

Log_Teff_lower = Log_Teff_obs - Log_Teff_ns
Log_Teff_upper = Log_Teff_obs + Log_Teff_ns
Log_L_lower = Log_L_obs - Log_L_ns
Log_L_upper = Log_L_obs + Log_L_ns
Log_g_lower = Log_g_obs - Log_g_ns
Log_g_upper = Log_g_obs + Log_g_ns


def useful_profiles(dirname):
    histnos = []
    modelnos = []
    profnos = []
    filtered = []
    #filtered1 = []
    #filtered2 = []
    #filtered3 = []
    profarray = []


    dire = mr.MesaLogDir(dirname)
    for root, dirs, files in sorted(os.walk(dirname)):
        for file in files:
            if file.startswith('profile') and file.endswith('.data'): #and os.path.exists(file)==True:
                    #print(root,file)
    
                m = re.search('profile(.+?).data', file)
              
                if m:
                    modelno = m.group(1)
                        #print(modelnos)
                    
                modelnos += [modelno]
    
            if file.startswith('history'):
                dirs = os.path.join(root,file)
                #print(dirs)
                #print(natsort.natsorted(dirs,reverse=True))
                
                h = mr.MesaData(dirs)
                Log_Teff_theo = h.log_Teff
                Log_L_theo = h.log_L
                Log_g_theo = h.log_g
                
                #mask = Log_Teff_lower < Log_Teff_theo and Log_Teff_upper > Log_Teff_theo
                
                histno = h.model_number
                histnos += [histno]
                histnos = np.array(histnos)
                
                
                for i in range(0,len(Log_Teff_theo)):               
                    mask1 = Log_Teff_lower < Log_Teff_theo[i] and Log_Teff_upper > Log_Teff_theo[i] and Log_L_lower < Log_L_theo[i] and Log_L_upper > Log_L_theo[i] and Log_g_lower < Log_g_theo[i] and Log_g_upper > Log_g_theo[i]
                    filtered += [mask1]
                
                filtered = np.array(filtered)
                
                array = histnos[0]
                array_filtered = array[filtered] 
                
           #     for j in filtered:
           #         if j == True:
    profiles = []
    
    for i in modelnos: 
        #i = int(i)
    
        p = dire.profile_data(profile_number=i)                
        profno = p.model_number
                #print('Trues:')
        for number in array_filtered:
            #print(number)
            #for l in range(1,len(array_filtered)):
            if profno == number:
                print(i)
                
                #models = 'profile{}-freqs.data'.format(i)
                profiles.append(i)
                #print(models)
        #profnos += [profno]
    profiles  
    
    return profiles

#profiles = useful_profiles('/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1')
     
