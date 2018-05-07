"""
Example: export emg to sto
"""

from pathlib import Path

import numpy as np

from pyomeca.obj.analogs import MVC
from pyosim import Conf
from pyosim.obj import Analogs3dOsim

# path
PROJECT_PATH = Path('../Misc/project_sample')

conf = Conf(project_path=PROJECT_PATH)

params = {
    'band_pass_cutoff': [10, 425],
    'low_pass_cutoff': 5,
    'order': 4,
    'outlier': 3,
    'emg_labels': conf.get_conf_field(participant='dapo', field=['emg', 'targets'])
}

participants = conf.get_participants_to_process()

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')
    directories = conf.get_conf_field(participant=iparticipant, field=['emg', 'data'])
    assigned = conf.get_conf_field(participant=iparticipant, field=['emg', 'assigned'])

    # --- MVC
    try:
        mva = conf.get_conf_field(participant=iparticipant, field=['emg', 'mva'])
    except KeyError:
        mvc = MVC(
            directories=directories,
            channels=assigned,
            outlier=params['outlier'],
            band_pass_cutoff=params['band_pass_cutoff'],
            low_pass_cutoff=params['low_pass_cutoff'],
            order=params['order']
        )
        mva = mvc.get_mva()
        # add mva in configuration
        conf.add_conf_field({
            iparticipant: {'emg': {'mva': mva}}
        })
    mva = np.array(mva, dtype=float)

    # --- Export EMG
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
                emg = Analogs3dOsim.from_c3d(itrial, names=iassign_without_nans, prefix=':')
                if nan_idx:
                    # if there is any empty assignment, fill the dimension with nan
                    for i in nan_idx:
                        emg = np.insert(emg, i, np.nan, axis=1)
                    print(f'\t{itrial.stem} (NaNs: {nan_idx})')
                else:
                    print(f'\t{itrial.stem}')

                # check if dimensions are ok
                if not emg.shape[1] == len(iassign):
                    raise ValueError('Wrong dimensions')
                break
            except IndexError:
                emg = []

        # processing
        emg = emg \
            .band_pass(freq=emg.get_rate, order=params['order'], cutoff=params['band_pass_cutoff']) \
            .center() \
            .rectify() \
            .low_pass(freq=emg.get_rate, order=params['order'], cutoff=params['low_pass_cutoff']) \
            .normalization(ref=mva, scale=1)

        emg.get_labels = params['emg_labels']
        sto_filename = f"{PROJECT_PATH / iparticipant / '0_emg' / itrial.stem}.sto"
        emg.to_sto(filename=sto_filename)
