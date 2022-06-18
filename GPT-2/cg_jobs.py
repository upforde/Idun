import os, shutil

IDUN_PATH = "/cluster/home/danilasm/masters/Idun/"

if not os.path.exists(IDUN_PATH + "GPT-2/cg_jobs"):
    os.makedirs(IDUN_PATH + "GPT-2/cg_jobs")

if len(os.listdir(IDUN_PATH + "GPT-2/cg_jobs")) != 0:
    shutil.rmtree(IDUN_PATH + "GPT-2/cg_jobs")
    os.makedirs(IDUN_PATH + "GPT-2/cg_jobs")

def make_text(output, dataset, entity_type, decimate):
    python_line = f"python3 /cluster/home/danilasm/masters/Idun/GPT-2/cg.py"
    python_line += f" --dataset={dataset}"
    python_line += f" --type={entity_type}"
    python_line += f" --decimate={decimate}"
    decimate_text = " decimate" if decimate else ""
    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --gres=gpu:1",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=72:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --mem=12000",
        f"#SBATCH --job-name=\"cg {dataset} {entity_type}{decimate_text}\"",
        f"#SBATCH --output={output}",
        "#SBATCH --mail-user=danilasm@stud.ntnu.no",
        "#SBATCH --mail-type=ALL",
        
        "module purge",
        "module load Anaconda3/2020.07",
        "pip3 install transformers==4.2.2 --user",
        python_line,
        "uname -a"
    ]
    return text

er_magellan = [
    "Dirty/DBLP-ACM",
    "Dirty/DBLP-GoogleScholar",
    "Dirty/iTunes-Amazon",
    "Dirty/Walmart-Amazon",
    "Structured/Amazon-Google",
    "Structured/Beer", 
    "Structured/DBLP-ACM",
    "Structured/DBLP-GoogleScholar",
    "Structured/Fodors-Zagats",
    "Structured/iTunes-Amazon",
    "Structured/Walmart-Amazon",
    "Textual/Abt-Buy"
    ]

def create(name, job, type, decimate):
    text = make_text(name + ".out", job, type, decimate)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

names = []

for job in er_magellan:
    name = "./cg_jobs/" + job.replace("/", "_") + "_matches"
    names.append(name)
    create(name, job, "matches", False)

    name = "./cg_jobs/" + job.replace("/", "_") + "_non_matches"
    names.append(name)
    create(name, job, "non_matches", False)

    name = "./cg_jobs/" + job.replace("/", "_") + "_matches_decimated"
    names.append(name)
    create(name, job, "matches", True)

    name = "./cg_jobs/" + job.replace("/", "_") + "_non_matches_decimated"
    names.append(name)
    create(name, job, "non_matches", True)

open("run_cg_jobs.sh", "w").close()
with open("run_cg_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm danilasm\n")