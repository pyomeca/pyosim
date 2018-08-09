"""
Example: run static optimization and export sto
"""

from pathlib import Path

from pyosim import Conf
from pyosim import StaticOptimization
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
            'model_input': f"{(PROJECT_PATH / iparticipant / '_models' / imodel).resolve()}_scaled_markers.osim",
            'xml_input': f"{(TEMPLATES_PATH / imodel).resolve()}_so.xml",
            'xml_output': f"{(PROJECT_PATH / iparticipant / '_xml' / imodel).resolve()}_so.xml",
            'xml_forces': f"{(TEMPLATES_PATH / 'forces_sensor.xml').resolve()}",
            'xml_actuators': f"{(TEMPLATES_PATH / f'{imodel}_actuators.xml').resolve()}",
            'ext_forces_dir': f"{(PROJECT_PATH / iparticipant / '0_forces').resolve()}",
            'sto_output': f"{(PROJECT_PATH / iparticipant / '3_static_optimization').resolve()}",
            'enforce_analysis': True
        }

        StaticOptimization(
            **path_kwargs,
            mot_files=trials,
            prefix=imodel,
            low_pass=5,
            multi=True
        )
