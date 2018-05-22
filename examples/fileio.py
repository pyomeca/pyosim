from pathlib import Path

from pyomeca import fileio as pyoio
from pyosim.types import Markers3dOsim

# Path to data
DATA_FOLDER = Path('..') / 'tests' / 'data'
MARKERS_ANALOGS_C3D = DATA_FOLDER / 'markers_analogs.c3d'
TRC = DATA_FOLDER / 'markers.trc'

# remove file if already exists
if TRC.is_file():
    TRC.unlink()

# read c3d
m = pyoio.read_c3d(MARKERS_ANALOGS_C3D, idx=[0, 1, 2, 3], kind='markers', prefix=':')
# convert pyomeca's Markers3d to pyosim's Markers3dOsim
mosim = Markers3dOsim(m)
# write a trc file
mosim.to_trc(file_name=TRC)
