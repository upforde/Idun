import os
import glob
import shutil

if os.listdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/jobs/'):
    files = glob.glob(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/jobs/*')
    for f in files:
        os.remove(f)
if os.path.exists(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_jobs.sh"):
    os.remove(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_jobs.sh")

val = input("Flush Models too? [y/n]: ")
if val == "y":
    shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models')
    os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models')