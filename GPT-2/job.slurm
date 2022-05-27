#!/bin/sh
#SBATCH --partition=GPUQ
#SBATCH --account=ie-idi
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12000
#SBATCH --job-name="test GPT-2"
#SBATCH --output=test_gpt2.out
#SBATCH --mail-user=danilasm@stud.ntnu.no
#SBATCH --mail-type=ALL

WORKDIR=${SLURM_SUBMIT_DIR}
cd ${WORKDIR}
echo "we are running from this directory: $SLURM_SUBMIT_DIR"
echo " the name of the job is: $SLURM_JOB_NAME"
echo "Th job ID is $SLURM_JOB_ID"

module purge
module load Anaconda3/2020.07
pip3 install transformers==4.2.2 --user
python3 ftgpt2.py --dataset=Dirty/DBLP-ACM --type=matches --amount=double

uname -a