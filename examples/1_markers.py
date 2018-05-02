"""
Example: export markers to trc
"""

from pathlib import Path

import numpy as np

from pyosim import Conf
from pyosim.obj import Markers3dOsim

# path
PROJECT_PATH = Path('../Misc/project_sample')

conf = Conf(project_path=PROJECT_PATH)

markers_labels = conf.get_conf_field(participant='dapo', field=['markers', 'targets'])

participants = conf.get_participants_to_process()
participants = participants[13:]

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')
    directories = conf.get_conf_field(participant=iparticipant, field=['markers', 'data'])
    assigned = conf.get_conf_field(participant=iparticipant, field=['markers', 'assigned'])

    for idir in directories:
        print(f'\n\tdirectory: {idir}')

        for itrial in Path(idir).glob('*.c3d'):
            # try participant's channel assignment
            for iassign in assigned:

                # delete some markers if particular trials (box markers during score)
                if Path(idir).parts[-1] == 'MODEL2':
                    iassign = iassign[:-8]
                    labels = markers_labels[:-8]
                else:
                    labels = markers_labels

                nan_idx = [i for i, v in enumerate(iassign) if not v]
                if nan_idx:
                    iassign_without_nans = [i for i in iassign if i]
                else:
                    iassign_without_nans = iassign

                try:
                    markers = Markers3dOsim.from_c3d(itrial, names=iassign_without_nans, prefix=':')
                    if nan_idx:
                        # if there is any empty assignment, fill the dimension with nan
                        for i in nan_idx:
                            markers = np.insert(markers, i, np.nan, axis=1)
                        print(f'\t{itrial.parts[-1]} (NaNs: {nan_idx})')
                    else:
                        print(f'\t{itrial.parts[-1]}')

                    # check if dimensions are ok
                    if not markers.shape[1] == len(iassign):
                        raise ValueError('Wrong dimensions')
                    break
                except IndexError:
                    markers = []

            markers.get_labels = labels
            trc_filename = PROJECT_PATH / iparticipant / '0_markers' / itrial.parts[-1].replace('c3d', 'trc')
            markers.to_trc(filename=trc_filename)
