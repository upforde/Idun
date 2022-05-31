import os
import glob
import shutil

if os.listdir(r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\jobs"):
    files = glob.glob(r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\jobs\*')
    for f in files:
        os.remove(f)
if os.path.exists(r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\run_jobs.sh"):
    os.remove(r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\run_jobs.sh')

val = input("Flush Models too? [y/n]: ")
if val == "y":
    shutil.rmtree(r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Models')
    os.mkdir(r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Models')