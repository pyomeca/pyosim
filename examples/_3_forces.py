"""
Example: export forces to sto
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pyosim import Conf
from pyosim.obj import Analogs3dOsim
from project_conf import PROJECT_PATH, CALIBRATION_MATRIX

# path

conf = Conf(project_path=PROJECT_PATH)
conf.check_confs()
participants = conf.get_participants_to_process()

calibration_matrix = np.genfromtxt(CALIBRATION_MATRIX, delimiter=',')
params = {
    'low_pass_cutoff': 30,
    'order': 4,
    'forces_labels': conf.get_conf_field(participant=participants[0], field=['analogs', 'targets'])
}


for iparticipant in participants:
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
                    forces.get_nan_idx = np.array(nan_idx)
                    # if there is any empty assignment, fill the dimension with nan
                    for i in nan_idx:
                        forces = np.insert(forces, i, np.nan, axis=1)
                    print(f'\t{itrial.stem} (NaNs: {nan_idx})')
                else:
                    print(f'\t{itrial.stem}')

                # check if dimensions are ok
                if not forces.shape[1] == len(iassign):
                    raise ValueError('Wrong dimensions')
                break
            except IndexError:
                forces = []

        # check if there is empty frames
        nan_rows = np.isnan(forces).any(axis=1).ravel()
        print(f'\t\tremoving {nan_rows.sum()} nan frames (indices: {np.argwhere(nan_rows)})')
        forces = forces[..., ~nan_rows]

        # processing (offset during the first second, calibration, )
        forces = forces \
            .center(mu=np.nanmedian(forces[..., 10:int(forces.get_rate)], axis=-1), axis=-1) \
            .squeeze().T.matmul(calibration_matrix.T) \
            .low_pass(freq=forces.get_rate, order=params['order'], cutoff=params['low_pass_cutoff']) \
            .dot(-1)

        norm = Analogs3dOsim(forces[0, :3, :].norm(axis=0).reshape(1, 1, -1))
        idx = norm[0, 0, :].detect_onset(
            threshold=5,  # 5 Newtons
            above=int(forces.get_rate) / 2,
            below=1000,
        )

        # Special cases
        if itrial.stem == 'MarSF12H4_1':
            idx[0][1] = 11983
        if itrial.stem == 'MarSF6H4_1':
            idx[0][1] = 10672
        if itrial.stem == 'GatBH18H4_2':
            idx[0][1] = 17122
        if itrial.stem == 'GatBH18H4_2':
            idx[0][1] = 17122
        if itrial.stem == 'GatBH18H4_3':
            idx = idx[0][None]
            idx[0][0] = 5271
            idx[0][1] = 15965

        if idx.shape[0] > 1:
            raise ValueError('more than one onset')

        ten_percents = int(forces.shape[-1] * 0.1)
        if idx[0][0] < ten_percents:
            raise ValueError(f'onset is less than 10% of the trial ({idx[0][0] / forces.shape[-1] * 100:2f}%)')

        ninety_percents = int(forces.shape[-1] * 0.97)
        if idx[0][1] > ninety_percents:
            raise ValueError(f'onset is less than 90% of the trial ({idx[0][1] / forces.shape[-1] * 100:.2f}%)')

        _, ax = plt.subplots(nrows=1, ncols=1)
        norm.plot(ax=ax)

        for (inf, sup) in idx:
            ax.axvline(x=inf, color='g', lw=2, ls='--')
            ax.axvline(x=sup, color='r', lw=2, ls='--')
        # plt.show()

        forces.get_labels = params['forces_labels']
        sto_filename = f"{PROJECT_PATH / iparticipant / '0_forces' / itrial.stem}.sto"

        forces.to_sto(filename=sto_filename)

        # add onset & offset in configuration
        onset = idx[0][0] / forces.get_rate
        offset = idx[0][1] / forces.get_rate
        conf.add_conf_field({
            iparticipant: {'onset': {itrial.stem: [onset, offset]}}
        })
