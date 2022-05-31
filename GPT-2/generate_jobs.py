def make_text(output, dataset, entity_type, decimate, size=None, ft=False):
    python_line = f"python3 /cluster/home/danilasm/masters/Idun/GPT-2/generate_data.py"
    python_line += f" --dataset={dataset}"
    python_line += f" --type={entity_type}"
    python_line += f" --decimate={decimate}"
    if size != None: python_line += f" --size={size}"
    python_line += f" --ft={ft}"
    decimate_text = "decimate" if decimate else ""
    size_text = " " + size if size != None else ""
    ft_text = "fine_tuned" if ft else "non_fine_tuned"
    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=08:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --mem=12000",
        f"#SBATCH --job-name=\"gen {dataset} {entity_type}{size_text} {decimate_text} {ft_text}\"",
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
    # FT
    name = "./gen_jobs/" + job.replace("/", "_") + "_matches_ft"
    names.append(name)
    text = make_text(name + ".out", job, "matches", False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_ft"
    names.append(name)
    text = make_text(name + ".out", job, "non_matches", False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./gen_jobs/" + job.replace("/", "_") + "_matches_decimated_ft"
    names.append(name)
    text = make_text(name + ".out", job, "matches", True)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_decimated_ft"
    names.append(name)
    text = make_text(name + ".out", job, "non_matches", True)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    # non FT
    name = "./gen_jobs/" + job.replace("/", "_") + "_matches_nft"
    names.append(name)
    text = make_text(name + ".out", job, "matches", False, ft=False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_nft"
    names.append(name)
    text = make_text(name + ".out", job, "non_matches", False, ft=False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./gen_jobs/" + job.replace("/", "_") + "_matches_decimated_nft"
    names.append(name)
    text = make_text(name + ".out", job, "matches", True, ft=False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_decimated_nft"
    names.append(name)
    text = make_text(name + ".out", job, "non_matches", True, ft=False)
    with open(name + ".slurm", "a") as file:
        for line in text:
            file.write(f"{line}\n")

for job in wdc:
    for size in sizes:
        # FT
        name = "./gen_jobs/" + job + "_matches_" + size + "_ft"
        names.append(name)
        text = make_text(name + ".out", job, "matches", False, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_" + size + "_ft"
        names.append(name)
        text = make_text(name + ".out", job, "non_matches", False, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./gen_jobs/" + job.replace("/", "_") + "_matches_decimated_" + size + "_ft"
        names.append(name)
        text = make_text(name + ".out", job, "matches", True, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_decimated_" + size + "_ft"
        names.append(name)
        text = make_text(name + ".out", job, "non_matches", True, size)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        # NFT
        name = "./gen_jobs/" + job + "_matches_" + size + "_nft"
        names.append(name)
        text = make_text(name + ".out", job, "matches", False, size, False)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_" + size + "_nft"
        names.append(name)
        text = make_text(name + ".out", job, "non_matches", False, size, False)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./gen_jobs/" + job.replace("/", "_") + "_matches_decimated_" + size + "_nft"
        names.append(name)
        text = make_text(name + ".out", job, "matches", True, size, False)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = "./gen_jobs/" + job.replace("/", "_") + "_non_matches_decimated_" + size + "_nft"
        names.append(name)
        text = make_text(name + ".out", job, "non_matches", True, size, False)
        with open(name + ".slurm", "a") as file:
            for line in text:
                file.write(f"{line}\n")

with open("run_gen_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm danilasm\n")