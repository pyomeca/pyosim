from pathlib import Path

import opensim as osim


class Model:
    """Wrapper around opensim's osim models."""

    def __init__(self, path):
        self.path = Path(path)
        if not self.path.is_file():
            raise ValueError(f'{path} does not exist')

        self.model = osim.Model(str(path))
        print(f'\t{self.model.getName()} model loaded')

        self.strengthen(factor=3, output=self.path.parents[0] / 'test.xml')

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
        new_model = self.model.clone()
        for i in range(new_model.getMuscles().getSize()):
            current_muscle = new_model.getMuscles().get(i)
            current_muscle.setMaxIsometricForce(current_muscle.getMaxIsometricForce() * factor)
        new_model.printToXML(str(output))
