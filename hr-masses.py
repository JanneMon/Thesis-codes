#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:52:44 2019

@author: janne
"""

from pylab import *
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
plt.close("all")
import natsort

Log_Teff_obs = 3.839
Log_L_obs = 1.340

Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.0065 

n = 10
#Three sigma intervals
Log_Teff_ns = n*Log_Teff_obs_unc
Log_L_ns = n*Log_L_obs_unc

Log_Teff_lower = Log_Teff_obs - Log_Teff_ns
Log_Teff_upper = Log_Teff_obs + Log_Teff_ns
Log_L_lower = Log_L_obs - Log_L_ns
Log_L_upper = Log_L_obs + Log_L_ns

# output_test_mlt02 is a good example for overshoot


s=0.25

for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_3_masses_ov025')):
    for file in files:
        
        if file.startswith('history'):
            #s+= 0.05
            #print(os.path.join(root,file))
            dirs = os.path.join(root,file)
            #print(natsort.natsorted(dirs,reverse=True))
            
            h = mr.MesaData(dirs)
            mass = h.initial_mass
            index = h.star_age > 2.0e7 
            noms_Teff = h.log_Teff[index]
            noms_L = h.log_L[index]
            #plot(h.log_Teff, h.log_L)
            #plot(noms_Teff, noms_L, label='%s$M_{\odot}$' %mass)
            #plt.gca().invert_xaxis()
            
            if file.endswith('profile1.data'):
            
                pdirs = os.path.join(root)
                print(pdirs)
                l = mr.MesaLogDir(pdirs)
                p = l.profile_data()
                Z = p.initial_z
                #M = p.initial_mass
                
            plt.plot(Log_Teff_obs, Log_L_obs,'r*', MarkerSize=10)
            plt.rcParams.update({'font.size': 20})
            plt.plot(noms_Teff, noms_L, '-', MarkerSize=10, label='Mass=%s' %mass)
            
# set axis labels
xlabel(r'$\logT_{eff}$')
ylabel(r'$\logL$')
legend()
plt.gca().invert_xaxis()


"""
PLOT ERRORBOX:
"""
plt.plot([Log_Teff_lower, Log_Teff_upper, Log_Teff_upper, Log_Teff_lower, Log_Teff_lower], [Log_L_lower, Log_L_lower, Log_L_upper, Log_L_upper, Log_L_lower], 'r-.', alpha=0.5, linewidth=3)
