"""
Project class in pyosim
"""

from pathlib import Path

import pandas as pd


class Project:
    """
    Project manager

    Parameters
    ----------
    path : str, Path
        Path to the project
    """

    def __init__(self, path):
        self.path = Path(path)

    def create_project(self):
        """create a new project pyosim project.

        1. Check if folder is empty or non existent (else error)
        2. Add project directories
        3. Create a configuration file
        """

        # check directory
        if not self.path.is_dir():
            self.path.mkdir()
            print(f'{self.path} created\n')
        else:
            files = [ifile for ifile in self.path.rglob('*')]
            if files:
                raise IsADirectoryError(f'{self.path} is not empty. Please choose an empty directory')
            else:
                print(f'{self.path} selected')

        # create project directories
        project_dirs = [
            '_templates',  # generic XML
            '_models'  # generic models*
        ]

        for idir in project_dirs:
            (self.path / idir).mkdir()

        conf_cols = ['participant', 'sex', 'laterality', 'group', 'mass', 'height', 'conf_file', 'process']

        pd.DataFrame(columns=conf_cols).to_csv(self.path / '_conf.csv', index=False)

        print(
            f'You should now:\n'
            f'\t1. Put one or several models into: `{self.path}/_models`\n'
            f'\t2. Put your generic XMLs into: `{self.path}/_templates`\n'
            f'\t3. Fill the conf file: {self.path}/_conf.csv\n'
        )

    def update_participants(self, specific_participant=-1):
        """add participants in project.

        1. Read the project configuration file
        2. Check if there is participant(s) added in the configuration file and not yet imported in the project
        3. Add these participants and add participant directories
        4. write a configuration file in each participant directory
        """
        conf = pd.read_csv(self.path / '_conf.csv')

        participant_dirs = [
            '_xml',  # generated XMLs
            '_models',  # generated models
            '0_markers',  # markers in TRC format
            '0_emg',  # emg in STO format
            '0_forces',  # forces in STO format
            '1_inverse_kinematic',  # generated MOT motion files from inverse kinematic
            '2_inverse_dynamic',  # generated STO files from inverse dynamic
            '3_static_optimization',  # generated STO files from static optimization
            '4_muscle_analysis',  # generated STO files from muscle analysis
            '5_joint_reaction_force',  # generated STO files from joint reaction force analysis
            'temp_optim_wrap',  # Serve as temporary folder while performing the wrapping adjustment
            'template_temp_optim_wrap'  # Serve as temporary folder while performing the wrapping adjustment
        ]

        count = 0
        for index, irow in conf.iterrows():
            if irow['process'] and not list(self.path.glob(f"{irow['participant']}")):
                count += 1
                if specific_participant < 0 or index == specific_participant:
                    for idir in participant_dirs:
                        (self.path / irow['participant'] / idir).mkdir(parents=True)

                    # create conf file
                    irow.to_json(self.path / irow['participant'] / '_conf.json')

        print(f'{count} participants added\n')
