#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 18:58:39 2019

@author: janne
"""
import mesa_reader as mr
import numpy as np

def getobsparams(fname):
    filename = 'temp1_l012.txt'
    list_of_lists = []
    pdata = []
    
    with open(filename) as f:
        for line in f:
            inner_list = [elt.strip() for elt in line.split(',')]
            list_of_lists.append(inner_list)
            
    for i in range(0,len(list_of_lists)):
        profnum = list_of_lists[i][4]
        profiles_indir = mr.MesaLogDir(fname)
        
        pr = profiles_indir.profile_data(profile_number=profnum)
        
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
        
        pdata += [[np.log10(teff), np.log10(g), np.log10(l)]]
        
    np.asarray(pdata)
    np.savetxt("temp2_l012.txt", pdata, delimiter=",", newline = "\n", fmt="%s")
    
    
    filename1 = 'temp1_l012.txt'
    filename2 = 'temp2_l012.txt'
    files = [[filename1, filename2]]
    
    with open('results_l012.txt', 'w') as outfile:
        for file in files:
            with open(file[0]) as newfile,open(file[1]) as newfile1:
                lines=zip(newfile,newfile1)
                for line in lines:
                    outfile.write(line[0].rstrip() + "," + line[1])
    
    return
#getobsparams('/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2')