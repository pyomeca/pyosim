"""
Example: create a project.
"""
import shutil

#from pyogui import FieldsAssignment
from pyosim import Conf
from pyosim import Project
from project_conf import PROJECT_PATH, DATA_PARENT_PATH, CONF_TEMPLATE, MVC_PARENT_PATH


def main(specific_participant=-1, erase_previous_project=False):
    try:
        if erase_previous_project:
            # remove project if already exists (you don't need to do this)
            if PROJECT_PATH.is_dir():
                shutil.rmtree(PROJECT_PATH)

        # create Project object
        project = Project(path=PROJECT_PATH)

        if erase_previous_project:
            # create project directory
            project.create_project()

            # add participants from the template conf file
            shutil.copy(CONF_TEMPLATE, PROJECT_PATH)
        project.update_participants(specific_participant)

        # Create a Conf object
        conf = Conf(project_path=PROJECT_PATH)

        # Check if all participants have a configuration file and update it in the project's configuration file
        conf.check_confs(specific_participant)

        # add some data path in participants' conf file
        participants = conf.get_participants_to_process()
        d = {}
        for iparticipant in participants:
            pseudo_in_path = iparticipant[0].upper() + iparticipant[1:-1] + iparticipant[-1].upper()
            trials = f'{DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/trials'
            score = f'{DATA_PARENT_PATH}/IRSST_{pseudo_in_path}d/MODEL2'
            mvc = f'{MVC_PARENT_PATH}/{pseudo_in_path}'

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

        # for ikind, itarget in targets.items():
        #     for iparticipant in participants:
        #         fields = FieldsAssignment(
        #             directory=conf.get_conf_field(iparticipant, field=[ikind, 'data']),
        #             targets=itarget,
        #             kind=ikind
        #         )
        #         conf.add_conf_field({iparticipant: fields.output})
        print("coucou")
        return True

    except:
        return False


if __name__ == "__main__":
    main()
