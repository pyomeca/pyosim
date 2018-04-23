"""
Example: create a project.
"""

import shutil
from pathlib import Path

from pyomeca.gui import FieldsAssignment
from pyosim.conf import Conf
from pyosim.project import Project

# path
PROJECT_PATH = Path('../Misc/project_sample')
CONF_TEMPLATE = Path('../tests/_conf.csv')

# remove project if already exists (you don't need to do this)
if PROJECT_PATH.is_dir():
    shutil.rmtree(PROJECT_PATH)

# create Project object
project = Project(path=PROJECT_PATH)

# create project directory
project.create_project()

# add participants from the template conf file
shutil.copy(CONF_TEMPLATE, PROJECT_PATH)
project.update_participants()

# Create a Conf object
project = Conf(project_path=PROJECT_PATH)

# Check if all participants have a configuration file and update it in the project's configuration file
project.check_confs()

# add some data path in participants' conf file
d = {
    'dapo': {
        'emg': {'data': ['/media/romain/F/Data/Shoulder/RAW/IRSST_DapOd/trials',
                         '/media/romain/F/Data/Shoulder/RAW/IRSST_DapOd/MODEL2',
                         '/media/romain/E/Projet_MVC/data/DataLandryD4/DapO']},
        'analogs': {'data': '/media/romain/F/Data/Shoulder/RAW/IRSST_DapOd/trials'},
        'markers': {'data': ['/media/romain/F/Data/Shoulder/RAW/IRSST_DapOd/trials',
                             '/media/romain/F/Data/Shoulder/RAW/IRSST_DapOd/MODEL2']}
    }
}

project.add_conf_field(d)

# assign channel fields to targets fields
TARGETS = {
    'emg': ['deltant', 'deltmed', 'deltpost', 'biceps', 'triceps', 'uptrap', 'lotrap',
            'serratus', 'ssp', 'isp', 'subs', 'pect', 'latissimus'],
    'analogs': ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']
}
for ikind, itarget in TARGETS.items():
    for iparticipant in ['dapo']:
        fields = FieldsAssignment(
            directory=project.get_conf_field(iparticipant, field=[ikind, 'data']),
            targets=itarget,
            kind=ikind
        )
        project.add_conf_field({iparticipant: fields.output})
