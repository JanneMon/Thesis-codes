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



for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_zs')):
    for file in files:
        if file.startswith('history'):
            #print(os.path.join(root,file))
            dirs = os.path.join(root,file)
            #print(natsort.natsorted(dirs,reverse=True))
            
            h = mr.MesaData(dirs)
            mass = h.initial_mass
            index = h.star_age > 1.9e7 
            noms_Teff = h.log_Teff[index]
            noms_L = h.log_L[index]
            #plot(h.log_Teff, h.log_L)
            #plot(noms_Teff, noms_L, label='%s$M_{\odot}$' %mass)
            #plt.gca().invert_xaxis()
        elif file.endswith('profile1.data'):
            
            pdirs = os.path.join(root)
            print(pdirs)
            l = mr.MesaLogDir(pdirs)
            p = l.profile_data()
            Z = p.initial_z
            plot(noms_Teff, noms_L, label='Z=%s' %Z)
# set axis labels
xlabel('log Effective Temperature')
ylabel('log Luminosity')
legend()
plt.gca().invert_xaxis()