"""
Example: export emg to sto
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pyosim.conf import Conf
from pyosim.obj.analogs import Analogs3dOsim

# path
PROJECT_PATH = Path('../Misc/project_sample')

conf = Conf(project_path=PROJECT_PATH)

PARTICIPANTS = ['arst']

for iparticipant in PARTICIPANTS:
    print(f'\nparticipant: {iparticipant}')
    directories = conf.get_conf_field(participant=iparticipant, field=['emg', 'data'])
    assigned = conf.get_conf_field(participant=iparticipant, field=['emg', 'assigned'])

    for idir in directories:
        print(f'\n\tdirectory: {idir}')

        for itrial in Path(idir).glob('*.c3d'):
            print(f'\t\ttrial: {itrial.parts[-1]}')
            # try participant's channel assignment
            for iassign in assigned:
                # get index where assignment are empty
                nan_idx = [i for i, v in enumerate(iassign) if not v]
                iassign_without_nans = [i for i in iassign if i]
                try:
                    # open file
                    emg = Analogs3dOsim.from_c3d(itrial, names=iassign_without_nans, prefix=':')
                except:
                    break

                # append nan dimensions
                for i in nan_idx:
                    emg = np.insert(emg, i, np.nan, axis=1)
                # check if dimensions are ok
                n = np.isnan(emg).sum(axis=2).ravel()
                # check if dimensions are ok
                if not emg.shape[1] == len(iassign):
                    raise ValueError('Wrong dimension')
                if not np.array_equal(n.argsort()[-len(nan_idx):], nan_idx):
                    raise ValueError('NaN dimensions misplaced')

                # processing
                emg = emg \
                    .band_pass(freq=emg.get_rate, order=4, cutoff=[10, 425]) \
                    .center() \
                    .rectify() \
                    .low_pass(freq=emg.get_rate, order=4, cutoff=5) \
                    .normalization()

                emg[0, :, :].T.plot()
                plt.show()

            sto_filename = PROJECT_PATH / iparticipant / '0_emg' / itrial.parts[-1].replace('c3d', 'trc')
            emg.to_sto(file_name=sto_filename)
