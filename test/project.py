import shutil
from pathlib import Path

from pyosim.project import Project

PROJECT_PATH = Path('./project_sample')
# remove project if already exist
if PROJECT_PATH.is_dir():
    shutil.rmtree(PROJECT_PATH)

# create Project object
project = Project(path=PROJECT_PATH)

# create project directory
project.create_project()

# add two participants from the template conf file
TEMPLATE_PATH = Path('./data/') / '_conf.csv'
shutil.copy(TEMPLATE_PATH, PROJECT_PATH)
project.update_participants()
