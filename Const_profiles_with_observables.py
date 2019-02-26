#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:18:04 2019

@author: janne

Thius code is meant to put constraints on the standard mesa input files to recognize which profiles 
lies within a three sigma uncertainty of the observed parameters. 
"""


#Observed parameters are from Lenz et al.: Study of the delta Scuti Star 44 tau
Log_Teff_obs = 3.839
Log_L_obs = 1.340
Log_g_obs = 3.6


Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.0065 
Log_g_obs_unc = 0.1

#Three sigma intervals
Log_Teff_3s = 3*Log_Teff_obs_unc
Log_L_3s = 3*Log_L_obs_unc
Log_g_3s = 3*Log_g_obs_unc


dire = mr.MesaLogDir('/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1')

histnos = []
modelno = []
for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1')):
    for file in files:
        if file.startswith('profile') and file.endswith('.data'): #and os.path.exists(file)==True:
                #print(root,file)

            m = re.search('profile(.+?).data', file)
          
            if m:
                modelnos = m.group(1)
                    #print(modelnos)
                
            modelno += [modelnos]

        if file.startswith('history'):
            dirs = os.path.join(root,file)
            #print(natsort.natsorted(dirs,reverse=True))
            
            h = mr.MesaData(dirs)
            Log_Teff_theo = h.log_Teff
            Log_L_theo = h.log_L
            log_g_theo = h.log_g
            
            histno = h.model_number
        
            histnos += [histno]    
            
                
            
for i in range(0,len(modelno)):             #   for i in range(1,len(modelno)):
    
    p = dire.profile_data(profile_number=modelno[i])                
    profno = p.model_number
    
    # And now for actually sorting the profiles: 
    print(i)
    if histnos[0][i] == profno:
        print('something please')
     
