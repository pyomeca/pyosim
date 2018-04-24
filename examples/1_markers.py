"""
Example: export markers to trc
"""

from pathlib import Path

import numpy as np

from pyosim.conf import Conf
from pyosim.obj.markers import Markers3dOsim

# path
PROJECT_PATH = Path('../Misc/project_sample')

conf = Conf(project_path=PROJECT_PATH)

participants = conf.get_participants_to_process()

participants = participants[55:]
'/media/romain/F/Data/Shoulder/RAW/IRSST_AmiAd/MODEL2/IRSST_AmiAd6.c3d'
for iparticipant in participants:

    print(f'\nparticipant: {iparticipant}')
    directories = conf.get_conf_field(participant=iparticipant, field=['markers', 'data'])
    assigned = conf.get_conf_field(participant=iparticipant, field=['markers', 'assigned'])

    for idir in directories:
        print(f'\n\tdirectory: {idir}')

        for itrial in Path(idir).glob('*.c3d'):
            print(f'\t\ttrial: {itrial.parts[-1]}')
            # try participant's channel assignment
            for iassign in assigned:
                # delete some markers if particular trials (box markers during score)
                if Path(idir).parts[-1] == 'MODEL2':
                    iassign = iassign[:-8]
                try:
                    # get index where assignment are empty
                    nan_idx = [i for i, v in enumerate(iassign) if not v]

                    if nan_idx:
                        iassign_without_nans = [i for i in iassign if i]
                        markers = Markers3dOsim.from_c3d(itrial, names=iassign_without_nans, prefix=':')

                        # append nan dimensions
                        for i in nan_idx:
                            markers = np.insert(markers, i, np.nan, axis=1)
                        # check if nan dimension are correctly inserted
                        n = np.isnan(markers).sum(axis=2).ravel()
                        if not np.array_equal(n.argsort()[-len(nan_idx):], nan_idx):
                            raise ValueError('NaN dimensions misplaced')
                    else:
                        iassign_without_nans = iassign
                        markers = Markers3dOsim.from_c3d(itrial, names=iassign_without_nans, prefix=':')

                    # check if dimensions are ok
                    if not markers.shape[1] == len(iassign):
                        raise ValueError('Wrong dimension')

                    break
                except IndexError:
                    markers = []

            trc_filename = PROJECT_PATH / iparticipant / '0_markers' / itrial.parts[-1].replace('c3d', 'trc')
            markers.to_trc(file_name=trc_filename)
