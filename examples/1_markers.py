"""
Example: export markers to trc
"""

from pathlib import Path

from pyosim.conf import Conf
from pyosim.obj.markers import Markers3dOsim

# path
PROJECT_PATH = Path('../Misc/project_sample')

conf = Conf(project_path=PROJECT_PATH)

PARTICIPANTS = ['dapo']

for iparticipant in PARTICIPANTS:

    print(f'\nparticipant: {iparticipant}')
    directories = conf.get_conf_field(participant=iparticipant, field=['markers', 'data'])
    assigned = conf.get_conf_field(participant=iparticipant, field=['markers', 'assigned'])

    for idir in directories:
        print(f'\n\tdirectory: {idir}')

        for itrial in Path(idir).glob('*.c3d'):
            print(f'\t\ttrial: {itrial.parts[-1]}')
            # try participant's channel assignment
            for iassign in assigned:
                # particular case: delete box if SCoRE trials
                if Path(idir).parts[-1] == 'MODEL2':
                    iassign = iassign[:-8]
                try:
                    markers = Markers3dOsim.from_c3d(itrial, names=iassign, prefix=':')
                    break
                except:
                    markers = []

            trc_filename = PROJECT_PATH / iparticipant / '0_markers' / itrial.parts[-1].replace('c3d', 'trc')
            markers.to_trc(file_name=trc_filename)
