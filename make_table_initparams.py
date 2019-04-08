#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 17:29:08 2019

@author: janne

calculate chi2 for one directory
"""

import gyre_output_read as gar
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import mesa_reader as mr
import re
from pylab import *

filename = 'test1.txt'
fname = '/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2/'

list_of_lists = []
pdata = []

with open(filename) as f:
    for line in f:
        inner_list = [elt.strip() for elt in line.split(',')]
        list_of_lists.append(inner_list)
        
for i in range(0,len(list_of_lists)):
    profnum = list_of_lists[i][6]
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
np.savetxt("test2.txt", pdata, delimiter=",", newline = "\n", fmt="%s")


filename1 = 'test1.txt'
filename2 = 'test2.txt'
files = [[filename1, filename2]]

with open('results.txt', 'w') as outfile:
    for file in files:
        with open(file[0]) as newfile,open(file[1]) as newfile1:
            lines=zip(newfile,newfile1)
            for line in lines:
                outfile.write(line[0].rstrip() + "," + line[1])

