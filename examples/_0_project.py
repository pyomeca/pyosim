import os
import json
import shutil

from pyogui import FieldsAssignment
from project_conf import PROJECT_PATH, LOCAL_DATA_PARENT_PATH, CONF_TEMPLATE, LOCAL_MVC_PARENT_PATH, DATA_PARENT_PATH, MVC_PARENT_PATH, BASE_PROJECT_DISTANT
from pyosim import Conf, Project

# ACTUAL PARTICIPANT TO PROCESS #
participant_to_do=5
debug='false'
distant_ip = 'ec2-34-212-104-202.us-west-2.compute.amazonaws.com'
pem_file_path = '~/.ssh/bimec29-kinesio.pem'
#################################


# All this is done just to get the local data folder
# remove project if already exists (you don't need to do this)
if PROJECT_PATH.is_dir():
    shutil.rmtree(PROJECT_PATH)

# create Project object
project = Project(path=PROJECT_PATH)

# create project directory
project.create_project()

# add participants from the template conf file
shutil.copy(CONF_TEMPLATE, PROJECT_PATH)
project.update_participants(participant_to_do)

# Create a Conf object
conf = Conf(project_path=PROJECT_PATH)

# Check if all participants have a configuration file and update it in the project's configuration file
conf.check_confs(participant_to_do)

# add some data path in participants' conf file
participants = conf.get_participants_to_process()
d = {}
for iparticipant in participants:
    pseudo_in_path = iparticipant[0].upper() + iparticipant[1:-1] + iparticipant[-1].upper()
    trials = f'{LOCAL_DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/trials'
    score = f'{LOCAL_DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/MODEL2'
    mvc = f'{LOCAL_MVC_PARENT_PATH}/{pseudo_in_path}'

    d.update({iparticipant: {'emg': {'data': [trials, mvc]},
                             'analogs': {'data': [trials]},
                             'markers': {'data': [trials, score]}}})
conf.add_conf_field(d)

# assign channel fields to targets fields
targets = {
    'emg': ['deltant', 'deltmed', 'deltpost', 'biceps', 'triceps', 'uptrap', 'lotrap',
            'serratus', 'ssp', 'isp', 'subs', 'pect', 'latissimus'],
    'analogs': ['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'],
    'markers': ['ASISl', 'ASISr', 'PSISl', 'PSISr', 'STER', 'STERl', 'STERr', 'T1', 'T10', 'XIPH', 'CLAVm', 'CLAVl',
                'CLAV_ant', 'CLAV_post', 'CLAV_SC', 'ACRO_tip', 'SCAP_AA', 'SCAPl', 'SCAPm', 'SCAP_CP', 'SCAP_RS',
                'SCAP_SA', 'SCAP_IA', 'CLAV_AC', 'DELT', 'ARMl', 'ARMm', 'ARMp_up', 'ARMp_do', 'EPICl', 'EPICm',
                'LARMm', 'LARMl', 'LARM_elb', 'LARM_ant', 'STYLr', 'STYLr_up', 'STYLu', 'WRIST', 'INDEX', 'LASTC',
                'MEDH', 'LATH', 'boite_gauche_ext', 'boite_gauche_int', 'boite_droite_int', 'boite_droite_ext',
                'boite_avant_gauche', 'boite_avant_droit', 'boite_arriere_droit', 'boite_arriere_gauche']
}

for ikind, itarget in targets.items():
    for iparticipant in participants:
        fields = FieldsAssignment(
            directory=conf.get_conf_field(iparticipant, field=[ikind, 'data']),
            targets=itarget,
            kind=ikind
        )
        conf.add_conf_field({iparticipant: fields.output})

actual_participant = participants[0]
pseudo_in_path = actual_participant[0].upper() + actual_participant[1:-1] + actual_participant[-1].upper()
trials_local = f'{LOCAL_DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/trials/'
score_local = f'{LOCAL_DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/MODEL2/'
mvc_local = f'{LOCAL_MVC_PARENT_PATH}/{pseudo_in_path}/'
trials_distant = f'{DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/'
score_distant = f'{DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/'
mvc_distant = f'{MVC_PARENT_PATH}/'

# CHANGE PATHS SO THE DISTANT JSON HAS A VALID FILE
filename = conf.get_conf_path(actual_participant)
file = open(filename, 'r')
data = json.load(file)
file.close()
data['conf_file'] = [f'{BASE_PROJECT_DISTANT}results/{actual_participant}/_conf.json/']
data['emg']['data'] = [f'{trials_distant}trials/', f'{mvc_distant}{pseudo_in_path}/']
data['analogs']['data'] = [f'{trials_distant}trials/']
data['markers']['data'] = [f'{trials_distant}trials/', f'{score_distant}MODEL2/']

# data.update(d)
file = open(filename, 'w+')
json.dump(data, file)
file.close()

# Do the same for the other conf file
conf.project_conf.loc[participant_to_do, 'conf_file'] = f"{BASE_PROJECT_DISTANT}results/{actual_participant}/_conf.json"
conf.project_conf.to_csv(conf.conf_path, index=False)

# Call the script that does the interface with distant computer
os.system(f"./ceinms_runner.sh {trials_local} {score_local} {mvc_local} {trials_distant} {score_distant} {mvc_distant} {distant_ip} {pem_file_path} {BASE_PROJECT_DISTANT} log_{actual_participant}.log {debug}")
