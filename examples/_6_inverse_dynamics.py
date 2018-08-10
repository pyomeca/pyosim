"""
Example: run inverse dynamic and export sto
"""

from pathlib import Path

from pyosim import Conf
from pyosim import InverseDynamics
from project_conf import PROJECT_PATH, TEMPLATES_PATH


model_names = ['wu']  #, 'das']

conf = Conf(project_path=PROJECT_PATH)
conf.check_confs()

participants = conf.get_participants_to_process()

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')

    # ignore some trials
    blacklist_suffix = '0'
    trials = [ifile for ifile in (PROJECT_PATH / iparticipant / '1_inverse_kinematic').glob('*.mot') if
              not ifile.stem.endswith(blacklist_suffix)]

    for imodel in model_names:
        path_kwargs = {
            'model_input': f"{PROJECT_PATH / iparticipant / '_models' / imodel}_scaled_markers.osim",
            'xml_input': f'{TEMPLATES_PATH / imodel}_id.xml',
            'xml_output': f"{PROJECT_PATH / iparticipant / '_xml' / imodel}_id.xml",
            'xml_forces': f'{TEMPLATES_PATH}/forces_sensor.xml',
            'forces_dir': f"{PROJECT_PATH / iparticipant / '0_forces'}",
            'sto_output': f"{(PROJECT_PATH / iparticipant / '2_inverse_dynamic').resolve()}",
        }

        InverseDynamics(
            **path_kwargs,
            mot_files=trials,
            prefix=imodel,
            low_pass=10,
            multi=True
        )
