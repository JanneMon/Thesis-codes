
"""
Created on Wed Apr 10 11:25:35 2019

@author: janne
"""
import gyre_output_read as gar
import numpy as np
import os

def to_get_chi2(fname):
    
    filename = 'results_l012.txt'
    final_list = []

    with open(filename) as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            final_list.append(inner_list)

    a = np.asarray(final_list)
    profnums = a[:,4]
    finalarray = []
    bm_array2 = []
    #fname = '/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2'
    
    for h in profnums:
        direc = fname + '/profile' + h + '-freqs.dat'
    
        #dires = os.path.join(root,file)
        data = gar.readmesa(direc)
        harm_degree = data['l']
        radial_order= data['n_pg']

        re_freq_theo = data['Refreq'] # these are the frequencies that will be compared to Lenz and observations. 
        #im_freq = data['Imfreq'] #imaginary part of frequencies are not observable. 
        #print(re_freq_theo)

        re_freq_obs = [ 6.8980, 7.0060, 9.1175, 11.5196, 8.9606, 9.5613, 7.3034, 6.7953, 9.5801, 6.3391, 8.6393, 11.2919]
        re_freq_obs_unc     = np.ones(len(re_freq_obs))*10**(-7)
        #print(len(np.atleast_1d(re_freq_theo)))
        #re_freq_obs_unc = np.ones(len(re_freq_obs)) * 0.1
        remaining_obs = re_freq_obs 
        #remaining_obs_unc = freq_obs_uncertainties
        remaining_theo = np.atleast_1d(re_freq_theo)
        remaining_ells = np.atleast_1d(harm_degree)
        remaining_radial = np.atleast_1d(radial_order)

        best_matching = []
        #names = []

        for ii in range(min(len(np.atleast_1d(re_freq_theo)), len(re_freq_obs))): #default: freq_obs, but depends if freq_obs is longer than re_freq
            best = np.inf
            bestjj = -1
            bestkk = -1
    
            #print(len(remaining_obs))
    
            for jj in range(len(np.atleast_1d(remaining_theo))):
                for kk in range(len(remaining_obs)):
                    val = (remaining_theo[jj] - remaining_obs[kk])**2 / 4 #put uncertainty here  
                    if (val < best):
                        best = val
                        bestjj = jj
                        bestkk = kk
                        
                        # print(best, bestjj, bestkk)
            best_matching += [[remaining_ells[bestjj], remaining_radial[bestjj], remaining_theo[bestjj], remaining_obs[bestkk]]]
                
            remaining_theo = np.delete(remaining_theo, bestjj)
            remaining_ells = np.delete(remaining_ells, bestjj)
            remaining_obs = np.delete(remaining_obs, bestkk)
            #remaining_obs_unc = np.delete(remaining_obs_unc, bestkk)
            remaining_radial = np.delete(remaining_radial,bestjj)
    
            #diff = np.asarray(diff)
            #final = np.append(bm_array,diff)
    
        bm_array = np.asarray(best_matching)           
        bm_array2 += [bm_array]
        finalarray += [[bm_array, h]]

    chi2sum = {}
    
    for i in range(len(finalarray)):
        for k in range(len(finalarray[i][0])):
            pname = finalarray[i][1]
            if pname not in chi2sum.keys():
                chi2sum[pname] = 0
            chi2sum[pname] = chi2sum[pname] + (np.abs(finalarray[i][0][k][2] - finalarray[i][0][k][3])/1*10**(-7))**2
    
    kolonne = chi2sum.values()
    
    output = np.column_stack((final_list, list(kolonne)))
    
    

    np.savetxt("results_l012.txt", output, delimiter=",", newline = "\n", fmt="%s")
    return kolonne 

#kolonne = to_get_chi2('/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2', 'test3.txt')