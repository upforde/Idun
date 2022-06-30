import os, random

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

no_data = []

IDUN_PATH = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/'

for job in er_magellan:
    GENERATED_CTGAN_DIR = IDUN_PATH + f"Datasets_Synth/Ditto/CTGAN/{job}/"
    PROCESS_CTGAN_DIR = IDUN_PATH + f"Datasets_Synth/Scenarios/{job}/"
    os.makedirs(PROCESS_CTGAN_DIR, exist_ok=True)

    with open(IDUN_PATH + f"/Datasets/er_magellan/{job}/train.txt") as real_file:
        real_data = [line.replace("\n", "") for line in real_file.readlines()]

    with open(IDUN_PATH + f"/Datasets/er_magellan/{job}/train.txt.matches.decimated") as real_file_decimated:
        decimated_real_data = [line.replace("\n", "") for line in real_file_decimated.readlines()]

    with open(IDUN_PATH + f"/Datasets/er_magellan/{job}/train.txt.non_matches.decimated") as real_file_decimated:
        for line in real_file_decimated.readlines():
            decimated_real_data.append(line.replace("\n", ""))

     # Creating file to store all decimated data
    open(IDUN_PATH + f"/Datasets/er_magellan/{job}/train_decimated.txt", "w").close()
    with open(IDUN_PATH + f"/Datasets/er_magellan/{job}/train_decimated.txt", "a") as decimated:
        random.shuffle(decimated_real_data)
        for line in decimated_real_data: decimated.write(f"{line}\n")

    with open(GENERATED_CTGAN_DIR + "train.matches.txt") as generated_matches:
        matches = []
        for line in generated_matches.readlines():
            if line[:3] == "COL": matches.append(line.replace("\n", " "))
            else: matches[-1] += line.replace("\n", " ")
    if len(matches) == 0: no_data.append(f"{job} matches")

    with open(GENERATED_CTGAN_DIR + "train.non_matches.txt") as generated_non_matches:
        non_matches = []
        for line in generated_non_matches.readlines():
            if line[:3] == "COL": non_matches.append(line.replace("\n", " "))
            else: non_matches[-1] += line.replace("\n", " ")
    if len(non_matches) == 0: no_data.append(f"{job} non-matches")

    # GEN only
    if f"{job} matches" not in no_data and f"{job} non-matches" not in no_data:
        gen_only_data = matches + non_matches
        random.shuffle(gen_only_data)
        open(PROCESS_CTGAN_DIR + "gen_only.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "gen_only.txt", "a") as gen_only:
            for entry in gen_only_data: gen_only.write(f"{entry}\n")
        
    # Real + matches
    if f"{job} matches" not in no_data:
        rpm_data = real_data + matches
        random.shuffle(rpm_data)
        open(PROCESS_CTGAN_DIR + "real_plus_matches.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "real_plus_matches.txt", "a") as real_plus_matches:
            for entry in rpm_data: real_plus_matches.write(f"{entry}\n")

    # Real + non-matches
    if f"{job} non-matches" not in no_data:
        rpnm_data = real_data + non_matches
        random.shuffle(rpnm_data)
        open(PROCESS_CTGAN_DIR + "real_plus_non_matches.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "real_plus_non_matches.txt", "a") as real_plus_non_matches:
            for entry in rpnm_data: real_plus_non_matches.write(f"{entry}\n")

    # Real + all
    if f"{job} matches" not in no_data and f"{job} non-matches" not in no_data:
        rpa_data = real_data + matches + non_matches
        random.shuffle(rpa_data)
        open(PROCESS_CTGAN_DIR + "real_plus_all.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "real_plus_all.txt", "a") as real_plus_all:
            for entry in rpa_data: real_plus_all.write(f"{entry}\n")

    
    # Decimated FT
    with open(GENERATED_CTGAN_DIR + "train.matches.decimated.txt") as generated_decimated_matches:
        decimated_matches = []
        for line in generated_decimated_matches.readlines():
            if line[:3] == "COL": decimated_matches.append(line.replace("\n", " "))
            else: decimated_matches[-1] += line.replace("\n", " ")
    if len(decimated_matches) == 0: no_data.append(f"{job} matches decimated")

    with open(GENERATED_CTGAN_DIR + "train.non_matches.decimated.txt") as generated_decimated_non_matches:
        decimated_non_matches = []
        for line in generated_decimated_non_matches.readlines():
            if line[:3] == "COL": decimated_non_matches.append(line.replace("\n", " "))
            else: decimated_non_matches[-1] += line.replace("\n", " ")
    if len(decimated_non_matches) == 0: no_data.append(f"{job} non-matches decimated")

    # GEN only
    if f"{job} matches decimated" not in no_data and f"{job} non-matches decimated" not in no_data:
        gen_only_data = decimated_matches + decimated_non_matches
        random.shuffle(gen_only_data)
        open(PROCESS_CTGAN_DIR + "gen_only_decimated.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "gen_only_decimated.txt", "a") as gen_only:
            for entry in gen_only_data: gen_only.write(f"{entry}\n")
        
    # Real + matches
    if f"{job} matches decimated" not in no_data:
        rpm_data = decimated_real_data + decimated_matches
        random.shuffle(rpm_data)
        open(PROCESS_CTGAN_DIR + "real_plus_matches_decimated.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "real_plus_matches_decimated.txt", "a") as real_plus_matches:
            for entry in rpm_data: real_plus_matches.write(f"{entry}\n")

    # Real + non-matches
    if f"{job} non-matches decimated" not in no_data:
        rpnm_data = decimated_real_data + decimated_non_matches
        random.shuffle(rpnm_data)
        open(PROCESS_CTGAN_DIR + "real_plus_non_matches_decimated.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "real_plus_non_matches_decimated.txt", "a") as real_plus_non_matches:
            for entry in rpnm_data: real_plus_non_matches.write(f"{entry}\n")

    # Real + all
    if f"{job} matches decimated" not in no_data and f"{job} non-matches decimated" not in no_data:
        rpa_data = decimated_real_data + decimated_matches + decimated_non_matches
        random.shuffle(rpa_data)
        open(PROCESS_CTGAN_DIR + "real_plus_all_decimated.txt", "w").close()
        with open(PROCESS_CTGAN_DIR + "real_plus_all_decimated.txt", "a") as real_plus_all:
            for entry in rpa_data: real_plus_all.write(f"{entry}\n")

if len(no_data) != 0: 
    print("Missing data:")
    for job in no_data: print(f"\t{job}")