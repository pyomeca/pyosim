"""
Scale class in pyosim
"""

import opensim as osim


class Scale:
    """
    Scale tool in pyosim

    Parameters
    ----------
    model_input : str
        Path to the generic model
    model_output : str
        Output path of the scaled model
    xml_input : str
        Path to the generic scaling xml
    xml_output : str
        Output path of the scaling xml
    static_path : str
        Path to the static trial (must be .trc)
    mass : double
        Participant's mass (kg)
    height : double
        Participant's height (mm)
    age : int
        Participant's age (year)
    add_model: str (optional)
        Append the specified model
    remove_unused : bool
        If unused markers have to be removed (default = True in OpenSim)

    Examples
    --------
    >>> from pathlib import Path
    >>>
    >>> from pyosim import Conf
    >>> from pyosim import Scale
    >>>
    >>> # path
    >>> PROJECT_PATH = Path('../Misc/project_sample')
    >>> MODELS_PATH = PROJECT_PATH / '_models'
    >>> TEMPLATES_PATH = PROJECT_PATH / '_templates'
    >>>
    >>> model = 'wu'
    >>> participant = 'dapo'
    >>> static_path = f"{PROJECT_PATH / participant / '0_markers' / 'IRSST_'}DapOd0.trc"
    >>>
    >>> conf = Conf(project_path=PROJECT_PATH)
    >>> mass = conf.get_conf_field(participant, ['mass'])
    >>> height = conf.get_conf_field(participant, ['height'])
    >>>
    >>>
    >>> path_kwargs = {
    >>>     'model_input': f'{MODELS_PATH / model}.osim',
    >>>     'model_output': f"{PROJECT_PATH / participant / '_models' / model}_scaled.osim",
    >>>     'xml_input': f'{TEMPLATES_PATH / model}_scaling.xml',
    >>>     'xml_output': f"{PROJECT_PATH / participant / '_xml' / model}_scaled.xml",
    >>>     'static_path': static_path
    >>> }
    >>>
    >>> Scale(
    >>>     **path_kwargs,
    >>>     mass=mass,
    >>>     height=height * 10,
    >>>     remove_unused=False
    >>> )
    """

    def __init__(
        self,
        model_input,
        model_output,
        xml_input,
        xml_output,
        static_path,
        mass=-1,
        height=-1,
        age=-1,
        add_model=None,
        remove_unused=True,
    ):
        self.model = osim.Model(model_input)
        self.model_output = model_output
        self.model_with_markers_output = model_output.replace(".osim", "_markers.osim")
        self.static_path = static_path
        self.xml_output = xml_output

        self.time_range = self.time_range_from_static()

        # initialize scale tool from setup file
        self.scale_tool = osim.ScaleTool(xml_input)
        self.set_anthropometry(mass, height, age)
        # Tell scale tool to use the loaded model
        self.scale_tool.getGenericModelMaker().setModelFileName(model_input)

        self.run_model_scaler(mass)
        self.run_marker_placer()

        if add_model:
            self.combine_models(add_model)

        if not remove_unused:
            self.add_unused_markers()

    def time_range_from_static(self):
        static = osim.MarkerData(self.static_path)
        initial_time = static.getStartFrameTime()
        final_time = static.getLastFrameTime()
        range_time = osim.ArrayDouble()
        range_time.set(0, initial_time)
        range_time.set(1, final_time)
        return range_time

    def set_anthropometry(self, mass, height, age):
        """
        Set basic anthropometric parameters in scaling model
        Parameters
        ----------
        mass : Double
            mass (kg)
        height : Double
            height (mm)
        age : int
            age (year)
        """
        self.scale_tool.setSubjectMass(mass)
        self.scale_tool.setSubjectHeight(height)
        self.scale_tool.setSubjectAge(age)

    def run_model_scaler(self, mass):
        model_scaler = self.scale_tool.getModelScaler()
        # Whether or not to use the model scaler during scale
        model_scaler.setApply(True)
        # Set the marker file to be used for scaling
        model_scaler.setMarkerFileName(self.static_path)

        # set time range
        model_scaler.setTimeRange(self.time_range)

        # Indicating whether or not to preserve relative mass between segments
        model_scaler.setPreserveMassDist(True)

        # Name of model file (.osim) to write when done scaling
        model_scaler.setOutputModelFileName(self.model_output)

        # Filename to write scale factors that were applied to the unscaled model (optional)
        model_scaler.setOutputScaleFileName(
            self.xml_output.replace(".xml", "_scaling_factor.xml")
        )

        model_scaler.processModel(self.model, "", mass)

    def run_marker_placer(self):
        # load a scaled model
        scaled_model = osim.Model(self.model_output)

        marker_placer = self.scale_tool.getMarkerPlacer()
        # Whether or not to use the model scaler during scale`
        marker_placer.setApply(True)
        marker_placer.setTimeRange(self.time_range)

        marker_placer.setStaticPoseFileName(self.static_path)

        # Name of model file (.osim) to write when done scaling
        marker_placer.setOutputModelFileName(self.model_with_markers_output)

        # Maximum amount of movement allowed in marker data when averaging
        marker_placer.setMaxMarkerMovement(-1)

        marker_placer.processModel(scaled_model)
        
        # save processed model
        scaled_model.printToXML(self.model_output)

        # print scale config to xml
        self.scale_tool.printToXML(self.xml_output)

    def add_unused_markers(self):
        with_unused = osim.Model(self.model_output)
        without_unused = osim.Model(self.model_with_markers_output)

        with_unused_markerset = with_unused.getMarkerSet()
        without_unused_markerset = without_unused.getMarkerSet()

        with_unused_l = [
            with_unused_markerset.get(imarker).getName()
            for imarker in range(with_unused.getNumMarkers())
        ]
        without_unused_l = [
            without_unused_markerset.get(imarker).getName()
            for imarker in range(without_unused.getNumMarkers())
        ]

        differences = set(with_unused_l).difference(without_unused_l)

        for idiff in differences:
            m = with_unused_markerset.get(idiff).clone()
            without_unused.addMarker(m)

        without_unused.printToXML(self.model_with_markers_output)

    def combine_models(self, model_to_add):
        # Open the models
        osim_base = osim.Model(self.model_output)
        osim_to_add = osim.Model(model_to_add)

        bodies = osim_to_add.getBodySet()
        joints = osim_to_add.getJointSet()
        controls = osim_to_add.getControllerSet()
        constraints = osim_to_add.getConstraintSet()
        markers = osim_to_add.getMarkerSet()

        print("Add bodies:")
        for body in bodies:
            print(f"\t{body.getName()}")
            osim_base.addBody(body.clone())

        print("Add joints:")
        for joint in joints:
            print(f"\t{joint.getName()}")
            osim_base.addJoint(joint.clone())

        print("Add controls:")
        for control in controls:
            print(f"\t{control.getName()}")
            osim_base.addControl(control.clone())

        print("Add constraints:")
        for constraint in constraints:
            print(f"\t{constraint.getName()}")
            osim_base.addConstraint(constraint.clone())

        print("Add markers")
        for marker in markers:
            print(f"\t{marker.getName()}")
            osim_base.addMarker(marker.clone())

        osim_base.initSystem()

        osim_base.printToXML(self.model_with_markers_output)
        print(f"{model_to_add} added to {self.model_with_markers_output}")
