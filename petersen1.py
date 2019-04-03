#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:34:44 2019

@author: janne

Making petersen diagrams! 
"""

from pylab import *
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
import gyre_output_read as gyr
import numpy as np
plt.close("all")

radial_funda = 6.8980
radial_first = 8.9606

r = 0.769815
runc = 0.000002
r_upper = r + runc
r_lower = r - runc


dires = []
frequencies = []
temp = []
frequency_dirs = []
frequency_roots = []
allfreqs = []
observed_ratio = 0.769815

#minValues = []


def petersen_plot(fname, minValueFirst):
    #directory = '/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1'
    list_number = [os.path.join(fname, file) 
                   for file in sorted(os.listdir(fname)) 
                   if file.endswith('-freqs.dat')]
    constraint_noprems = 480
    periods = []
    ratios = []
    minima = []
    alle = []
    
    for file in list_number:
        #file.sort(key=lambda x: '{0:0>20}'.format(x))
        pnum = re.search('profile(.+?)-freqs', file)
        if pnum: 
            pnums = pnum.group(1)
        if int(pnums) >= int(constraint_noprems):
            #print(pnums)
        
            freqs = gyr.readmesa(file)
            if size(freqs) == 1:
                continue
            if not freqs[0][1] == 1 and freqs[1][1] == 2:
                continue
            
            allfrequencies = [freqs[0][4]/freqs[1][4], file, pnums]
            
            
            rat = freqs[0][4]/freqs[1][4]
            
            currentValueFirst = np.abs(rat-r)
                    
            if minValueFirst == None:
                minValueFirst = currentValueFirst
            else:
                minValueFirst = min(minValueFirst, currentValueFirst)
            
            minima += [ minValueFirst, pnums ]
            ratios += [freqs[0][4]/freqs[1][4]]
            periods += [1. / freqs[0][4]]
            alle.append(allfrequencies)
    
    plt.plot(np.log10(1. / radial_funda), observed_ratio,'k*')
    #legend()
    plt.plot(np.log10(periods), ratios, 'r-')
    #plt.gca().invert_xaxis()
    # plt.gca().invert_yaxis()
    ylabel(r'$\Pi_1/\Pi_0$')
    xlabel(r'$log\Pi_0$')
    plt.rcParams.update({'font.size': 15}) 
    
    return alle, minValueFirst, ratios, periods 

def getpdata(newdir, pnumber):
    
    l = mr.MesaLogDir(newdir)

    p = l.profile_data(profile_number=pnumber)
    mass = p.initial_mass
    
    return mass

    
results_final = []
chis = []
peris = []
firstchi = None
chisfordir = []

for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/output_postms_3ms_01ov_mlt02/')):
        for dire in dirs:
            plt.figure(dire)
            dires = os.path.join(root,dire)
            #print(dires)
            alle, minValues, ratios, periods = petersen_plot(dires, None)
            
            some = r + minValues
            entry = ratios.index(some)
            #print(alle[entry])
            
            peri = periods[entry]
            mini = ratios[entry]
            
            plt.plot(np.log10(peri),mini ,'b.', MarkerSize = 15)
            
            
            #print(alle[entry])
            
            diff1 = np.abs(np.log10(peri) - np.log10(1. /radial_funda))
            diff2 = np.abs(mini - r)
            
            print(diff1,diff2)
            chi = (diff1 + diff2)**2 / 2
            
            chisfordir += [chi, alle[entry], dires]
            peris.append(peri)
            chis.append(chi)

best_chi = min(chis)
best_entry = chisfordir.index(best_chi)
best_pentry = best_entry + 1
best_pnum = chisfordir[best_pentry][2]
best_dir = chisfordir[best_pentry + 1]
            
best_masses = getpdata(best_dir, best_pnum)
print(best_masses)

#best = min(chis)   
#bestentry = chisfordir.index(best)
#pentry = bestentry + 1
#pnumber = chisfordir[pentry]      
#plt.figure()
#plt.plot(peris, chis, 'g.' )
            
            
            
           # results_final.append(results.copy())
            #print(results)
            




