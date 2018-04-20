"""
Example: Create configuration files and export data for each participants
"""

from pathlib import Path

from pyosim.obj.conf import Conf as pyoconf

PROJECT_PATH = Path('../Misc/project_sample')

# Create a Conf object
project = pyoconf(project_path=PROJECT_PATH)

# Check if all participants have a configuration file and update it in the project's configuration file
project.check_confs()

# add data path in participants' conf file


