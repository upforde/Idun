import os

def make_text(output, dataset, matches, decimate, size=None, threshold=0.7, drop_dupes=True):
    script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/CTGAN_generation.py"
    python_line = f"python3 \"{script_path}\" --dataset=\"{dataset}\" --matches={matches} --decimate={decimate} --threshold={threshold} --drop_dupes={drop_dupes}"
    if size != None: python_line += " --size=" + size
    decimate_text = "decimate" if decimate else ""
    size_text = size if size != None else ""
    matched_text = "matched" if matches else "non_matched"
    drop_text = "drop dupes" if drop_dupes else ""
    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=04:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --gres=gpu:V10032:1",
        f"#SBATCH --job-name=\"CTGAN_gen {dataset} {matched_text} {size_text} {decimate_text} {drop_text}\"",
        f"#SBATCH --output={output}",
        "#SBATCH --mail-user=alekssim@stud.ntnu.no",
        "#SBATCH --mail-type=ALL",
        
        "module purge",
        "module load Anaconda3/2020.07",
        "module load Python/3.8.6-GCCcore-10.2.0",
        "pip3 install pandas --user",
        "pip3 install sdv --user",
        "pip3 install numpy==1.21",
        "pip3 install python-Levenshtein --user",
        python_line,
        "uname -a"
    ]
    return text


er_magellan = [
    r"Dirty/DBLP-ACM",
    r"Dirty/DBLP-GoogleScholar",
    r"Dirty/iTunes-Amazon",
    r"Dirty/Walmart-Amazon",
    r"Structured/Amazon-Google",
    r"Structured/Beer",
    r"Structured/DBLP-ACM",
    r"Structured/DBLP-GoogleScholar",
    r"Structured/Fodors-Zagats",
    r"Structured/iTunes-Amazon",
    r"Structured/Walmart-Amazon",
    r"Textual/Abt-Buy"
    ]

names = []

jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/'

for job in er_magellan:
    name = jobs_dir + job.replace(os.sep, "_") + "_matches"
    names.append(name)
    text = make_text(name + ".out", job, True, False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = jobs_dir + job.replace(os.sep, "_") + "_non_matches"
    names.append(name)
    text = make_text(name + ".out", job, False, False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = jobs_dir + job.replace(os.sep, "_") + "_matches_decimated"
    names.append(name)
    text = make_text(name + ".out", job, True, True)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = jobs_dir + job.replace(os.sep, "_") + "_non_matches_decimated"
    names.append(name)
    text = make_text(name + ".out", job, False, True)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

with open("run_gen_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm alekssim\n")