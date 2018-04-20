from pathlib import Path

from pyomeca import fileio as pyoio
from pyosim.types import Markers3dOsim, Analogs3dOsim

# Path to data
DATA_FOLDER = Path('..') / 'tests' / 'data'
MARKERS_ANALOGS_C3D = DATA_FOLDER / 'markers_analogs.c3d'
TRC_OUT = DATA_FOLDER / 'markers.trc'
STO_OUT = DATA_FOLDER / 'analogs.sto'

# remove file if already exists
if TRC_OUT.is_file():
    TRC_OUT.unlink()

# read markers from c3d
m = pyoio.read_c3d(MARKERS_ANALOGS_C3D, idx=[0, 1, 2, 3], kind='markers', prefix=':')
# convert pyomeca's Markers3d to pyosim's Markers3dOsim
mosim = Markers3dOsim(m)
# write a trc file
mosim.to_trc(file_name=TRC_OUT)

# read analogs from c3d
a = pyoio.read_c3d(MARKERS_ANALOGS_C3D, names=['1', '2', '3', '4', '5', '6'], kind='analogs', prefix=':')
# convert pyomeca's Analogs3d to pyosim's Analogs3dOsim
aosim = Analogs3dOsim(a)
# write a sto file
aosim.to_sto(file_name=STO_OUT)
