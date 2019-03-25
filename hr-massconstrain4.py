#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 22:06:38 2019

@author: janne
"""
from pylab import *
import numpy as np
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
import gyre_output_read as gyr
plt.close("all")



Log_Teff_obs = 3.839
Log_g_obs = 3.6

Log_Teff_obs_unc = 0.007
#Log_L_obs_unc = 0.0065 
Log_g_obs_unc = 0.1

n = 3

Log_Teff_ns = n*Log_Teff_obs_unc
#Log_L_ns = n*Log_L_obs_unc
Log_g_ns = n*Log_g_obs_unc

Log_Teff_lower = Log_Teff_obs - Log_Teff_ns
Log_Teff_upper = Log_Teff_obs + Log_Teff_ns
#Log_L_lower = Log_L_obs - Log_L_ns
#Log_L_upper = Log_L_obs + Log_L_ns
Log_g_upper = Log_g_obs + Log_g_ns
Log_g_lower = Log_g_obs - Log_g_ns

radial_funda = 6.8980

#radial_first = 8.9606


loggs = []
logteffs = []
profile_numbers = []
alle_final = []

for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')):
    files.sort(key=lambda x: '{0:0>20}'.format(x))
    for file in files:
           
        if file.startswith('profile') and file.endswith('.data'):
           profiledirs = os.path.join(root,file)
           profileroots = os.path.join(root)
           
           constraint_noprems = 500
           
           pnum = re.search('profile(.+?).data', profiledirs)
            
           if pnum: 
               pnums = pnum.group(1)
           if int(pnums) >= int(constraint_noprems): 
               #print(pnums)
               
               profiles_indir = mr.MesaLogDir('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')
               pr = profiles_indir.profile_data(profile_number=pnums)
               pr_modelnos = pr.model_number
               
               teff = pr.Teff
               #logteff = np.log(teff)
               r = pr.photosphere_r
               m = pr.initial_mass
               g = m/r**2
               #logg = np.log(g) 
               
               profile_numbers.append(pnums)
               loggs.append(g)
               logteffs.append(teff)
               alle = [g, teff, pnums]
               alle_final.append(alle)
              
# %%

plt.plot(np.log10(logteffs),np.log10(loggs),'r-')
xlabel(r'$\logT_{eff}$')
ylabel(r'$\log(g)$')
legend()
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.rcParams.update({'font.size': 20})
#plt.plot([Log_Teff_lower, Log_Teff_upper, Log_Teff_upper, Log_Teff_lower, Log_Teff_lower], [Log_g_lower, Log_g_lower, Log_g_upper, Log_g_upper, Log_g_lower], 'r-.', alpha=0.5, linewidth=3)

alle = []
differences = []
minValue = None
diffsndirs = []
    
for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')):
    files.sort(key=lambda x: '{0:0>20}'.format(x))
    for file in files:
           
        if file.endswith('freqs.dat'):
                
                gyredirs = os.path.join(root,file)
                gyreroots = os.path.join(root)
                gnum = re.search('profile(.+?)-freqs.dat', gyredirs)
            
                if gnum: 
                    gnums = gnum.group(1)
                if int(gnums) >= int(constraint_noprems):
                    #print(gnums)
                    freqs = gyr.readmesa(gyredirs)
                    
                    if freqs[0][1] == 1 and freqs[1][1] == 2: 
                        difference_funda = np.abs(freqs[0][4] - radial_funda)
                        difference_first = np.abs(freqs[1][4] - radial_first)    
                        #differences.append()
                        
                        currentValue = difference_funda
                
                        if minValue == None:
                            minValue = currentValue
                        else:
                            minValue = min(minValue, currentValue)
                                
                        differences.append(difference_funda)
                        temp2 = [gyredirs, difference_funda]
                        diffsndirs.append(temp2)

minimum = differences.index(minValue)
minimum_profile = diffsndirs[minimum] 

best_g = alle_final[minimum][0]
best_teff = alle_final[minimum][1]

plt.plot(np.log10(best_teff),np.log10(best_g),'k.', MarkerSize = 15)                       
#%% 
                
           