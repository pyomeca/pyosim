"""
Example: create a project.
"""

import shutil
from pathlib import Path
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
