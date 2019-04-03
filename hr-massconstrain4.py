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
import math
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
radial_first = 8.9606


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
               m_solar = 1.9892 * 10 ** (33)
               r_solar = 6.9598 * 10 ** (10)
               R = r*r_solar
               M = m*m_solar
               G = 6.67428 * 10 ** (-8)
               
               g = G*M/R**2
               logg = np.log10(g)
               logteff = np.log10(teff)
               
               profile_numbers.append(pnums)
               loggs.append(logg)
               logteffs.append(logteff)
               alle = [g, teff, pnums]
               alle_final.append(alle)
              
# %%

plt.plot(logteffs,loggs,'r-')

plt.plot([Log_Teff_lower, Log_Teff_upper, Log_Teff_upper, Log_Teff_lower, Log_Teff_lower], [Log_g_lower, Log_g_lower, Log_g_upper, Log_g_upper, Log_g_lower], 'r-.', alpha=0.5, linewidth=3)

alle = []
differences_radial = []
differences_first = []
minValueRadial = None
minValueFirst = None
diffsndirs_radial = []
diffsndirs_first = []
    
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
                        
                        currentValueRadial = difference_funda
                
                        if minValueRadial == None:
                            minValueRadial = currentValueRadial
                        else:
                            minValueRadial = min(minValueRadial, currentValueRadial)
                            
                        currentValueFirst = difference_first
                
                        if minValueFirst == None:
                            minValueFirst = currentValueFirst
                        else:
                            minValueFirst = min(minValueFirst, currentValueFirst)
                                
                        differences_radial.append(difference_funda)
                        differences_first.append(difference_first)
                        temp_radial = [gyredirs, difference_funda]
                        temp_first = [gyredirs, difference_first]
                        diffsndirs_radial.append(temp_radial)
                        diffsndirs_first.append(temp_first)

minimum_radial = differences_radial.index(minValueRadial)
minimum_profile_radial = diffsndirs_radial[minimum_radial]
minimum_first = differences_first.index(minValueFirst)
minimum_profile_first = diffsndirs_first[minimum_first] 
 

best_g_radial = alle_final[minimum_radial][0]
best_teff_radial = alle_final[minimum_radial][1]
best_g_first = alle_final[minimum_first][0]
best_teff_first = alle_final[minimum_first][1]

plt.plot(np.log10(best_teff_radial),np.log10(best_g_radial),'k.', MarkerSize = 15)   
plt.plot(np.log10(best_teff_first),np.log10(best_g_first),'r.', MarkerSize = 5)  

xlabel(r'$\logT_{eff}$')
ylabel(r'$\log(g)$')
legend()
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.rcParams.update({'font.size': 20})                    
#%% 
                
           