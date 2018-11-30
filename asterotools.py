#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 13:53:31 2018

@author: janne

"""

import numpy as np


def readmesa(fname, numfreqs):
    """
    Reads standard format MESA astero module sample file, for comparison of frequencies
    The returned arrays contains named fields. The available fields can be seen
    using `data.dtype.names` and accessed with e.g. `data['log_g']`.
    Arguments:
    - `fname` : Name of history file
    Returns:
    - `data`  : Array with data columns
    - `header`: Array with header info
    """

    # Assuming Python 3 read mode (for comparability with NumPy)
    with open(fname, 'rb') as f:
        lines = f.readlines()
        header = np.genfromtxt(lines[0:2])
        data = np.genfromtxt(lines[2:numfreqs+2])

    return data, header