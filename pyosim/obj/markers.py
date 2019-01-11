from pathlib import Path

import numpy as np
import opensim as osim

from pyomeca import Markers3d


class Markers3dOsim(Markers3d):
    def __new__(cls, *args, **kwargs):
        """Convenient wrapper around Markers3d from the pyomeca library"""
        return super(Markers3dOsim, cls).__new__(cls, *args, **kwargs)

    def __array_finalize__(self, obj):
        super().__array_finalize__(obj)
        # Allow slicing
        if obj is None or not isinstance(obj, Markers3dOsim):
            return

    def to_trc(self, filename):
        """
        Write a trc file from a Markers3dOsim
        Parameters
        ----------
        filename : string
            path of the file to write
        """
        filename = Path(filename)
        # Make sure the directory exists, otherwise create it
        if not filename.parents[0].is_dir():
            filename.parents[0].mkdir()

        # Make sure the metadata are set
        if not self.get_rate:
            raise ValueError('get_rate is empty. Please fill with `your_variable.get_rate = 100.0` for example')
        if not self.get_unit:
            raise ValueError('get_unit is empty. Please fill with `your_variable.get_unit = "mm"` for example')
        if not self.get_labels:
            raise ValueError(
                'get_labels is empty. Please fill with `your_variable.get_labels = ["M1", "M2"]` for example')

        table = osim.TimeSeriesTableVec3()

        # set metadata
        table.setColumnLabels(self.get_labels)
        table.addTableMetaDataString('DataRate', str(self.get_rate))
        table.addTableMetaDataString('Units', self.get_unit)

        time_vector = np.arange(start=0, stop=1 / self.get_rate * self.shape[2], step=1 / self.get_rate)

        for iframe in range(self.shape[-1]):
            a = np.round(self.get_frame(iframe)[:-1, ...], decimals=4)
            row = osim.RowVectorOfVec3(
                [osim.Vec3(a[0, i], a[1, i], a[2, i]) for i in range(a.shape[-1])]
            )
            table.appendRow(time_vector[iframe], row)

        adapter = osim.TRCFileAdapter()
        adapter.write(table, str(filename))
