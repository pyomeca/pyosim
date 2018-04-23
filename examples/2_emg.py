"""
Example: export emg to sto
"""

from pathlib import Path

from pyosim.conf import Conf
from pyosim.obj.analogs import Analogs3dOsim
import matplotlib.pyplot as plt

# path
PROJECT_PATH = Path('../Misc/project_sample')

conf = Conf(project_path=PROJECT_PATH)

PARTICIPANTS = ['dapo']

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
                try:
                    emg = Analogs3dOsim.from_c3d(itrial, names=iassign, prefix=':')

                    # processing
                    emg = emg \
                        .band_pass(freq=emg.get_rate, order=4, cutoff=[10, 425]) \
                        .center() \
                        .rectify() \
                        .low_pass(freq=emg.get_rate, order=4, cutoff=5) \
                        .normalization()

                    emg[0, :, :].T.plot()
                    plt.show()

                    print('')

                    break
                except:
                    emg = []

            sto_filename = PROJECT_PATH / iparticipant / '0_emg' / itrial.parts[-1].replace('c3d', 'trc')
            emg.to_sto(file_name=sto_filename)
