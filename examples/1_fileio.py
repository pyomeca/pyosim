"""
Example: Create configuration files and export data for each participants
"""

from pathlib import Path

from pyosim.conf import Conf as pyoconf

PROJECT_PATH = Path('../Misc/project_sample')

# Create a Conf object
project = pyoconf(project_path=PROJECT_PATH)

# Check if all participants have a configuration file and update it in the project's configuration file
project.check_confs()

# add some data path in participants' conf file
d = {
    'dapo': {'data': '/home/romain/Downloads/conf-files/DapO/mvc'},
    'davo': {'data': '/home/romain/Downloads/conf-files/DavO/mvc'},
    'fabd': {'data': '/home/romain/Downloads/conf-files/FabD/mvc'}
}
project.add_conf_field(d)

# assign channel fields to targets fields
TARGETS = [
    'deltant', 'deltmed', 'deltpost', 'biceps', 'triceps', 'uptrap',
    'lotrap', 'serratus', 'ssp', 'isp', 'subs', 'pect', 'latissimus'
]
