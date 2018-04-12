from pathlib import Path
from pyomeca import fileio as pyoio
from pyosim.project import Project

PROJECT_PATH = Path('./project_sample')
DATA_FOLDER = Path('.') / 'data'
MARKERS_ANALOGS_C3D = DATA_FOLDER / 'markers_analogs.c3d'

# open project
project = Project(path=PROJECT_PATH)

m_c3d_1 = pyoio.read_c3d(MARKERS_ANALOGS_C3D, idx=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                         kind='markers', prefix=':')

from pyomeca.math import matrix
m_c3d_1 = matrix.reshape_3d_to_2d_matrix(m_c3d_1)

import opensim as osim
table = osim.TimeSeriesTableVec3()

adapter = osim.C3DFileAdapter()
tables = adapter.read('./data/marcheAccel01.c3d')
markers = tables['markers']


# create markers TRC from csv

# create markers TRC from c3d

# create analogs STO from csv

# create analogs STO from c3d

# create emg STO from csv
