#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 13:16:14 2019

@author: janne
"""
import gyre_output_read as gar
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import mesa_reader as mr
import re
from pylab import *


constraint_noprems = 650
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

#observations = []
               
def get_freqs(fname):
    alle = []
    fnumbers = []
    allobs = []
    
    for root, dirs, files in sorted(os.walk(fname)):
        files.sort(key=lambda x: '{0:0>20}'.format(x)) 
        for file in files:
            if not file.endswith('freqs.dat'): #and os.path.exists(file)==True:
                continue 
            
            fdires = os.path.join(root,file)
            fdata = gar.readmesa(fdires)
            
            if fdata[0][1] == 1 and fdata[1][1] == 2:
                    fnum = re.search('profile(.+?)-freqs.dat', fdires)
                    
                    if fnum: 
                       fnums = fnum.group(1)
                    if int(fnums) >= int(constraint_noprems): 
                        
                        chi_radial = (np.abs(radial_funda - fdata[0][4])/radial_funda_unc)**2
                        chi_first = (np.abs(radial_first - fdata[1][4])/radial_first_unc)**2
                        
                        fnumbers += [fnums]
                        alle += [[chi_radial, chi_first, fnums]]
                    
    for i in fnumbers:
        #print(i)
        obs = getprofile(fname, i)
        allobs += [obs]       
    
    return alle, allobs

def getprofile(fname, pnumber):
    
    #print(fname, pnumber)
    
    profiles_indir = mr.MesaLogDir(fname)
    pr = profiles_indir.profile_data(profile_number=pnumber)
    
    teff = pr.Teff
    r = pr.photosphere_r
    l = pr.photosphere_L
    m = pr.initial_mass
    m_solar = 1.9892 * 10 ** (33)
    r_solar = 6.9598 * 10 ** (10)
    R = r*r_solar
    M = m*m_solar
    G = 6.67428 * 10 ** (-8)
    g = G*M/R**2
   
    chi_l = (np.abs(np.log10(l) - Log_L_obs)/Log_L_obs_unc)**2
    chi_teff = (np.abs(np.log10(teff) - Log_Teff_obs)/Log_Teff_obs_unc)**2
    chi_g = (np.abs(np.log10(g) - Log_g_obs)/Log_g_obs_unc)**2
    
    observations = [chi_l, chi_teff, chi_g]
    
    return observations
"""

def getprofile(fname, pnumber):
    loggs = []
    alle_obs = []
    logteffs = []
    for root, dirs, files in sorted(os.walk(fname)):
        for file in files:
            if file.startswith('profile') and file.endswith('.data'):
                 
                profiledirs = os.path.join(root,file)
                profileroots = os.path.join(root)
                           
                
                           
                pnum = re.search('profile(.+?).data', profiledirs)
                
                if pnum: 
                   pnums = pnum.group(1)
                if int(pnums) >= int(constraint_noprems): 
                   #print(pnums)
                   
                   profiles_indir = mr.MesaLogDir(fname)
                   pr = profiles_indir.profile_data(profile_number=pnumber)
                   pr_modelnos = pr.model_number
                   
                   teff = pr.Teff
                   #logteff = np.log(teff)r = pr.photosphere_r
                   r = pr.photosphere_r
                   m = pr.initial_mass
                   m_solar = 1.9892 * 10 ** (33)
                   r_solar = 6.9598 * 10 ** (10)
                   R = r*r_solar
                   M = m*m_solar
                   G = 6.67428 * 10 ** (-8)
                   #logg = np.log(g) 
                   g = G*M/R**2
                   
                   #profile_numbers.append(pnums)
                   loggs.append(g)
                   logteffs.append(teff)
                   all_observables = [g, teff, pnums]
                   alle_obs.append(all_observables)
                
                
                   return alle_obs
"""          
allchi = []
allnos = []
for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_postms_3ms/')):#output_test_mlt_freqs/output_test_mlt/')):
    dirs.sort(key=lambda x: '{0:0>20}'.format(x))    
    for dire in dirs:
            #plt.figure(dire)
            dires = os.path.join(root,dire)
            alle_freqs, alle_obs = get_freqs(dires)
            
            for i in range(0,len(alle_obs)):
                chi2 = alle_freqs[i][0] + alle_freqs[i][1] + alle_obs[i][0] + alle_obs[i][1] + alle_obs[i][2]
                allchi += [chi2]
                allnos += [alle_freqs[i][2]]
            
            minValue = min(allchi)
            print(minValue)
            entry = allchi.index(minValue)
            #print(allnos[entry])
            
            #Fin min chi for each dir
            
            #print(min(allchi))
            