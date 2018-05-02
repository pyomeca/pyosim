import opensim as osim


class Scale:

    def __init__(self, model_input, model_output, xml_input, xml_output, static_path, mass=-1, height=-1, age=-1):
        self.model = osim.Model(model_input)
        self.model_output = model_output
        self.static_path = static_path
        self.xml_output = xml_output

        self.time_range = self.time_range_from_static()

        # load generic scale xml
        self.scale_tool = osim.ScaleTool(xml_input)
        self.set_anthropometry(mass, height, age)
        # Tell scale tool to use the loaded model
        self.scale_tool.getGenericModelMaker().setModelFileName(model_input)

        self.run_model_scaler()
        self.run_marker_placer()

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

    def run_model_scaler(self):
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
        self.scale_tool.getModelScaler().setOutputScaleFileName(self.xml_output.replace('.xml', '_scaling_factor.xml'))

        model_scaler.processModel(self.model)

    def run_marker_placer(self):
        # load a scaled model
        scaled_model = osim.Model(self.model_output)

        marker_placer = self.scale_tool.getMarkerPlacer()
        # Whether or not to use the model scaler during scale`
        marker_placer.setApply(True)
        marker_placer.setTimeRange(self.time_range)

        marker_placer.setStaticPoseFileName(self.static_path)

        # Name of model file (.osim) to write when done scaling
        marker_placer.setOutputModelFileName(self.model_output.replace('.osim', '_markers.osim'))

        # Maximum amount of movement allowed in marker data when averaging
        marker_placer.setMaxMarkerMovement(-1)

        marker_placer.processModel(scaled_model)

        # print scale config to xml
        self.scale_tool.printToXML(self.xml_output)
