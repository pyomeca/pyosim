"""
Joint reaction class in pyosim
"""
from pyosim import AnalyzeTool


class JointReaction(AnalyzeTool):
    """
    Static Optimization in pyosim

    Parameters
    ----------
    model_input : str
        Path to the osim model
    xml_input : str
        Path to the generic so xml
    xml_output : str
        Output path of the so xml
    xml_forces : str, optional
        Path to the generic forces sensor xml (Optional)
    ext_forces_dir : str, optional
        Path of the directory containing the external forces files (`.sto`) (Optional)
    muscle_forces_dir : str, optional
        Path of the directory containing the muscle forces files (`.sto`) (Optional)
    mot_files : str, Path, list
        Path or list of path to the directory containing the motion files (`.mot`)
    sto_output : Path, str
        Output directory
    xml_actuators: Path, str
        Actuators (Optional)
    prefix : str, optional
        Optional prefix to put in front of the output filename (typically model name) (Optional)
    low_pass : int, optional
        Cutoff frequency for an optional low pass filter on coordinates (Optional)
    remove_empty_files : bool, optional
        remove empty files i in `sto_output` if True (Optional)

    Examples
    --------
    >>> from pathlib import Path
    >>>
    >>> from pyosim import MuscleAnalysis
    >>>
    >>> PROJECT_PATH = Path('../Misc/project_sample')
    >>> TEMPLATES_PATH = PROJECT_PATH / '_templates'
    >>>
    >>> participant = 'dapo'
    >>> model = 'wu'
    >>> trials = [ifile for ifile in (PROJECT_PATH / participant / '1_inverse_kinematic').glob('*.mot')]
    >>>
    >>> path_kwargs = {
    >>>     'model_input': f"{(PROJECT_PATH / participant / '_models' / model).resolve()}_scaled_markers.osim",
    >>>     'xml_input': f"{(TEMPLATES_PATH / model).resolve()}_ma.xml",
    >>>     'xml_output': f"{(PROJECT_PATH / participant / '_xml' / model).resolve()}_ma.xml",
    >>>     'xml_forces': f"{(TEMPLATES_PATH / 'forces_sensor.xml').resolve()}",
    >>>     'xml_actuators': f"{(TEMPLATES_PATH / f'{model}_actuators.xml').resolve()}",
    >>>     'forces_dir': f"{(PROJECT_PATH / participant / '0_forces').resolve()}",
    >>>     'sto_output': f"{(PROJECT_PATH / participant / '4_muscle_analysis').resolve()}",
    >>> }
    >>>
    >>> MuscleAnalysis(
    >>>     **path_kwargs,
    >>>     mot_files=trials,
    >>>     prefix=model,
    >>>     low_pass=5,
    >>>     remove_empty_files=True
    >>> )
    """
    pass
