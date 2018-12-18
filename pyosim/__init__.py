from .scale import *
from .project import *
from .model import *
from .conf import *
from .inverse_kinematics import *
from .inverse_dynamics import *
from .analyse_tool import *
from .static_optimization import *
from .muscle_analysis import *
from .joint_reaction import *

__author__ = "Romain Martinez"

__version__ = '0.1.0'

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
