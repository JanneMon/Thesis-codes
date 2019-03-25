#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 14:58:13 2019

@author: janne
"""

from pylab import *
import os
import mesa_reader as mr
import matplotlib.pyplot as plt
import gyre_output_read as gyr
plt.close("all")
import natsort

Log_Teff_obs = 3.839
Log_L_obs = 1.340
Log_g_obs = 3.6

Log_Teff_obs_unc = 0.007
Log_L_obs_unc = 0.0065 
Log_g_obs_unc = 0.1

n = 3

Log_Teff_ns = n*Log_Teff_obs_unc
Log_L_ns = n*Log_L_obs_unc
Log_g_ns = n*Log_g_obs_unc

Log_Teff_lower = Log_Teff_obs - Log_Teff_ns
Log_Teff_upper = Log_Teff_obs + Log_Teff_ns
Log_L_lower = Log_L_obs - Log_L_ns
Log_L_upper = Log_L_obs + Log_L_ns
Log_g_upper = Log_g_obs + Log_g_ns
Log_g_lower = Log_g_obs - Log_g_ns

radial_funda = 6.8980
radial_first = 8.9606

l = 10
radial_unc = l* 0.05
radial_funda_lower = radial_funda - radial_unc
radial_funda_upper = radial_funda + radial_unc
radial_first_upper = radial_first + radial_unc
radial_first_lower = radial_first - radial_unc

frequencies = []
frequency_dirs = []
frequency_roots = []
temp = []
ages = []
profdata = []
dires = []
logg_model = []
test_result = []
allresults_history = []
logg_dires = []
diffsndirs = []
minimum = []


for root, dirs, files in sorted(os.walk('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')):
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
            
            profiles_indir = mr.MesaLogDir('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')
            pr = profiles_indir.profile_data(profile_number=pnums)
            pr_modelnos = pr.model_number
            
            if pr_modelnos == noms_model[0]:
                cutoff = pnums
    #allresults_history.append(test_result)
    
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
    
profiledata = mr.MesaLogDir('/home/janne/Gunter_project/44_tau/example_10_masses/LOGS-1.50-0.02-0.7-0.4')
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

profiles = []
roots_all = []
alle = []
alle2 = []
profnos = []
working_logg_dires = []
logteffs = []
allprofiles = []
profiles_all = []
modelnos = []
alllogteffs = []
diffs1 = []
diffs2 = []
diffs3 = []
diffsndirs = []
mins = []
minimum = []
diff = []
smallest = 0


for i in range(0,len(temp)):
    if size(temp[i][0]) ==1:
        continue
    if temp[i][0][0][1] == 1 and temp[i][0][1][1] == 2:
        
        succesfull_profiles = temp[i][1]
        profile_directories = temp[i][2]
        
        
        diff = np.abs(temp[i][0][0][4]-radial_funda
        
        temp2 = [succesfull_profiles, diff]
        diffsndirs.append(temp2)
        



for i in range(0,len(temp)):
    if size(temp[i][0]) == 1:
        continue
    if temp[i][0][0][1] == 1 and radial_funda_lower < temp[i][0][0][4] and temp[i][0][0][4] < radial_funda_upper:
           #print(i,temp[i][1])
        succesfull_profiles = temp[i][1]
        profile_directories = temp[i][2]
        
        
        diff = np.abs(temp[i][0][0][4]-radial_funda)
        diffs.append(diff)
       
        #print(diff,succesfull_profiles)
        temp2 = [succesfull_profiles, diff]
        
        diffsndirs.append(temp2)
        #print(diffsndirs)
        
        #profiles.append(succesfull_profiles)
        gnum = re.search('profile(.+?)-freqs.dat', succesfull_profiles)
        
        if gnum: 
             gnums = gnum.group(1)
        
        root_pnumber = [profile_directories, gnums]
        alle.append(root_pnumber)
        
    if temp[i][0][1][1] == 2 and radial_first_lower < temp[i][0][1][4] and temp[i][0][1][4] < radial_first_upper:
        
        succesfull_profiles2 = temp[i][1]
        profile_directories2 = temp[i][2]
     
        #profiles.append(succesfull_profiles)
        gnum2 = re.search('profile(.+?)-freqs.dat', succesfull_profiles2)
        
        if gnum2: 
             gnums2 = gnum2.group(1)
        
        root_pnumber2 = [profile_directories2, gnums2]
        alle2.append(root_pnumber2) 

        alle_final = [alle,alle2]


i = -1      
for b in alle_final:
    
    i += 1
    np.concatenate(b)
    
    for k, (logdir,profnum) in enumerate(b):
        #print(k)
        profiledata = mr.MesaLogDir(logdir)
        p = profiledata.profile_data(profile_number=profnum)
        
        teff = p.Teff
        #print(teff)
        logteff = np.log10(teff)
        lmodel = p.photosphere_L
        logl = np.log10(lmodel)
        modelno_profile = p.model_number 
        #print(modelno_profile)
        
        
        
        for r in range(0,len(logg_dires)):
            if logdir == logg_dires[r][2]:
                for t in range(0,len(logg_dires[r][1])):
                    #print(modelno_profile)
                    #print(modelno_profile, logg_dires[r][1][t])
                    
                    if not modelno_profile == logg_dires[r][1][t]:#logg_dires[r][1][t]:
                        continue
                    #print(modelno_profile, logg_dires[r][1][t])
                    some_logg_dires = logg_dires[r][0][t]
                    working_logg_dires.append(some_logg_dires)
                    
                    plt.plot(logteff,logg_dires[r][0][t],'k.', MarkerSize = 15)
                    logteffs.append(logteff)
        #print(logteff)           
                    
    
    alllogteffs.append(logteffs)
    #plt.plot([logteffs[0],logteffs[-1]],[working_logg_dires[0], working_logg_dires[-1]],'k--')
    plt.plot([alllogteffs[i][0],alllogteffs[i][-1]],[working_logg_dires[0], working_logg_dires[-1]],'k--') 
    
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

