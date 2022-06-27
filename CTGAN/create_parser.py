import os

def make_text(output, dataset, matches, decimate, ditto_parse=True, generator_type=1):
    generator_text = [
    r"CTGAN",
    r"GPT-2_ft",
    r"GPT-2_nft",
    r"Augmentation"
    ]
    
    script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/parse_data.py"
    python_line = f"python3 \"{script_path}\" --dataset=\"{dataset}\" --matches={matches} --decimate={decimate} --ditto_parse={ditto_parse} --generator_type={generator_type}"
    decimate_text = "decimate" if decimate else ""
    matched_text = "matched" if matches else "non_matched"
    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=00:20:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --gres=gpu:V10032:1",
        f"#SBATCH --job-name=\"Parse {generator_text[generator_type-1]} {dataset} {matched_text} {decimate_text} \"",
        f"#SBATCH --output={output}",
        "#SBATCH --mail-user=alekssim@stud.ntnu.no",
        "#SBATCH --mail-type=ALL",
        
        "module purge",
        "module load Anaconda3/2020.07",
        "module load Python/3.8.6-GCCcore-10.2.0",
        "pip3 install pandas --user",
        "pip3 install numpy==1.21",
        python_line,
        "uname -a"
    ]
    return text

generator_type = [
    r"CTGAN",
    r"GPT-2_ft",
    r"GPT-2_nft",
    r"Augmentation"
    ]

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

jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/parse_jobs/'


# TODO
# NOTE: Change according to what format we wish for. True = Ditto
data_format = True


for i in range(1, 5): # 5
    for job in er_magellan:
        name = jobs_dir + generator_type[i-1] + os.sep + job.replace(os.sep, "_") + "_matches"
        names.append(name)
        text = make_text(name + ".out", job, True, False, data_format, i)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = jobs_dir + generator_type[i-1] + os.sep + job.replace(os.sep, "_") + "_non_matches"
        names.append(name)
        text = make_text(name + ".out", job, False, False, data_format, i)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = jobs_dir + generator_type[i-1] + os.sep + job.replace(os.sep, "_") + "_matches_decimated"
        names.append(name)
        text = make_text(name + ".out", job, True, True, data_format, i)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = jobs_dir + generator_type[i-1] + os.sep + job.replace(os.sep, "_") + "_non_matches_decimated"
        names.append(name)
        text = make_text(name + ".out", job, False, True, data_format, i)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

with open("run_parse_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm alekssim\n")