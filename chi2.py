#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 15:21:06 2018

@author: janne

data.dtype.names
"""
import gyre_output_read as gar
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from pylab import *

data, header = gar.readmesa('/home/janne/Gunter_project/gunther_project/44_tau/44tau_nad_output.txt')

harm_degree = data['l']
radial_order= data['n_pg']
acou_num = data['n_p']
grav_num = data['n_g']
#re_omega = data['Re(omega)']
#im_omega = data['Im(omega)']
#re_omega_int = data['Re(omega_int)']
#m_omega_int = data['Im(omega_int)']
re_freq = data['Refreq'] # these are the frequencies that will be compared to Lenz and observations. 
im_freq = data['Imfreq'] #imaginary part of frequencies are not observable. 


cd_to_mhz = 11.58
freq_obs = [6.8980, 7.0060, 9.1175, 11.5196, 8.9606, 9.5613, 7.3034, 6.7953, 9.5801, 6.3391, 8.6393, 11.2919 ]
freq_obs_uncertainties = [2.762223525*10**(-7), 1.212730436*10**(-6), 3.311156496*10**(-6), 1.09791050*10**(-6), 8.454940424*10**(-7), 1.984809926*10**(-6), 1.648992107*10**(-6), 2.793833032*10**(-6), 4.381429983*10**(-6), 4.226006653*10**(-6), 5.442115161*10**(-6), 6.202960588*10**(-6)]


freq_obs = np.asarray(freq_obs)*cd_to_mhz
freq_obs_uncertainties = np.asarray(freq_obs_uncertainties)*cd_to_mhz
im_freq = np.asarray(im_freq)*cd_to_mhz

#filter off positive imaginary frequencies
mask = im_freq>0
im_freq = im_freq[~mask]
re_freq = re_freq[~mask]
radial_order = radial_order[~mask]
harm_degree = harm_degree[~mask]
#freq_obs_uncertainties = freq_obs_uncertainties[~mask] 

#print(re_freq)
# chi2 = 1/k sum(vi_obs-vi_theo)**2

#k = # number of observed oscillation modes


remaining_obs = freq_obs 
remaining_obs_unc = freq_obs_uncertainties
remaining_theo = re_freq
remaining_ells = harm_degree
remaining_radial = radial_order

best_matching = []

for ii in range(min(len(re_freq), len(freq_obs))): #default: freq_obs, but depends if freq_obs is longer than re_freq
    best = np.inf
    bestjj = -1
    bestkk = -1
    
    #print(len(remaining_obs))
    
    for jj in range(len(remaining_theo)):
        for kk in range(len(remaining_obs)):
            val = (remaining_theo[jj] - remaining_obs[kk])**2 / 12 #put uncertainty here  
            if (val < best):
                best = val
                bestjj = jj
                bestkk = kk
    
   # print(best, bestjj, bestkk)
    best_matching += [[remaining_ells[bestjj], remaining_radial[bestjj], remaining_theo[bestjj], remaining_obs[bestkk], remaining_obs_unc[bestkk]]]
    
    remaining_theo = np.delete(remaining_theo, bestjj)
    remaining_ells = np.delete(remaining_ells, bestjj)
    remaining_obs = np.delete(remaining_obs, bestkk)
    remaining_obs_unc = np.delete(remaining_obs_unc, bestkk)
    remaining_radial = np.delete(remaining_radial,bestjj)
    
best_matching = np.asarray(best_matching)
#print(best_matching)
#print(best_matching[:,3])

# Close all open plots!
plt.close('all')

sns.set(context='talk', style='ticks', palette='colorblind',
        color_codes=True, font_scale=1.0)

greycol = sns.xkcd_rgb["greyish"]
cmapname = 'viridis'

xlab = r'Observed frequency $[\mu Hz]$'
ylab = r'Theoretical frequency $[\mu Hz]$'
# ylab = r'$\log(g)$'
obs = best_matching[:,3]
theo = best_matching[:,2]
l = best_matching[:,0]

#construct fake amplitudes for all l=0, l=1 and l=2 modes for both observed and theoretical frequencies
index0 = l == 0
obs_0 = obs[index0] 
theo_0 = theo[index0]

index1 = l == 1
obs_1 = obs[index1] 
theo_1 = theo[index1]

index2 = l == 2
obs_2 = obs[index2] 
theo_2 = theo[index2]

amplitude_0 = [3, 3, 3, 3]
amplitude_1 = [2, 2, 2, 2]
amplitude_2 = [1, 1, 1, 1]


plt.xlim(70,140)
plt.stem(theo_0,amplitude_0, linefmt='b-', markerfmt=" ", basefmt=" ") #linefmt='b-', markerfmt='bo', basefmt='r-'
plt.stem(theo_1,amplitude_1, linefmt='r-', markerfmt=" ", basefmt=" ")
plt.stem(theo_2,amplitude_2, linefmt='g-', markerfmt=" ", basefmt=" ")

plt.show()
#plt.plot()




# Plot into multi-paged pdf file
"""with PdfPages('44tau_freq.pdf') as pdf:

    plt.figure()
    #plt.errorbar(x, y, yerr=None, xerr=None, fmt=''
    plt.errorbar(best_matching[:,3], best_matching[:,2],yerr=None, xerr=best_matching[:,4],fmt='.', label=r'44_tau frequency plot', alpha=0.7)
    plt.plot(xx, yy)
    plt.plot(xx, xx, '--')
    # Labels --> If more space is required around the labels,
    #            add: labelpad = 10 (or a different number)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    #plt.show()
    # Place a legend
    #plt.legend(loc='best')

    # Will save current figure to pdf and re-calculate trimming correctly
    pdf.savefig(bbox_inches='tight')


    #
    # Second plot
    #

    # Open another figure
    plt.figure()

    # HERE GOES THE PLOTTING!

    # Save the new figure
    pdf.savefig(bbox_inches='tight')
    """
    