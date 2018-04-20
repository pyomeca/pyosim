from pathlib import Path

import numpy as np
import opensim as osim

from pyomeca.obj.analogs import Analogs3d


class Analogs3dOsim(Analogs3d):
    def __new__(cls, *args, **kwargs):
        """Convenient wrapper around Analogs3d from the pyomeca library"""
        return super(Analogs3dOsim, cls).__new__(cls, *args, **kwargs)

    def __array_finalize__(self, obj):
        super().__array_finalize__(obj)
        # Allow slicing
        if obj is None or not isinstance(obj, Analogs3dOsim):
            return

    def to_sto(self, file_name):
        """
        Write a sto file from a Analogs3dOsim
        Parameters
        ----------
        file_name : string
            path of the file to write
        """
        file_name = Path(file_name)
        # Make sure the directory exists, otherwise create it
        if not file_name.parents[0].is_dir():
            file_name.parents[0].mkdir()

        table = osim.TimeSeriesTable()

        # set metadata
        table.setColumnLabels(self.get_labels)

        time_vector = np.arange(start=0, stop=1 / self.get_rate * self.shape[2], step=1 / self.get_rate)

        for iframe in range(self.shape[-1]):
            a = self.get_frame(iframe)
            row = osim.RowVector(a.ravel().tolist())
            table.appendRow(time_vector[iframe], row)

        adapter = osim.STOFileAdapter()
        adapter.write(table, str(file_name))
