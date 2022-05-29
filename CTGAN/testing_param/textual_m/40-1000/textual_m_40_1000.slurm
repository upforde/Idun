#!/bin/sh
#SBATCH --partition=GPUQ
#SBATCH --account=ie-idi
#SBATCH --time=09:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12000
#SBATCH --job-name="Textual Data Matches with 40 batch size and 1000 epochs"
#SBATCH --output=textual_m.out
#SBATCH --mail-user=alekssim@stud.ntnu.no
#SBATCH --mail-type=ALL

WORKDIR=${SLURM_SUBMIT_DIR}
cd ${WORKDIR}
echo "we are running from this directory: $SLURM_SUBMIT_DIR"
echo " the name of the job is: $SLURM_JOB_NAME"
echo "Th job ID is $SLURM_JOB_ID"

module purge
module load Anaconda3/2020.07
module load Python/3.8.6-GCCcore-10.2.0
pip3 install pandas --user
pip3 install sdv --user
pip3 install numpy==1.21
python3 CTGAN_train_m.py

uname -a