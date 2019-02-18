#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 16:44:14 2019

@author: janne
"""

from pylab import *
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
plt.close("all")


for root, dirs, files in os.walk('/home/janne/Gunter_project/44_tau/example_alphas'):
    for file in files:
        if file.startswith('history'):
            print(os.path.join(root,file))
            dirs = os.path.join(root,file)
            
            h = mr.MesaData(dirs)
            
            #alpha 
            mass = h.initial_mass
            index = h.star_age > 5e7 
            noms_Teff = h.log_Teff[index]
            noms_L = h.log_L[index]
            #plot(h.log_Teff, h.log_L)
            plot(noms_Teff, noms_L, label='%s$M_{\odot}$' %mass)
            plt.gca().invert_xaxis()

# set axis labels
xlabel('log Effective Temperature')
ylabel('log Luminosity')
legend()