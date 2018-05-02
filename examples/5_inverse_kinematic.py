"""
Example: run inverse kinematic and export mot
"""

from pathlib import Path

from pyosim import Conf

# path
PROJECT_PATH = Path('../Misc/project_sample')
MODELS_PATH = PROJECT_PATH / '_models'
TEMPLATES_PATH = PROJECT_PATH / '_templates'

model_names = ['wu', 'das']

conf = Conf(project_path=PROJECT_PATH)

participants = conf.get_participants_to_process()
participants = ['dapo']

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')

    for imodel in model_names:
        model_path = f'{MODELS_PATH / imodel}_scaled_markers.osim'