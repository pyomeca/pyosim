"""
Example: run inverse kinematic and export mot
"""

from pathlib import Path

from pyosim import Conf
from pyosim import IK

# path
PROJECT_PATH = Path('../Misc/project_sample')
TEMPLATES_PATH = PROJECT_PATH / '_templates'

model_names = ['wu', 'das']
offset = 0.05  # take 1 second before and after onsets

conf = Conf(project_path=PROJECT_PATH)

# participants = conf.get_participants_to_process()
participants = ['dapo']  # launch yosc

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')

    trials = [ifile for ifile in (PROJECT_PATH / iparticipant / '0_markers').glob('*.trc')]
    onsets = conf.get_conf_field(iparticipant, ['onset'])
    onsets = {key: [values[0] - offset, values[1] + offset] for key, values in onsets.items()}

    for imodel in model_names:
        ik = IK(
            model_input=f"{PROJECT_PATH / iparticipant / '_models' / imodel}_scaled_markers.osim",
            xml_input=f'{TEMPLATES_PATH / imodel}_ik.xml',
            xml_output=f"{PROJECT_PATH / iparticipant / '_xml' / imodel}_ik.xml",
            trc_files=trials,
            mot_output=f"{PROJECT_PATH / iparticipant / '1_inverse_kinematic'}",
            onsets=onsets,
            prefix=imodel
        )
