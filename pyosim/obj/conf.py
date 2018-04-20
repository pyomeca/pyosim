"""
Configuration class in pyosim
"""
from pathlib import Path

import pandas as pd


class Conf:
    def __init__(self, project_path, conf_file='_conf.csv'):
        """Configuration class in pyosim"""
        # load project dir
        self.project_path = Path(project_path)
        if not self.project_path.is_dir():
            raise ValueError(f'{self.project_path} does not exist')
        else:
            print('Project loaded')

        # load project conf
        self.conf_path = self.project_path / conf_file
        if not self.conf_path.is_file():
            raise ValueError(f'{self.conf_path} does not exist')
        else:
            self.project_conf = pd.read_csv(self.conf_path)
            print('Configuration file loaded')

    def get_conf_column(self, col):
        """
        Get column(s) from the conf file

        Parameters
        ----------
        col : str
            column to return

        Returns
        -------
        pandas series
        """
        return self.project_conf[col]

    def check_confs(self):
        """check if all participants have a configuration file and update it in the project's configuration file"""

        for index, irow in self.project_conf.iterrows():
            if irow['conf_file'] == irow['conf_file']:  # check if nan
                if Path(irow['conf_file']).is_file():
                    print(f'{irow["participant"]}: checked')
                else:
                    raise ValueError(f'{irow["participant"]} does not have a configuration file in {irow["conf_file"]}')
            else:
                d = (self.project_path / irow['participant'] / '_conf.json')
                if d.is_file():
                    self.project_conf.loc[index, 'conf_file'] = str(d.absolute())
                    print(f'{irow["participant"]}: updated in project conf')

        # update conf file
        self.project_conf.to_csv(self.conf_path)
