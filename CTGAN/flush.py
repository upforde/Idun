import os
import glob
import shutil
import time

val0 = input("Flush matching job files? [y/n]")
if val0 == "y":
    if os.listdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/'):
        shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/Augmentation')
        shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/CTGAN')
        shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/GPT-2_ft')
        shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/GPT-2_nft')
        os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/Augmentation')
        os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/CTGAN')
        os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/GPT-2_ft')
        os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/GPT-2_nft')
    if os.path.exists(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_match_jobs.sh"):
        os.remove(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_match_jobs.sh")
    if os.path.exists(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/Temp_Tables"):
        shutil.rmtree(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/Temp_Tables")
        os.mkdir(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/Temp_Tables")
    if os.path.exists(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Results"):
        shutil.rmtree(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Results")
        os.mkdir(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Results")
        

val1 = input("Flush training or generation? [t/g/n]: ")
if val1 == "t":
    if os.listdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/jobs/'):
        files = glob.glob(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/jobs/*')
        for f in files:
            os.remove(f)
    if os.path.exists(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_jobs.sh"):
        os.remove(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_jobs.sh")
elif val1 == "g":
    if os.listdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/'):
        files = glob.glob(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/*')
        for f in files:
            os.remove(f)
    if os.path.exists(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_gen_jobs.sh"):
        os.remove(r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/run_gen_jobs.sh")

if val1 == "t":
    val2 = input("Flush Models too? [y/n]: ")
    if val2 == "y":
        val3 = input("WOAH. Are you sure? [y/n]: ")
        if val3 == "y":
            print("I'm giving you 5 seconds to think about it...")
            for i in range(1, 6):
                time.sleep(1)
                print("..." + i + "...")
            shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models')
            os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models')
elif val1 == "g":
    val2 = input("Flush Generated Synthethic Data too? [y/n]: ")
    if val2 == "y":
        val3 = input("Is the data Magellan? [y/n]: ")
        if val3 == "y":
            shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan')
            os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan')
        else:
            shutil.rmtree(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Ditto')
            os.mkdir(r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Ditto')