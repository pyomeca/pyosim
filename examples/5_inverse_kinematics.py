"""
Example: run inverse kinematic and export mot
"""

from pathlib import Path

from pyosim import Conf
from pyosim import InverseKinematics
from project_conf import PROJECT_PATH, WU_MASS_FACTOR, MODELS_PATH, TEMPLATES_PATH


model_names = ['wu']  #, 'das']
offset = 0.05  # take 1 second before and after onsets

conf = Conf(project_path=PROJECT_PATH)
conf.check_confs()

participants = conf.get_participants_to_process()

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')

    trials = [ifile for ifile in (PROJECT_PATH / iparticipant / '0_markers').glob('*.trc')]
    onsets = conf.get_conf_field(iparticipant, ['onset'])
    onsets = {key: [values[0] - offset, values[1] + offset] for key, values in onsets.items()}

    for imodel in model_names:
        path_kwargs = {
            'model_input': f"{PROJECT_PATH / iparticipant / '_models' / imodel}_scaled_markers.osim",
            'xml_input': f'{TEMPLATES_PATH / imodel}_ik.xml',
            'xml_output': f"{PROJECT_PATH / iparticipant / '_xml' / imodel}_ik.xml",
            'mot_output': f"{PROJECT_PATH / iparticipant / '1_inverse_kinematic'}",
        }

        InverseKinematics(
            **path_kwargs,
            trc_files=trials,
            onsets=onsets,
            prefix=imodel,
            multi=True
        )
