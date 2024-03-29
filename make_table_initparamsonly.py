#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 15:56:52 2019

@author: janne

make_table_og l=0 pi 0 and pi1
"""

import gyre_output_read as gar
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import mesa_reader as mr
import re
from pylab import *

def getmodelparams(fname):
    constraint_noprems = 400
    fnumbers = []
    alle = []
    #fname = '/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2/'
    
    for root, dirs, files in sorted(os.walk(fname)):
            files.sort(key=lambda x: '{0:0>20}'.format(x)) 
            for file in files:
                if not file.endswith('freqs.dat'): #and os.path.exists(file)==True:
                    continue 
                
                fdires = os.path.join(root,file)
                fdirec = os.path.join(root)
                finaldir = fdirec.strip("/")
                fdata = gar.readmesa(fdires)
                dire = finaldir.split('-')
                mass = float(dire[1])
                z    = float(dire[2])
                y    = float(dire[3])
                mlt  = float(dire[4])
                #ove  = [float(dire[5])]

                fnum = re.search('profile(.+?)-freqs.dat', fdires)
                        
                if fnum: 
                    fnums = fnum.group(1)
                    if int(fnums) >= int(constraint_noprems): 
                                   
                        fnumbers += [fnums]
                        alle += [[mass, z, y, mlt, fnums]]
                    
    np.asarray(alle)
    np.savetxt('temp1_l012.txt', alle, delimiter=",", newline = "\n", fmt="%s")
    #np.savetxt('test1.txt', alle, fmt='%10d' )
    return

getmodelparams('/home/janne/Gunter_project/44_tau/output_postms_3ms/LOGS-1.5-0.02-0.7-0.2')