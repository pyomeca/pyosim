"""
Inverse kinematic class in pyosim
"""
from pathlib import Path

import opensim as osim


class IK:
    def __init__(self, model_input, xml_input, xml_output, trc, mot_output, onsets=None, prefix=None):
        self.model = osim.Model(model_input)
        self.mot_output = mot_output
        self.onsets = onsets
        self.xml_output = xml_output
        if prefix:
            self.prefix = prefix

        if not isinstance(trc, list):
            self.trc = [trc]
        else:
            self.trc = trc

        if not isinstance(self.trc[0], Path):
            self.trc = [Path(i) for i in self.trc]

        # initialize inverse kinematic tool from setup file
        self.ik_tool = osim.InverseKinematicsTool(xml_input)
        self.ik_tool.setModel(self.model)

        self.run_ik_tool()

    def run_ik_tool(self):
        for ifile in self.trc:
            print(f'\t{ifile.stem}')

            # set name of input (trc) file and output (mot)
            if self.prefix:
                filename = f"{self.prefix}_{ifile.stem}"
            else:
                filename = ifile.stem
            self.ik_tool.setName(filename)
            self.ik_tool.setMarkerDataFileName(f'{ifile}')
            self.ik_tool.setOutputMotionFileName(f"{Path(self.mot_output) / filename}.mot")
            self.ik_tool.setResultsDir(self.mot_output)

            if ifile.stem in self.onsets:
                # set start and end times from configuration file
                start = self.onsets[ifile.stem][0]
                end = self.onsets[ifile.stem][1]
            else:
                # use the trc file to get the start and end times
                m = osim.MarkerData(f'{ifile}')
                start = m.getStartFrameTime()
                end = m.getLastFrameTime() - 1e-2  # -1e-2 because remove last frame resolves some bug
            self.ik_tool.setStartTime(start)
            self.ik_tool.setEndTime(end)

            self.ik_tool.printToXML(self.xml_output)
            self.ik_tool.run()
