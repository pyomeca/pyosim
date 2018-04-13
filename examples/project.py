import shutil
from pathlib import Path

from pyosim.project import Project

DATA_PATH = Path('../tests/data')
PROJECT_PATH = DATA_PATH / 'project_sample'
CONF_TEMPLATE = DATA_PATH / '_conf.csv'

# remove project if already exists
if PROJECT_PATH.is_dir():
    shutil.rmtree(PROJECT_PATH)

# create Project object
project = Project(path=PROJECT_PATH)

# create project directory
project.create_project()

# add two participants from the template conf file
shutil.copy(CONF_TEMPLATE, PROJECT_PATH)
project.update_participants()
