"""
Test and example script for file IO
"""

from pathlib import Path
from pyomeca import fileio as pyoio

# Path to data
DATA_FOLDER = Path('.') / 'data'
MARKERS_CSV = DATA_FOLDER / 'markers.csv'
MARKERS_ANALOGS_C3D = DATA_FOLDER / 'markers_analogs.c3d'
ANALOGS_CSV = DATA_FOLDER / 'analogs.csv'

# create markers TRC from csv
# m_csv_1 = pyoio.read_csv(MARKERS_CSV, first_row=5, first_column=2, header=2,
#                          idx=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], prefix=':')

# create markers TRC from c3d
m_c3d_1 = pyoio.read_c3d(MARKERS_ANALOGS_C3D, idx=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         kind='markers', prefix=':')

# create analogs STO from csv

# create analogs STO from c3d

# create emg STO from csv

# create emg STO from c3d
print('')