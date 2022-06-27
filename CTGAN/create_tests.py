import os

def make_text(output, dataset, job_type=0, generator_type=0):
    generator_text = [
        r"CTGAN",
        r"GPT-2_ft",
        r"GPT-2_nft",
        r"Augmentation"
    ]

    job_text = [
        r"Baseline",
        r"matches_non-matches",
        r"real_data_matches",
        r"real_data_non-matches",
        r"real_data_matches_non-matches",
        r"decimate_Baseline",
        r"decimate_matches_non-matches",
        r"decimate_real_data_matches",
        r"decimate_real_data_non-matches",
        r"decimate_real_data_matches_non-matches"
    ]

    script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Magellan_testing.py"
    python_line = f"python3 \"{script_path}\" --dataset=\"{dataset}\" --job_type={job_type} --generator_type={generator_type}"
    text = [
        "#!/bin/sh",
        "#SBATCH --partition=GPUQ",
        "#SBATCH --account=ie-idi",
        "#SBATCH --time=04:00:00",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks-per-node=1",
        "#SBATCH --gres=gpu:V10032:1",
        f"#SBATCH --job-name=\"Testing {job_text[job_type]} {dataset} {generator_text[generator_type]} \"",
        f"#SBATCH --output={output}",
        "#SBATCH --mail-user=alekssim@stud.ntnu.no",
        "#SBATCH --mail-type=ALL",
        
        "module purge",
        "module load Anaconda3/2020.07",
        "module load Python/3.8.6-GCCcore-10.2.0",
        "pip3 install pandas --user",
        "pip3 install numpy==1.21",
        "pip3 install scipy",
        "pip3 install py_entitymatching",
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

generator_type = [
    r"CTGAN",
    r"GPT-2_ft",
    r"GPT-2_nft",
    r"Augmentation"
]

data_scenario = [
        r"Baseline",
        r"matches_non-matches",
        r"real_data_matches",
        r"real_data_non-matches",
        r"real_data_matches_non-matches",
        r"decimate_Baseline",
        r"decimate_matches_non-matches",
        r"decimate_real_data_matches",
        r"decimate_real_data_non-matches",
        r"decimate_real_data_matches_non-matches"
    ]

names = []

jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/'

for i in range(0, 4):
    for j in range(0, 10):
        for job in er_magellan:
            name = jobs_dir + generator_type[i] + os.sep + job.replace(os.sep, "_") + data_scenario[j]
            names.append(name)
            text = make_text(name + ".out", job, j, i)
            with open(name + ".slurm", "a") as file:
                for line in text:
                    file.write(f"{line}\n")

with open("run_match_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sbatch {name}.slurm alekssim\n")