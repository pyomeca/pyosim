"""
Analyze tool class in pyosim.
Used in static optimization, muscle analysis and joint reaction analysis.
"""
from pathlib import Path

import opensim as osim


class AnalyzeTool:
    """
    Analyze tool in pyosim.
    Used in static optimization, muscle analysis and joint reaction analysis.

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
    >>> from pyosim import AnalyzeTool
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
    >>>     'xml_input': f"{(TEMPLATES_PATH / model).resolve()}_so.xml",
    >>>     'xml_output': f"{(PROJECT_PATH / participant / '_xml' / model).resolve()}_so.xml",
    >>>     'xml_forces': f"{(TEMPLATES_PATH / 'forces_sensor.xml').resolve()}",
    >>>     'xml_actuators': f"{(TEMPLATES_PATH / f'{model}_actuators.xml').resolve()}",
    >>>     'ext_forces_dir': f"{(PROJECT_PATH / participant / '0_forces').resolve()}",
    >>>     'muscle_forces_dir': f"{(PROJECT_PATH / participant / '3_static_optimization').resolve()}",
    >>>     'sto_output': f"{(PROJECT_PATH / participant / '3_static_optimization').resolve()}",
    >>> }
    >>>
    >>> AnalyzeTool(
    >>>     **path_kwargs,
    >>>     mot_files=trials,
    >>>     prefix=model,
    >>>     low_pass=5
    >>> )
    """

    def __init__(
            self,
            model_input,
            xml_input,
            xml_output,
            sto_output,
            mot_files,
            xml_forces=None,
            ext_forces_dir=None,
            muscle_forces_dir=None,
            xml_actuators=None,
            prefix=None,
            low_pass=None,
            remove_empty_files=False
    ):
        self.model_input = model_input
        self.xml_input = xml_input
        self.xml_output = xml_output
        self.sto_output = sto_output
        self.xml_forces = xml_forces
        self.ext_forces_dir = ext_forces_dir
        self.muscle_forces_dir = muscle_forces_dir
        self.xml_actuators = xml_actuators
        self.prefix = prefix
        self.low_pass = low_pass
        self.remove_empty_files = remove_empty_files

        if not isinstance(mot_files, list):
            self.mot_files = [mot_files]
        else:
            self.mot_files = mot_files

        if not isinstance(self.mot_files[0], Path):
            self.mot_files = [Path(i) for i in self.mot_files]

        self.run_analyze_tool()

    def run_analyze_tool(self):
        for ifile in self.mot_files:
            if self.prefix and not ifile.stem.startswith(self.prefix):
                # skip file if user specified a prefix and prefix is not present in current file
                pass
            else:
                print(f'\t{ifile.stem}')

                analyze_tool = osim.AnalyzeTool(self.xml_input, False)

                model = osim.Model(self.model_input)
                analyze_tool.setModel(model)
                analyze_tool.setModelFilename(model.getDocumentFileName())

                if self.xml_actuators:
                    force_set = osim.ArrayStr()
                    force_set.append(self.xml_actuators)
                    analyze_tool.setForceSetFiles(force_set)
                    analyze_tool.updateModelForces(model, self.xml_actuators)

                # get starting and ending time
                motion = osim.Storage(f'{ifile.resolve()}')
                start = motion.getFirstTime()
                end = motion.getLastTime()

                analyze_tool.setInitialTime(start)
                analyze_tool.setFinalTime(end)

                analyze_tool.getAnalysisSet().get(0).setStartTime(start)
                analyze_tool.getAnalysisSet().get(0).setEndTime(end)

                analyze_tool.setCoordinatesFileName(f'{ifile.resolve()}')

                # external loads file
                if self.xml_forces:
                    loads = osim.ExternalLoads(model, self.xml_forces)
                    if self.prefix:
                        loads.setDataFileName(
                            f"{Path(self.ext_forces_dir, ifile.stem.replace(f'{self.prefix}_', '')).resolve()}.sto"
                        )
                    else:
                        loads.setDataFileName(
                            f"{Path(self.ext_forces_dir, ifile.stem).resolve()}.sto"
                        )
                    loads.setExternalLoadsModelKinematicsFileName(f'{ifile.resolve()}')
                    temp_xml = Path('temp.xml')
                    loads.printToXML(f'{temp_xml.resolve()}')  # temporary xml file
                    analyze_tool.setExternalLoadsFileName(f'{temp_xml}')

                if self.muscle_forces_dir:
                    temp_2_xml = Path('temp_2.xml')
                    analyze_tool.printToXML(f'{temp_2_xml.resolve()}')
                    # temporary hack: edit xml to set force_file
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(f'{temp_2_xml.resolve()}')
                    root = tree.getroot()
                    attr = root.find("./AnalyzeTool/AnalysisSet/objects/JointReaction/forces_file")
                    attr.text = f"{Path(self.muscle_forces_dir, ifile.stem).resolve()}_StaticOptimization_force.sto"
                    tree.write(f'{temp_2_xml.resolve()}')
                    analyze_tool = osim.AnalyzeTool(f'{temp_2_xml.resolve()}', False)

                    model = osim.Model(self.model_input)
                    analyze_tool.setModel(model)
                    analyze_tool.setModelFilename(model.getDocumentFileName())
                    temp_2_xml.unlink()

                if self.low_pass:
                    analyze_tool.setLowpassCutoffFrequency(self.low_pass)

                state = model.initSystem()
                analyze_tool.setStatesFromMotion(state, motion, True)

                # set name of input (mot) file and output (sto)
                analyze_tool.setName(f'{ifile.stem}')

                analyze_tool.setResultsDir(f'{self.sto_output}')

                analyze_tool.printToXML(self.xml_output)

                analyze_tool.run()
                temp_xml.unlink()  # delete temporary xml file

                if self.remove_empty_files:
                    self._remove_empty_files(directory=self.sto_output)

    @staticmethod
    def _remove_empty_files(directory, threshold=1000):
        """
        Remove empty files from a directory.

        Parameters
        ----------
        directory : str, Path
            directory
        threshold : int
            threshold in bytes
        """
        for ifile in Path(directory).iterdir():
            if ifile.stat().st_size < threshold:
                ifile.unlink()
