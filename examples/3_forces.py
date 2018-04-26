"""
Example: export forces to sto
"""

from pathlib import Path

import numpy as np

from pyosim.conf import Conf
from pyosim.obj.analogs import Analogs3dOsim

# path
PROJECT_PATH = Path('../Misc/project_sample')
CALIBRATION_MATRIX = Path('../tests/data/forces_calibration_matrix.csv')

conf = Conf(project_path=PROJECT_PATH)

calibration_matrix = np.genfromtxt(CALIBRATION_MATRIX)
params = {
    'low_pass_cutoff': 30,
    'order': 4,
    'forces_labels': conf.get_conf_field(participant='dapo', field=['analogs', 'targets'])
}

PARTICIPANTS = conf.get_participants_to_process()

for iparticipant in PARTICIPANTS:
    print(f'\nparticipant: {iparticipant}')
    directories = conf.get_conf_field(participant=iparticipant, field=['analogs', 'data'])
    assigned = conf.get_conf_field(participant=iparticipant, field=['analogs', 'assigned'])

    for itrial in Path(directories[0]).glob('*.c3d'):
        # try participant's channel assignment
        for iassign in assigned:
            # get index where assignment are empty
            nan_idx = [i for i, v in enumerate(iassign) if not v]
            if nan_idx:
                iassign_without_nans = [i for i in iassign if i]
            else:
                iassign_without_nans = iassign

            try:
                forces = Analogs3dOsim.from_c3d(itrial, names=iassign_without_nans, prefix=':')
                if nan_idx:
                    # if there is any empty assignment, fill the dimension with nan
                    for i in nan_idx:
                        forces = np.insert(forces, i, np.nan, axis=1)
                    print(f'\t{itrial.parts[-1]} (NaNs: {nan_idx})')
                else:
                    print(f'\t{itrial.parts[-1]}')

                # check if dimensions are ok
                if not forces.shape[1] == len(iassign):
                    raise ValueError('Wrong dimensions')
            except IndexError:
                forces = []

        # processing
        forces = forces \
            .

        # --- Get force onset-offset

    forces.get_labels = params['forces_labels']
    sto_filename = PROJECT_PATH / iparticipant / '0_forces' / itrial.parts[-1].replace('c3d', 'sto')
    forces.to_sto(filename=sto_filename)
