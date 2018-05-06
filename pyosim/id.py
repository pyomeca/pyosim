"""
Inverse dynamic class in pyosim
"""
from pathlib import Path

import opensim as osim


class ID:
    """
    Inverse dynamic in pyosim

    Parameters
    ----------
    model_input : str
        Path to the osim model
    xml_input : str
        Path to the generic ik xml
    xml_output : str
        Output path of the ik xml
    xml_forces : str
        Path to the generic forces sensor xml
    forces_dir : str
        Path of the directory containing the forces files (`.sto`)
    mot_files : str, Path, list
        Path or list of path to the directory containing the motion files (`.mot`)
    sto_output : Path, str
        Output directory
    prefix : str, optional
        Optional prefix to put in front of the output filename (typically model name)
    low_pass : int, optional
        Cutoff frequency for an optional low pass filter on coordinates

    Examples
    --------
    >>> from pyosim import Conf
    >>> from pyosim import ID
    >>> participant = 'dapo'
    >>> model = 'wu'
    >>> PROJECT_PATH = Path('../Misc/project_sample')

    >>> trials = [ifile for ifile in (PROJECT_PATH / iparticipant / '1_inverse_kinematic').glob('*.mot')]
    >>> conf = Conf(project_path=PROJECT_PATH)
    >>> onsets = conf.get_conf_field(participant, ['onset'])

    >>> idyn = ID(
    >>>         model_input=f"{PROJECT_PATH / iparticipant / '_models' / imodel}_scaled_markers.osim",
    >>>         xml_input=f'{TEMPLATES_PATH / imodel}_ik.xml',
    >>>         xml_output=f"{PROJECT_PATH / iparticipant / '_xml' / imodel}_ik.xml",
    >>>         xml_forces=f'{TEMPLATES_PATH}/forces_sensor.xml',
    >>>         forces_dir=f"{PROJECT_PATH / iparticipant / '0_forces'}",
    >>>         mot_files=trials,
    >>>         sto_output=f"{(PROJECT_PATH / iparticipant / '2_inverse_dynamic').resolve()}",
    >>>         prefix=imodel,
    >>>         low_pass=10
    >>>     )
    """

    def __init__(self, model_input, xml_input, xml_output, xml_forces, forces_dir, mot_files, sto_output, prefix=None,
                 low_pass=None):
        self.model_input = model_input
        self.sto_output = sto_output
        self.xml_input = xml_input
        self.xml_output = xml_output
        self.xml_forces = xml_forces
        self.forces_dir = forces_dir
        self.low_pass = low_pass

        if prefix:
            self.prefix = prefix

        if not isinstance(mot_files, list):
            self.mot_files = [mot_files]
        else:
            self.mot_files = mot_files

        if not isinstance(self.mot_files[0], Path):
            self.mot_files = [Path(i) for i in self.mot_files]

        self.run_id_tool()

    def run_id_tool(self):
        for ifile in self.mot_files:
            if self.prefix and not ifile.stem.startswith(self.prefix):
                # skip file if user specified a prefix and prefix is not present in current file
                pass
            else:
                print(f'\t{ifile.stem}')

                # initialize inverse dynamic tool from setup file
                model = osim.Model(self.model_input)
                id_tool = osim.InverseDynamicsTool(self.xml_input)
                id_tool.setModel(model)

                # get starting and ending time
                motion = osim.Storage(f'{ifile.resolve()}')
                start = motion.getFirstTime()
                end = motion.getLastTime()

                # external load file
                loads = osim.ExternalLoads(model, self.xml_forces)
                if self.prefix:
                    loads.setDataFileName(
                        f"{Path(self.forces_dir, ifile.stem.replace(f'{self.prefix}_', '')).resolve()}.sto"
                    )
                else:
                    loads.setDataFileName(
                        f"{Path(self.forces_dir, ifile.stem).resolve()}.sto"
                    )
                loads.setExternalLoadsModelKinematicsFileName(f'{ifile.resolve()}')

                temp_xml = Path('temp.xml')
                loads.printToXML(f'{temp_xml.resolve()}')  # temporary xml file

                # inverse dynamics tool
                id_tool.setStartTime(start)
                id_tool.setEndTime(end)
                id_tool.setCoordinatesFileName(f'{ifile.resolve()}')
                id_tool.setExternalLoadsFileName(f'{temp_xml}')

                if self.low_pass:
                    id_tool.setLowpassCutoffFrequency(self.low_pass)

                # set name of input (mot) file and output (sto)
                filename = f'{ifile.stem}'
                id_tool.setName(filename)
                id_tool.setOutputGenForceFileName(f"{filename}.sto")
                id_tool.setResultsDir(f'{self.sto_output}')

                id_tool.run()
                temp_xml.unlink()  # delete temporary xml file
