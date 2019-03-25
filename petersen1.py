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
plt.close("all")

radial_funda = 6.8980
radial_first = 8.9606

r = 0.77
runc = 0.40
r_upper = r + runc
r_lower = r - runc


dires = []
frequencies = []
temp = []
frequency_dirs = []
frequency_roots = []
allfreqs = []



def petersen_plot(fname):
    #directory = '/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1'
    list_number = [os.path.join(fname, file) for file in os.listdir(fname) if file.endswith('-freqs.dat')]
    #plt.figure(fname)
    for file in list_number:
        #print(file)
        freqs = gyr.readmesa(file)
        if size(freqs) == 1:
            continue
        for i in range(0,len(freqs)):
                    #for j in range(0,len(freqs[i]):
                    if not freqs[0][1] == 1 and freqs[1][1] == 2:
                        continue
                    ratio = freqs[0][4]/freqs[1][4]
                    
                    plt.plot(np.log(freqs[0][4]),ratio,'r.')
    
    return freqs            
        

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

#freqs = petersen_plot('/home/janne/Gunter_project/44_tau/example_3ms/LOGS-1')    
"""
for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_3ms')):
    logdirs = os.path.join(root)
    #plt.plot()
    dires += [logdirs]
    for file in files:
        if file.endswith('-freqs.dat'):
            gyredirs = os.path.join(root,file)
            gyreroots = os.path.join(root)
            #print(gyredirs)
            freqs = gyr.readmesa(gyredirs)
            
            
            #for k in len(1,dires)
            for i in range(0,len(freqs)):
                #for j in range(0,len(freqs[i]):
                if not freqs[0][1] == 1 and freqs[1][1] == 2:
                    continue
                ratio = freqs[0][4]/freqs[1][4]
            plt.plot(freqs[0][4],ratio,'k.')
            
            plt.plot()
"""            
"""frequencies += [freqs]
            frequency_dirs += [gyredirs]
            frequency_roots += [gyreroots]
            allfreqs = [freqs ,gyredirs,gyreroots]
            temp.append(allfreqs)
            
            
            for i in range(0,len(temp)):
                    k = temp[i][2] 
                    if not k == gyreroots:
                        continue
                    for j in(0,len(1,3))
                        if not temp[i][0][0][1] == 1 and temp[i][0][1][1] == 2:
                            continue
                        ratio = temp[i][0][1][4]/temp[i][0][0][4]
                        plt.figure(k)
                        plt.plot(np.log10(temp[i][0][0][4]),ratio,'r.')
                        #plt.figure()
                        if r_lower < ratio < r_upper:
                            
                            print(ratio)
                            #plt.figure()
                            #plt.plot(np.log10(temp[i][0][0][4]),ratio,'r.')
                            #print(k)
                            #print('succes')
"""                  
ylabel(r'$\Pi_1/\Pi_0$')
xlabel(r'$\Pi_0$')
#legend()
#plt.gca().invert_xaxis()
#plt.gca().invert_yaxis()
plt.rcParams.update({'font.size': 20})
                
