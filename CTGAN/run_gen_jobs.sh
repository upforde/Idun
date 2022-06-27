#!/bin/sh

sbatch /cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/Dirty_DBLP-GoogleScholar_non_matches.slurm alekssim
sbatch /cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/Dirty_Walmart-Amazon_non_matches.slurm alekssim
sbatch /cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/Structured_Beer_matches_decimated.slurm alekssim
sbatch /cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/Structured_Walmart-Amazon_non_matches.slurm alekssim
sbatch /cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/Structured_DBLP-GoogleScholar_matches.slurm alekssim
sbatch /cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/Structured_DBLP-GoogleScholar_non_matches.slurm alekssim
