import os, shutil, random

IDUN_PATH = "/cluster/home/danilasm/masters/Idun/"

if not os.path.exists(IDUN_PATH + "ditto/jobs"):
    os.makedirs(IDUN_PATH + "ditto/jobs")

if len(os.listdir(IDUN_PATH + "ditto/jobs")) != 0:
    shutil.rmtree(IDUN_PATH + "ditto/jobs")
    os.makedirs(IDUN_PATH + "ditto/jobs")

def make_text(task, name):
    python_line = f"python3 /cluster/home/danilasm/masters/Idun/ditto/train_ditto.py"
    python_line += f" --task={task}"
    python_line += " --batch_size=32"
    python_line += f" --output_name={name}"
    seed = str(round(random.random()*2147483647))
    python_line += f" --seed={seed}"

    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=12:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --mem=12000",
        f"#SBATCH --job-name=\"ditto {task}\"",
        f"#SBATCH --output={task}",
        "#SBATCH --mail-user=danilasm@stud.ntnu.no",
        "#SBATCH --mail-type=ALL",
        "module purge",
        "module load Anaconda3/2020.07",
        python_line,
        "uname -a"
    ]
    return text

def make_config(task, train, test, valid):
    text = [
        "{",
        f"\t\"name\": \"{task}\",",
        "\t\"task_type\": \"classification\",",
        "\t\"vocab\": [\"0\", \"1\"],",
        f"\t\"trainset\": \"{train}\",",
        f"\t\"validset\": \"{valid}\",",
        f"\t\"testset\": \"{test}\"",
        "}"
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

config = open(IDUN_PATH + "ditto/configs.json", "w")
config.close()

config = open(IDUN_PATH + "ditto/configs.json", "a")
config.write("[ \n")

def make_files(task, train, test, valid):
    for i in range(10):
        output = "run_" + str(i+1)
        names.append(f"{task}_{output}")
        text = make_text(task, output)
        with open(IDUN_PATH + "ditto/jobs/" + task + "_" + output + ".slurm", "a") as job_file:
            for line in text: job_file.write(f"{line}\n")

    config_text = make_config(task, train, test, valid)
    for line in config_text: config.write(f"{line}\n")
    config.write(",\n")

for job in er_magellan:
    test = IDUN_PATH + "ditto/data/er_magellan/" + job + "/test.txt"
    valid = IDUN_PATH + "ditto/data/er_magellan/" + job + "/valid.txt"

    # Baseline
    task = job.replace("/", "_") + "_baseline"
    train = IDUN_PATH + "ditto/data/er_magellan/" + job + "/train.txt"
    make_files(task, train, test, valid)

    # GEN only
    task = job.replace("/", "_") + "_gen_only"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/augmented_only.txt"
    make_files(task, train, test, valid)

    # GEN only decimated
    task = job.replace("/", "_") + "_gen_only_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "_decimated/augmented_only.txt"
    make_files(task, train, test, valid)

    # Real + match 
    task = job.replace("/", "_") + "_real_pluss_match"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/real_pluss_match.txt"
    make_files(task, train, test, valid)

    # Real + match decimated
    task = job.replace("/", "_") + "_real_pluss_match_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "_decimated/real_pluss_match.txt"
    make_files(task, train, test, valid)

    # Real + non-match
    task = job.replace("/", "_") + "_real_pluss_non_match"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/real_pluss_non_match.txt"
    make_files(task, train, test, valid)

    # Real + non-match decimated
    task = job.replace("/", "_") + "_real_pluss_non_match_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "_decimated/real_pluss_non_match.txt"
    make_files(task, train, test, valid)

    # Real + all
    task = job.replace("/", "_") + "_real_pluss_all"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/real_pluss_all.txt"
    make_files(task, train, test, valid)

    # Real + all decimated
    task = job.replace("/", "_") + "_real_pluss_all_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "_decimated/real_pluss_all.txt"
    make_files(task, train, test, valid)


for job in wdc:
    test = IDUN_PATH + "ditto/data/wdc/" + job + "/test.txt"
    for size in sizes:
        valid = IDUN_PATH + "ditto/data/wdc/" + job + "/valid.txt." + size

        # Baseline
        task = job + "_" + size + "_baseline"
        train = IDUN_PATH + "ditto/data/wdc/" + job + "/train.txt." + size
        make_files(task, train, test, valid)

        # GEN only
        task = job + "_" + size + "_gen_only"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "/augmented_only.txt"
        make_files(task, train, test, valid)

        # GEN only decimated
        task = job + "_" + size + "_gen_only_decimated"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "_decimated/augmented_only.txt"
        make_files(task, train, test, valid)

        # Real + match 
        task = job + "_" + size + "_real_pluss_match"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "/real_pluss_match.txt"
        make_files(task, train, test, valid)

        # Real + match decimated
        task = job + "_" + size + "_real_pluss_match_decimated"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "_decimated/real_pluss_match.txt"
        make_files(task, train, test, valid)

        # Real + non-match
        task = job + "_" + size + "_real_pluss_match"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "/real_pluss_match.txt"
        make_files(task, train, test, valid)

        # Real + non-match decimated
        task = job + "_" + size + "_real_pluss_match_decimated"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "_decimated/real_pluss_match.txt"
        make_files(task, train, test, valid)
        
        # Real + all
        task = job + "_" + size + "_real_pluss_all"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "/real_pluss_all.txt"
        make_files(task, train, test, valid)

        # Real + all decimated
        task = job + "_" + size + "_real_pluss_all_decimated"
        train = IDUN_PATH + "Augmentation/Generated/" + job + "_" + size + "_decimated/real_pluss_all.txt"
        make_files(task, train, test, valid)

config.write("{}]")

config.close()

open(IDUN_PATH + "ditto/run_jobs.sh", "w").close() 
with open(IDUN_PATH + "ditto/run_jobs.sh", "a") as file: 
    for name in names: file.write(f"sbatch ./jobs/{name}.slurm danilasm\n")