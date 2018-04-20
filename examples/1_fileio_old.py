from pathlib import Path

from pyosim.obj.markers import Markers3dOsim
from pyosim.obj.analogs import Analogs3dOsim

# Path to data
DATA_FOLDER = Path('..') / 'tests' / 'data'
MARKERS_ANALOGS_C3D = DATA_FOLDER / 'markers_analogs.c3d'
TRC_OUT = DATA_FOLDER / 'markers.trc'
STO_OUT = DATA_FOLDER / 'analogs.sto'

# remove file if already exists
if TRC_OUT.is_file():
    TRC_OUT.unlink()
if STO_OUT.is_file():
    STO_OUT.unlink()

# read markers from c3d
m = Markers3dOsim.from_c3d(MARKERS_ANALOGS_C3D, idx=[0, 1, 2, 3])
# write a trc file
m.to_trc(file_name=TRC_OUT)

# read analogs from c3d
a = Analogs3dOsim.from_c3d(MARKERS_ANALOGS_C3D, names=['1', '2', '3', '4', '5', '6'])
# convert pyomeca's Analogs3d to pyosim's Analogs3dOsim
a = Analogs3dOsim(a)
# write a sto file
a.to_sto(file_name=STO_OUT)
