"""
Configuration class in pyosim
"""
import json
from pathlib import Path

import pandas as pd


class Conf:
    """
    Configuration class in pyosim

    Parameters
    ----------
    project_path : str, Path
        Path to the project
    conf_file : str
        Filename of the configuration file
    """

    def __init__(self, project_path, conf_file='_conf.csv'):
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
        print('\n')

    def get_participants_to_process(self):
        """
        Get a list of participants with the flag 'process' to one or true in project configuration file
        Returns
        -------
        list
        """
        to_process = self.project_conf['process'] == True
        return self.project_conf['participant'].loc[to_process].tolist()

    def get_project_conf_column(self, col):
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

    def check_confs(self, specific_participant=-1):
        """check if all participants have a configuration file and update it in the project's configuration file"""

        for index, irow in self.project_conf.iterrows():
            if not irow['process']:
                break
            if specific_participant >= 0 and index != specific_participant:
                self.project_conf.loc[index, "process"] = 0
                continue
            default = (self.project_path / irow['participant'] / '_conf.json')
            is_nan = irow['conf_file'] != irow['conf_file']
            if not is_nan and Path(irow['conf_file']).is_file():
                print(f'{irow["participant"]}: checked')
            if (is_nan and default.is_file()) or default.is_file():  # check if nan or file exist in default location
                conf_file = str(default.resolve())
                self.project_conf.loc[index, 'conf_file'] = conf_file
                self.update_conf(conf_file, {'conf_file': conf_file})
                print(f'{irow["participant"]}: updated in project conf')
            else:
                raise ValueError(f'{irow["participant"]} does not have a configuration file in {irow["conf_file"]}')

        # update conf file
        print('\n')
        self.project_conf.to_csv(self.conf_path, index=False)

    @classmethod
    def update_conf(cls, filename, d):
        """
        Update a json file with the dictionary `d`
        Parameters
        ----------
        filename : str
            Path to the json file
        d : dict
            Dictionary to add in configuration file
        """

        def dict_merge(dct, merge_dct):
            """Recursive dict merge. Inspired by :meth:`dict.update()`, instead of
            updating only top-level keys, dict_merge recurses down into dicts nested
            to an arbitrary depth, updating keys. The `merge_dct` is merged into
            `dct`.


            Parameters
            ----------
            dct : dict
                dict onto which the merge is executed
            merge_dct : dict
                dct merged into dct
            """
            from collections import Mapping
            for k, v in merge_dct.items():
                if (k in dct and isinstance(dct[k], dict)
                        and isinstance(merge_dct[k], Mapping)):
                    dict_merge(dct[k], merge_dct[k])
                else:
                    dct[k] = merge_dct[k]
            return dct

        file = open(filename, 'r')
        data = json.load(file)

        # data.update(d)
        file = open(filename, 'w+')
        json.dump(dict_merge(data, d), file)
        file.close()

    @classmethod
    def get_conf_file(cls, filename):
        """
        Get a configuration file

        Parameters
        ----------
        filename : str
            Path to the json file

        Returns
        -------
        dict
        """
        with open(filename) as file:
            data = json.load(file)
        return data

    def add_conf_field(self, d):
        """
        Update configurations files from a dictionary. The keys should be the participant's pseudo

        Parameters
        ----------
        d : dict
            Dictionary to add in configuration file

        Examples
        -------
        # add some data path
        d = {
            'dapo': {'data': '/home/romain/Downloads/conf-files/DapO/mvc'},
            'davo': {'data': '/home/romain/Downloads/conf-files/DavO/mvc'},
            'fabd': {'data': '/home/romain/Downloads/conf-files/FabD/mvc'}
        }
        project.add_conf_field(d)
        """
        for iparticipant, ivalue in d.items():
            conf_file = self.get_conf_path(iparticipant)
            self.update_conf(conf_file, ivalue)
            print(f"{iparticipant}'s conf file updated")

    def get_conf_path(self, participant):
        """
        Get participant's configuration file path

        Parameters
        ----------
        participant : str
            Participant
        """
        conf_path = self.project_conf[self.project_conf['participant'] == participant]['conf_file'].values[0]
        return conf_path

    def get_conf_field(self, participant, field):
        """
        Get participant's specific configuration field
        Parameters
        ----------
        participant : str
            Participant
        field : str, list
            Field(s) to search in the configuration file

        Returns
        -------
        str
        """
        conf_path = self.get_conf_path(participant)
        conf_file = self.get_conf_file(conf_path)

        def get_from_dict(d, keys):
            for k in keys:
                d = d[k]
            return d

        return get_from_dict(conf_file, field)
