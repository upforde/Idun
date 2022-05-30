def make_text(job_name, output, dataset, entity_type, decimate, size=None):
    python_line = f"python3 /cluster/home/danilasm/masters/Idun/GPT-2/create_model.py --dataset={dataset} --type={entity_type} --decimate={decimate}"
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
        f"#SBATCH --job-name=\"{job_name} {entity_type}{size_text} {decimate_text}\"",
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
    for i in range(2):
        if i % 2 == 0: entity_type = "matches"
        else: entity_type = "non_matches"
        for j in range(2): 
            decimate = j % 2 == 0
            
            name = "./jobs/" + job.replace("/", "_") + "_" + entity_type
            if decimate: name += "_decimated"

            output = name + ".out"
            
            text = make_text(job, output, job, entity_type, decimate)

            names.append(name)

            with open(name + ".slurm", "a") as file:
                for line in text:
                    file.write(f"{line}\n")

for job in wdc:
    for size in sizes:
        for i in range(2):
            if i % 2 == 0: entity_type = "matches"
            else: entity_type = "non_matches"
            for j in range(2):
                decimate = j % 2 == 0

                name = "./jobs/" + job.replace("/", "_") + "_" + size + "_" + entity_type
                if decimate: name += "_decimated"

                output = name + ".out"
                
                text = make_text(job, output, job, entity_type, decimate, size)

                names.append(name)

                with open(name + ".slurm", "a") as file:
                    for line in text:
                        file.write(f"{line}\n")

with open("run_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm danilasm\n")