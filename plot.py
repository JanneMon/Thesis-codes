# -*- coding: utf-8 -*-

# Modules
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# Personal modules
import mesatools as mt

# Close all open plots!
plt.close('all')

# Seaborn settings (with new interface, version 0.8.x)
# -> Documentation:  http://seaborn.pydata.org/generated/seaborn.set.html
# -> Possible contexts: paper, notebook, talk, poster
sns.set(context='talk', style='ticks', palette='colorblind',
        color_codes=True, font_scale=1.0)

# How to use XKCD color names
greycol = sns.xkcd_rgb["greyish"]

# Named colormap --> Can be used with cmap=plt.get_cmap(cmapname)
cmapname = 'viridis'

# Labels as raw strings for math support
xlab = r'$\log(T_{\mathregular{eff}})$ [K]'
ylab = r'$\log(L)$'
# ylab = r'$\log(g)$'

# Read data from MESA
data, header = mt.readmesa('/home/janne/Gunter_project/44_tau/LOGS/history.data')
teff = data['log_Teff']
radius = data['log_L']
# logg = data['log_g']

# Plot into multi-paged pdf file
with PdfPages('44tau.pdf') as pdf:

    #
    # First plot
    #
    plt.figure()
    
    #x1 = 3.78
    #x2 = 3.89
    #y1 = 0.5
    #y2 = 1.5
    
    #x1,x2,y1,y2 = plt.axis()
   # plt.axis((x1,x2,y1,y2))
    #ax.set_xlim([3.85,3.9])
    #ax.set_ylim([0,1.5])
    # Add plot with a label (with math symbols) and make it transparent
    plt.plot(teff, radius, label=r'2.01 M$_{\odot}$, modified', alpha=0.7)

    # Labels --> If more space is required around the labels,
    #            add: labelpad = 10 (or a different number)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    # Invert axes for Kiel diagram
    # plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()

    # Place a legend
    plt.legend(loc='best')

    # Remove the two unnecessary lines from the plot
    sns.despine()

    # Will save current figure to pdf and re-calculate trimming correctly
    pdf.savefig(bbox_inches='tight')


    #
    # Second plot
    #

    # Open another figure
    #plt.figure()

    # HERE GOES THE PLOTTING!

    # Save the new figure
    pdf.savefig(bbox_inches='tight')
