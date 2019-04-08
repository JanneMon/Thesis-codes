#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:29:08 2019

@author: janne

calculate chi2 for one directory
"""

#import make_table_initparams as init
#import make_table_fundfreqs as fund

#import gyre_output_read as gar
#import numpy as np
#import matplotlib.pyplot as plt
#import os, sys
#import mesa_reader as mr
#import re
#from pylab import *
import numpy as np

radial_funda = 6.8980
radial_first = 8.9606

#The following uncertainties are incorrect! - Discuss with Vichi what to do 
radial_funda_unc = 0.001
radial_first_unc = 0.001

Log_L_obs = 1.305
Log_Teff_obs = 3.839
Log_g_obs = 3.6
Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.0065 
Log_g_obs_unc = 0.1

filename = 'results.txt'

final_list = []
total_chi = []
red_chi = []
with open(filename) as f:
    for line in f:
        inner_list = [elt.strip() for elt in line.split(',')]
        final_list.append(inner_list)
        
for i in range(0,len(final_list)):
    fund  = float(final_list[i][0])
    first = float(final_list[i][1])
    teff  = float(final_list[i][7])
    g     = float(final_list[i][8])
    l     = float(final_list[i][9])
    
    chi_fund  = (np.abs(fund-radial_funda))**2/radial_funda_unc
    chi_first = (np.abs(first-radial_first))**2/radial_first_unc
    chi_teff  = (np.abs(teff-Log_Teff_obs))**2/Log_Teff_obs_unc
    chi_g     = (np.abs(g-Log_g_obs))**2/Log_g_obs_unc
    chi_l     = (np.abs(l-Log_L_obs))**2/Log_L_obs_unc 
    
    chi = chi_fund + chi_first + chi_teff + chi_g + chi_l
    
    N = len(final_list)
    P = 5
    K = N-P
    red_chi   = chi/K
    total_chi += [[chi, red_chi]]

output = np.concatenate((final_list, total_chi), axis =1)
np.savetxt("results_final.txt", output, delimiter=",", newline = "\n", fmt="%s")
#output = np.concatenate((final_list,total_chi), axis=0)

                
