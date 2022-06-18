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
    python_line += f" --run_id={seed}"

    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=12:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --mem=12000",
        f"#SBATCH --job-name=\"ditto {task}\"",
        f"#SBATCH --output=Output/{task}",
        "#SBATCH --mail-user=danilasm@stud.ntnu.no",
        "#SBATCH --mail-type=ALL",
        "module purge",
        "module load Anaconda3/2020.07",
        "source /cluster/home/danilasm/.bashrc",
        "source activate masters",
        "module load CUDA/11.1.1-GCC-10.2.0",

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

names = []

open(IDUN_PATH + "ditto/configs.json", "w").close()

config = open(IDUN_PATH + "ditto/configs.json", "a")
config.write("[ \n")

def make_files(task, train, test, valid):
    for i in range(3):
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
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_gen_only"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/gen_only.txt"
    make_files(task, train, test, valid)

    # GPT-2 
    task = "GPT-2_" + job.replace("/", "_") + "_gen_only_ft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/gen_only.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_gen_only_nft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/gen_only.txt"
    make_files(task, train, test, valid)

    # CTGAN
    # -------- Your code here --------

    # GEN only decimated
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_gen_only_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/gen_only_decimated.txt"
    make_files(task, train, test, valid)

    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_gen_only_ft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/gen_only_decimated.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_gen_only_nft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/gen_only_decimated.txt"
    make_files(task, train, test, valid)

    # CTGAN
    # -------- Your code here --------


    # Real + match 
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_real_plus_matches"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/real_plus_matches.txt"
    make_files(task, train, test, valid)

    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_matches_ft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/real_plus_matches.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_matches_nft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/real_plus_matches.txt"
    make_files(task, train, test, valid)

    # CTGAN
    # -------- Your code here --------

    # Real + match decimated
    # Augmentaion
    task = "Augmentation_" + job.replace("/", "_") + "_real_plus_matches_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "real_plus_matches_decimated.txt"
    make_files(task, train, test, valid)
    
    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_matches_ft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/real_plus_matches_decimated.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_matches_nft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/real_plus_matches_decimated.txt"
    make_files(task, train, test, valid)


    # CTGAN
    # -------- Your code here --------

    # Real + non-match
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_real_plus_non_matches"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/real_plus_non_matches.txt"
    make_files(task, train, test, valid)

    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_non_matches_ft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/real_plus_non_matches.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_non_matches_nft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/real_plus_non_matches.txt"
    make_files(task, train, test, valid)

    # CTGAN
    # -------- Your code here --------

    # Real + non-match decimated
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_real_plus_non_matches_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "_decimated/real_plus_non_matches.txt"
    make_files(task, train, test, valid)

    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_non_matches_ft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/real_plus_matches_non_decimated.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_non_matches_nft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/real_plus_non_matches_decimated.txt"
    make_files(task, train, test, valid)

    # CTGAN
    # -------- Your code here --------

    # Real + all
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_real_plus_all"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "/real_plus_all.txt"
    make_files(task, train, test, valid)

    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_all_ft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/real_plus_all.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_all_nft"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/real_plus_all.txt"
    make_files(task, train, test, valid)


    # CTGAN
    # -------- Your code here --------

    # Real + all decimated
    # Augmentation
    task = "Augmentation_" + job.replace("/", "_") + "_real_plus_all_decimated"
    train = IDUN_PATH + "Augmentation/Generated/" + job + "_decimated/real_plus_all.txt"
    make_files(task, train, test, valid)

    # GPT-2
    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_all_ft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/fine_tuned/real_plus_all_decimated.txt"
    make_files(task, train, test, valid)

    task = "GPT-2_" + job.replace("/", "_") + "_real_plus_all_nft_decimated"
    train = IDUN_PATH + "GPT-2/Processed_Generated/" + job + "/non_fine_tuned/real_plus_all_decimated.txt"
    make_files(task, train, test, valid)

    # CTGAN
    # -------- Your code here --------

config.write("{\"name\":\"eof\"}]")

config.close()

open(IDUN_PATH + "ditto/run_jobs.sh", "w").close() 
with open(IDUN_PATH + "ditto/run_jobs.sh", "a") as file: 
    for name in names: file.write(f"sbatch ./jobs/{name}.slurm danilasm\n")