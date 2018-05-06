"""
Example: run inverse dynamic and export sto
"""

from pathlib import Path

from pyosim import Conf
from pyosim import ID

# path
PROJECT_PATH = Path('../Misc/project_sample')
TEMPLATES_PATH = PROJECT_PATH / '_templates'

model_names = ['wu', 'das']
offset = 0.05  # take 1 second before and after onsets

conf = Conf(project_path=PROJECT_PATH)

# participants = conf.get_participants_to_process()
participants = ['dapo']

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')

    # ignore some trials
    blacklist_suffix = '0'

    trials = [ifile for ifile in (PROJECT_PATH / iparticipant / '1_inverse_kinematic').glob('*.mot') if
              not ifile.stem.endswith(blacklist_suffix)]
    onsets = conf.get_conf_field(iparticipant, ['onset'])
    onsets = {key: [values[0] - offset, values[1] + offset] for key, values in onsets.items()}

    for imodel in model_names:
        idyn = ID(
            model_input=f"{PROJECT_PATH / iparticipant / '_models' / imodel}_scaled_markers.osim",
            xml_input=f'{TEMPLATES_PATH / imodel}_ik.xml',
            xml_output=f"{PROJECT_PATH / iparticipant / '_xml' / imodel}_ik.xml",
            xml_forces=f'{TEMPLATES_PATH}/forces_sensor.xml',
            forces_dir=f"{PROJECT_PATH / iparticipant / '0_forces'}",
            mot_files=trials,
            sto_output=f"{(PROJECT_PATH / iparticipant / '2_inverse_dynamic').resolve()}",
            prefix=imodel,
            low_pass=10
        )
