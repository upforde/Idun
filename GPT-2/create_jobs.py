def make_text(output, dataset, entity_type, decimate, size=None):
    python_line = f"python3 /cluster/home/danilasm/masters/Idun/GPT-2/create_model.py"
    python_line += f" --dataset={dataset}"
    python_line += f" --type={entity_type}"
    python_line += f" --decimate={decimate}"
    if size != None: python_line += f" --size={size}"
    decimate_text = "decimate" if decimate else ""
    size_text = " " + size if size != None else ""
    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=08:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --mem=12000",
        f"#SBATCH --job-name=\"model {dataset} {entity_type}{size_text} {decimate_text}\"",
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
    "Structured/Amazon-Google/",
    "Structured/Beer/", 
    "Structured/DBLP-ACM/",
    "Structured/DBLP-GoogleScholar/",
    "Structured/Fodors-Zagats/",
    "Structured/iTunes-Amazon/",
    "Structured/Walmart-Amazon/",
    "Textual/Abt-Buy"
    ]

wdc = [
    "all",
    "cameras",
    "computers",
    "shoes",
    "watches"
]

sizes = [
    "small",
    "medium",
    "large",
    "xlarge"
]

names = []

for job in er_magellan:
    name = "./jobs/" + job.replace("/", "_") + "_matches"
    names.append(name)
    text = make_text(name + ".out", job, "matches", False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./jobs/" + job.replace("/", "_") + "_non_matches"
    names.append(name)
    text = make_text(name + ".out", job, "non_matches", False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./jobs/" + job.replace("/", "_") + "_matches_decimated"
    names.append(name)
    text = make_text(name + ".out", job, "matches", True)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./jobs/" + job.replace("/", "_") + "_non_matches_decimated"
    names.append(name)
    text = make_text(name + ".out", job, "non_matches", True)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

for job in wdc:
    for size in sizes:
        name = "./jobs/" + job + "_matches_" + size
        names.append(name)
        text = make_text(name + ".out", job, "matches", False, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./jobs/" + job.replace("/", "_") + "_non_matches_" + size
        names.append(name)
        text = make_text(name + ".out", job, "non_matches", False, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./jobs/" + job.replace("/", "_") + "_matches_decimated_" + size
        names.append(name)
        text = make_text(name + ".out", job, "matches", True, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./jobs/" + job.replace("/", "_") + "_non_matches_decimated_" + size
        names.append(name)
        text = make_text(name + ".out", job, "non_matches", True, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

with open("run_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm danilasm\n")