#!/bin/sh
#SBATCH --partition=GPUQ
#SBATCH --account=ie-idi
#SBATCH --time=00:15:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=12000
#SBATCH --job-name="Creating the conda environment for ditto"
#SBATCH --output=conda_env
#SBATCH --mail-user=danilasm@stud.ntnu.no
#SBATCH --mail-type=ALL

module purge
module load Anaconda3/2020.
conda env create -f env.yml

uname -a
