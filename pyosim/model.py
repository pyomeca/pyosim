"""
Model class in pyosim
"""
import opensim as osim


class Model(osim.Model):
    """Wrapper around opensim's osim models."""

    def strengthen(self, factor, output):
        """
        Strengthens a model by multiplying the maximum isometric forces of each muscle by the `factor` parameter

        Parameters
        ----------
        factor : int
            Factor with which to multiply the max. iso. forces of each muscles
        output : str
            New model path
        """
        new_model = self.clone()
        output = str(output)
        for i in range(new_model.getMuscles().getSize()):
            current_muscle = new_model.getMuscles().get(i)
            current_muscle.setMaxIsometricForce(current_muscle.getMaxIsometricForce() * factor)
        new_model.printToXML(output)
        print(f'{output} created')
