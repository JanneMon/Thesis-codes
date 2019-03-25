#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:58:13 2019

@author: janne
"""

from pylab import *
import numpy as np
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
import gyre_output_read as gyr
plt.close("all")
#import natsort

def onedir(fname):
    Log_Teff_obs = 3.839
    #Log_L_obs = 1.340
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
    
    #l = 10
    #radial_unc = l* 0.05
    #radial_funda_lower = radial_funda - radial_unc
    #radial_funda_upper = radial_funda + radial_unc
    #radial_first_upper = radial_first + radial_unc
    #radial_first_lower = radial_first - radial_unc

    frequencies = []
    frequency_dirs = []
    frequency_roots = []
    temp = []
    dires = []
    test_result = []
    logg_dires = []
    diffsndirs = []
    minimum = []


    for root, dirs, files in sorted(os.walk(fname)):
        logdirs = os.path.join(root)
        dires += [logdirs]
        for file in files:
            
            if file.startswith('history'):
                  
                    #print(os.path.join(root,file))
                direcs = os.path.join(root,file)
                rooties = os.path.join(root)
                #print(natsort.natsorted(dirs,reverse=True))
                
                h = mr.MesaData(direcs)
                mass = h.initial_mass
                model = h.model_number
                index = h.star_age > 2.0e7
                noms_model = model[index]
                noms_logg = h.log_g[index]
                
                
                logg_dir = [noms_logg, noms_model, rooties]
                logg_dires.append(logg_dir)
               
                noms_Teff = h.log_Teff[index]
                noms_L = h.log_L[index]
        
                test_result = np.zeros((len(noms_model),3))
                #rint(test_result)
                for i in range(0,len(noms_model)):
                    test_result[i][0] = noms_model[i]
                    test_result[i][1] = noms_logg[i]
                    test_result[i][2] = noms_Teff[i]
               
                plt.plot(noms_Teff, noms_logg, '-',label='M=%s' %mass)
            
            if file.startswith('profile') and file.endswith('.data'):
                
                profiledirs = os.path.join(root,file)
                
                pnum = re.search('profile(.+?).data', profiledirs)
            
                if pnum: 
                    pnums = pnum.group(1)  
                
                profiles_indir = mr.MesaLogDir(fname)
                pr = profiles_indir.profile_data(profile_number=pnums)
                pr_modelnos = pr.model_number
                
                
                if pr_modelnos == noms_model[0]:
                    cutoff = pnums
        
            if file.endswith('freqs.dat'):
                gyredirs = os.path.join(root,file)
                gyreroots = os.path.join(root)
                fnum = re.search('profile(.+?)-freqs.dat', gyredirs)
            
                if fnum: 
                    fnums = fnum.group(1)  
                if int(cutoff) <= int(fnums):
                    #print(fnums)
                    
                    #print(gyredirs)
                    
                    freqs = gyr.readmesa(gyredirs)
                    
                    frequencies += [freqs]
                    frequency_dirs += [gyredirs]
                    frequency_roots += [gyreroots]
                    allfreqs = [freqs ,gyredirs,gyreroots]
                    temp.append(allfreqs)
    
    profiles = []
    differs = []
    temp3 = []
    minValue = None
    
    
    for i in range(0,len(temp)):
        if size(temp[i][0]) ==1:
            continue
        if temp[i][0][0][1] == 1 and temp[i][0][1][1] == 2:
            #print('hej')
            
            succesfull_profiles = temp[i][1]
            profile_directories = temp[i][2]
            difference = np.abs(temp[i][0][0][4]-radial_funda)
            #print(difference)
            
            #difference_next = np.abs(temp[i+1][0][0][4]-radial_funda)
           
            currentValue = difference
            
            if minValue == None:
                minValue = currentValue
            else:
                minValue = min(minValue, currentValue)
                
        
            temp2 = [succesfull_profiles, difference]
            diffsndirs.append(temp2)
            
            profiles.append(profile_directories)
            differs.append(difference)
    
    minimum = differs.index(minValue)
    minimum_profile = diffsndirs[minimum]
    
    gnum = re.search('profile(.+?)-freqs.dat', minimum_profile[0])
            
    if gnum: 
        gnums = gnum.group(1)        
        
    profiledata = mr.MesaLogDir(fname)
    p = profiledata.profile_data(profile_number=gnums)
    
    teff = p.Teff
    #print(teff)
    logteff = np.log10(teff)
    lmodel = p.photosphere_L
    logl = np.log10(lmodel)
    modelno_profile = p.model_number 
    
    entry = np.where(logg_dires[0][1]== modelno_profile)
    best_logg = logg_dires[0][0][entry]
    
    plt.plot(logteff,best_logg,'k.', MarkerSize = 15)
    
    """

    results_final = []

    for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_3ms/')):
        for dire in dirs:
            plt.figure(dire)
            dires = os.path.join(root,dire)
            #print(dires)
            results = petersen_plot(dires)
            results_final.append(results)
            #print(results)
            
            results
        #print(logteff)           
                    
    
    #alllogteffs.append(logteffs)
    
    #plt.plot([alllogteffs[i][0],alllogteffs[i][-1]],[working_logg_dires[0], working_logg_dires[-1]],'k--') 
    
    """

    # set axis labels
    xlabel(r'$\logT_{eff}$')
    ylabel(r'$\log(g)$')
    legend()
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()
    plt.rcParams.update({'font.size': 20})
    

    #PLOT ERRORBOX:

    plt.plot([Log_Teff_lower, Log_Teff_upper, Log_Teff_upper, Log_Teff_lower, Log_Teff_lower], [Log_g_lower, Log_g_lower, Log_g_upper, Log_g_upper, Log_g_lower], 'r-.', alpha=0.5, linewidth=3)
    
    return best_logg,logteff

onedir('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')
