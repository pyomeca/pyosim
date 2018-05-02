"""
Example: export models
"""

from pathlib import Path

from pyosim import Conf
from pyosim import Scale

# path
PROJECT_PATH = Path('../Misc/project_sample')
MODELS_PATH = PROJECT_PATH / '_models'
TEMPLATES_PATH = PROJECT_PATH / '_templates'

model_names = ['wu', 'das']

conf = Conf(project_path=PROJECT_PATH)

participants = conf.get_participants_to_process()

for iparticipant in participants:
    print(f'\nparticipant: {iparticipant}')
    pseudo_in_path = iparticipant[0].upper() + iparticipant[1:-1] + iparticipant[-1].upper()
    static_path = f"{PROJECT_PATH / iparticipant / '0_markers' / 'IRSST_'}{pseudo_in_path}d0.trc"
    mass = conf.get_conf_field(iparticipant, ['mass'])
    height = conf.get_conf_field(iparticipant, ['height'])

    for imodel in model_names:
        model_path = f'{MODELS_PATH / imodel}.osim'

        scaling = Scale(
            model_input=model_path,
            model_output=f"{PROJECT_PATH / iparticipant / '_models' / imodel}_scaled.osim",
            xml_input=f'{TEMPLATES_PATH / imodel}_scaling.xml',
            xml_output=f"{PROJECT_PATH / iparticipant / '_xml' / imodel}_scaled.xml",
            static_path=static_path,
            mass=mass,
            height=height * 10
        )

        # TODO: get total squared error + marker error + max
