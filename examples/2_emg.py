"""
Example: export emg to sto
"""

import os
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from pyomeca.obj.analogs import MVC
from pyosim import Conf
from pyosim.obj import Analogs3dOsim
from project_conf import PROJECT_PATH

# path
MULTIPROC = True

conf = Conf(project_path=PROJECT_PATH)
participants = conf.get_participants_to_process()

params = {
    'band_pass_cutoff': [10, 425],
    'low_pass_cutoff': 5,
    'order': 4,
    'outlier': 5,
    'emg_labels': conf.get_conf_field(participant=participants[0], field=['emg', 'targets'])
}


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


    def process(trial):
        # try participant's channel assignment
        for iassign in assigned:
            # get index where assignment are empty
            nan_idx = [i for i, v in enumerate(iassign) if not v]
            if nan_idx:
                iassign_without_nans = [i for i in iassign if i]
            else:
                iassign_without_nans = iassign

            try:
                emg = Analogs3dOsim.from_c3d(trial, names=iassign_without_nans, prefix=':')
                if nan_idx:
                    # if there is any empty assignment, fill the dimension with nan
                    emg.get_nan_idx = np.array(nan_idx)
                    for i in nan_idx:
                        emg = np.insert(emg, i, np.nan, axis=1)
                    print(f'\t{trial.stem} (NaNs: {nan_idx})')
                else:
                    print(f'\t{trial.stem}')

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
            .normalization(ref=mva, scale=1) \
            .clip(0, 1)

        emg.get_labels = params['emg_labels']
        sto_filename = f"{PROJECT_PATH / iparticipant / '0_emg' / trial.stem}.sto"
        emg.to_sto(filename=sto_filename, metadata={'nColumns': emg.shape[1] + 1})


    if MULTIPROC:
        pool = Pool(os.cpu_count())
        pool.map(process, Path(directories[0]).glob('*.c3d'))
    else:
        for itrial in Path(directories[0]).glob('*.c3d'):
            process(itrial)
