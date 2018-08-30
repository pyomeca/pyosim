"""
Inverse kinematic class in pyosim
"""
from pathlib import Path

import opensim as osim


class InverseKinematics:
    """
    Inverse kinematic in pyosim

    Parameters
    ----------
    model_input : str
        Path to the osim model
    xml_input : str
        Path to the generic ik xml
    xml_output : str
        Output path of the ik xml
    trc_files : str, list
        Path or list of path to the marker files (`.trc`)
    mot_output : str
        Output directory
    onsets : dict, optional
        Dictionary which contains the starting and ending point in second as values and trial name as keys
    prefix : str, optional
        Optional prefix to put in front of the output filename (typically model name)
    multi : bool, optional
        Launch InverseKinematics in multiprocessing if True

    Examples
    --------
    >>> from pathlib import Path
    >>>
    >>> from pyosim import Conf
    >>> from pyosim import InverseKinematics
    >>>
    >>> PROJECT_PATH = Path('../Misc/project_sample')
    >>> TEMPLATES_PATH = PROJECT_PATH / '_templates'
    >>>
    >>> participant = 'dapo'
    >>> model = 'wu'
    >>>
    >>> trials = [ifile for ifile in (PROJECT_PATH / participant / '0_markers').glob('*.trc')]
    >>> conf = Conf(project_path=PROJECT_PATH)
    >>> onsets = conf.get_conf_field(participant, ['onset'])
    >>>
    >>> ik = InverseKinematics(
    >>>     model_input=f"{PROJECT_PATH / participant / '_models' / model}_scaled_markers.osim",
    >>>     xml_input=f'{TEMPLATES_PATH / model}_ik.xml',
    >>>     xml_output=f"{PROJECT_PATH / participant / '_xml' / model}_ik.xml",
    >>>     trc_files=trials,
    >>>     mot_output=f"{PROJECT_PATH / participant / '1_inverse_kinematic'}",
    >>>     onsets=onsets,
    >>>     prefix=model
    >>> )
    """

    def __init__(
            self,
            model_input,
            xml_input,
            xml_output,
            trc_files,
            mot_output,
            onsets=None,
            prefix=None,
            multi=False
    ):
        self.model_input = model_input
        self.mot_output = mot_output
        self.onsets = onsets
        self.xml_input = xml_input
        self.xml_output = xml_output
        self.multi = multi

        if prefix:
            self.prefix = prefix

        if not isinstance(trc_files, list):
            self.trc_files = [trc_files]
        else:
            self.trc_files = trc_files

        if not isinstance(self.trc_files[0], Path):
            self.trc_files = [Path(i) for i in self.trc_files]

        self.main_loop()

    def main_loop(self):
        if self.multi:
            import os
            from multiprocessing import Pool

            pool = Pool(os.cpu_count()-1)
            pool.map(self.run_ik_tool, self.trc_files)
        else:
            for itrial in self.trc_files:
                self.run_ik_tool(itrial)

    def run_ik_tool(self, trial):
        model = osim.Model(self.model_input)
        # initialize inverse kinematic tool from setup file
        ik_tool = osim.InverseKinematicsTool(self.xml_input)
        ik_tool.setModel(model)

        print(f'\t{trial.stem}')
        # initialize inverse kinematic tool from setup file
        ik_tool = osim.InverseKinematicsTool(self.xml_input)
        ik_tool.setModel(model)

        # set name of input (trc) file and output (mot)
        if self.prefix:
            filename = f"{self.prefix}_{trial.stem}"
        else:
            filename = trial.stem
        ik_tool.setName(filename)
        ik_tool.setMarkerDataFileName(f'{trial}')
        ik_tool.setOutputMotionFileName(f"{Path(self.mot_output) / filename}.mot")
        ik_tool.setResultsDir(self.mot_output)

        if trial.stem in self.onsets:
            # set start and end times from configuration file
            start = self.onsets[trial.stem][0]
            end = self.onsets[trial.stem][1]
        else:
            # use the trc file to get the start and end times
            m = osim.MarkerData(f'{trial}')
            start = m.getStartFrameTime()
            end = m.getLastFrameTime() - 1e-2  # -1e-2 because removing last frame resolves some bug
        ik_tool.setStartTime(start)
        ik_tool.setEndTime(end)

        ik_tool.printToXML(self.xml_output)
        ik_tool.run()
