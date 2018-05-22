from pathlib import Path

import pandas as pd


class Project:
    """Project manager."""

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
            print(f'{self.path} created')
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

        conf_cols = ['participant', 'sex', 'laterality', 'group', 'mass', 'height', 'raw_data', 'process']

        pd.DataFrame(columns=conf_cols).to_csv(self.path / '_conf.csv')

        print(
            f'You should now:\n'
            f'\t1. Put one or several models into: `{self.path}/_models`\n'
            f'\t2. Put your generic XMLs into: `{self.path}/_templates`\n'
            f'\t3. Fill the conf file: {self.path}/_conf.csv'
        )

    def update_participants(self):
        """add participants in project.

        1. Read the project configuration file
        2. Check if there is participant(s) added in the configuration file and not yet imported in the project
        3. Add these participants and add participant directories
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
            '4_muscle_analysis'  # generated STO files from muscle analysis
        ]

        count = 0
        for irow in conf.iterrows():
            if irow[1]['process'] and not list(self.path.glob(f"{irow[1]['participant']}")):
                count += 1
                for idir in participant_dirs:
                    (self.path / irow[1]['participant'] / idir).mkdir(parents=True)

        print(f'{count} participants added')


if __name__ == '__main__':
    PROJECT_PATH = Path('/home/romain/Downloads/opensim/project')
    project = Project(PROJECT_PATH)

    if not PROJECT_PATH.is_dir():
        project.create_project()
    project.update_participants()
