#!/bin/bash
# Arguments are 
#...


## SETUP ##

debug=${11}
if [ -z "$debug" ]
then
    debug=false
fi

# Get the data folder
local_data_folder=$1
local_score_folder=$2
local_mvc_folder=$3
distant_data_folder=$4
distant_score_folder=$5
distant_mvc_folder=$6
if [ -z "$local_data_folder" ] || [ -z "$local_mvc_folder" ] || [ -z "$distant_data_folder" ] || [ -z "$distant_mvc_folder" ]
then
    echo "Data were not provided (Arg1-Local data / Arg2-local MVC / Arg3-Distant data folder / Arg4 Distant MVC folder)"
    exit 1
fi

# Get the distant informations
hostname=$7
pem_file=$8
distant_user_name=ubuntu
if [ -z "$hostname" ] || [ -z "$pem_file" ]
then
    echo "Hosting informations were not provided (Arg5-DNS / Arg6-pem file / destination)"
    exit 1
fi
distant_data_folder_address=$distant_user_name@$hostname:$distant_data_folder
distant_score_folder_address=$distant_user_name@$hostname:$distant_score_folder
distant_mvc_folder_address=$distant_user_name@$hostname:$distant_mvc_folder

# Get the script to run
running_python_script=$9
log_file=${10}

# Print if needed
if [ $debug = true ] ;
then
    echo "Printing some debug informations.."
    echo "local_data_folder = $local_data_folder"
    echo "local_score_folder = $local_score_folder"
    echo "local_mvc_folder = $local_mvc_folder"
    echo "hostname = $hostname"
    echo "pem_file = $pem_file"
    echo "distant_user_name = $distant_user_name"
    echo "distant_data_folder_address = $distant_data_folder_address"
    echo "distant_score_folder_address = $distant_score_folder_address"
    echo "distant_mvc_folder_address = $distant_mvc_folder_address"
    echo "running_python_script = $running_python_script"
    echo "log_file = $log_file"
    echo "Done"
    echo ""
    exit 1
fi



## START THE ACTUAL PROGRAM ##

# Commit push all modification of pyosim from local / pull from distant
git_branch=ceinms
git commit -am "Automatically generated commit..."
git push origin $git_branch
ssh -i $pem_file $distant_user_name@$hostname "cd $running_python_script; git pull origin $git_branch"

# Copy data from local
echo "Copying local data and mvc to distant folder.."
ssh -i $pem_file $distant_user_name@$hostname "mkdir -p $distant_data_folder"
ssh -i $pem_file $distant_user_name@$hostname "mkdir -p $distant_score_folder"
ssh -i $pem_file $distant_user_name@$hostname "mkdir -p $distant_mvc_folder"

scp -r -i $pem_file $local_data_folder $distant_data_folder_address
scp -r -i $pem_file $local_score_folder $distant_score_folder_address
scp -r -i $pem_file $local_mvc_folder $distant_mvc_folder_address
echo "Done"
echo ""

# Do the analysis
echo "Executing the analysis.."
cp -r _models results/
cp -r _templates results/
scp -r -i $pem_file results $distant_user_name@$hostname:$running_python_script
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _1_markers.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _2_emg.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _3_forces.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _4_scaling.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _5_inverse_kinematics.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _6_inverse_dynamics.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _7_static_optimization.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _8_muscle_analysis.py >> $log_file"
ssh -X -i $pem_file $distant_user_name@$hostname "cd $running_python_script; /home/ubuntu/miniconda3/envs/CEINMS/bin/python3 _9_joint_reaction.py >> $log_file"
echo "Done"
echo ""

# Copy back the results
mkdir final_results
scp -r -i $pem_file $distant_user_name@$hostname:${running_python_script}results final_results

# Delete distant data
echo "Deleting distant data and mvc.."
ssh -i $pem_file $distant_user_name@$hostname "rm -rf $distant_data_folder"
ssh -i $pem_file $distant_user_name@$hostname "rm -rf $distant_score_folder"
ssh -i $pem_file $distant_user_name@$hostname "rm -rf $distant_mvc_folder"
ssh -i $pem_file $distant_user_name@$hostname "rm -rf $distant_user_name@$hostname:${running_python_script}results"
echo "Done"
echo ""



