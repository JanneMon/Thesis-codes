import numpy as np


def readmesa(fname):
    """
    Reads standard format MESA history file.
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
        header = np.genfromtxt(lines[1:3], names=True)
        data = np.genfromtxt(lines[5:], names=True)

    return data, header
