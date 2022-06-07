import os, shutil
import numpy

# IDUN_PATH = "/cluster/home/danilasm/masters/Idun/"
IDUN_PATH = "../"

if not os.path.exists(IDUN_PATH + "GPT-2/processed_generated"):
    os.makedirs(IDUN_PATH + "GPT-2/processed_generated")

if len(os.listdir(IDUN_PATH + "GPT-2/processed_generated")) != 0:
    shutil.rmtree(IDUN_PATH + "GPT-2/processed_generated")
    os.makedirs(IDUN_PATH + "GPT-2/processed_generated")

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

no_data = []

for job in er_magellan:
    GENERATED_FT_DIR = IDUN_PATH + f"GPT-2/Generated/{job}/fine_tuned/"
    GENERATED_NFT_DIR = IDUN_PATH + f"GPT-2/Generated/{job}/non_fine_tuned/"
    FINE_TUNED_DIR = IDUN_PATH + f"GPT-2/processed_generated/{job}/fine_tuned/"
    NON_FINE_TUNED_DIR = IDUN_PATH + f"GPT-2/processed_generated/{job}/non_fine_tuned/"
    os.makedirs(FINE_TUNED_DIR)
    os.makedirs(NON_FINE_TUNED_DIR)

    with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt") as real_file:
        real_data = [line.replace("\n", "") for line in real_file.readlines()]

    with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.matches.decimated") as real_file_decimated:
        decimated_real_data = [line.replace("\n", "") for line in real_file_decimated.readlines()]
    with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.non_matches.decimated") as real_file_decimated:
        for line in real_file_decimated.readlines():
            decimated_real_data.append(line.replace("\n", ""))

    # Fine-tuned
    with open(GENERATED_FT_DIR + "matches.txt") as generated_matches_ft:
        ft_matches = []
        for line in generated_matches_ft.readlines():
            if line[:3] == "COL": ft_matches.append(line.replace("\n", " "))
            else: ft_matches[-1] += line.replace("\n", " ")
    if len(ft_matches) == 0: no_data.append(f"{job} fine-tuned matches")

    with open(GENERATED_FT_DIR + "non_matches.txt") as generated_non_matches_ft:
        ft_non_matches = []
        for line in generated_non_matches_ft.readlines():
            if line[:3] == "COL": ft_non_matches.append(line.replace("\n", " "))
            else: ft_non_matches[-1] += line.replace("\n", " ")
    if len(ft_non_matches) == 0: no_data.append(f"{job} fine-tuned non-matches")

    # GEN only
    if f"{job} fine-tuned matches" not in no_data and f"{job} fine-tuned non-matches" not in no_data:
        open(FINE_TUNED_DIR + "gen_only.txt", "w").close()
        with open(FINE_TUNED_DIR + "gen_only.txt", "a") as gen_only:
            for entry in ft_matches: gen_only.write(f"{entry}\n")
            for entry in ft_non_matches: gen_only.write(f"{entry}\n")
        
    # Real + matches
    if f"{job} fine-tuned matches" not in no_data:
        open(FINE_TUNED_DIR + "real_plus_matches.txt", "w").close()
        with open(FINE_TUNED_DIR + "real_plus_matches.txt", "a") as real_plus_matches:
            for entry in real_data: real_plus_matches.write(f"{entry}\n")
            for entry in ft_matches: real_plus_matches.write(f"{entry}\n")

    # Real + non-matches
    if f"{job} fine-tuned non-matches" not in no_data:
        open(FINE_TUNED_DIR + "real_plus_non_matches.txt", "w").close()
        with open(FINE_TUNED_DIR + "real_plus_non_matches.txt", "a") as real_plus_non_matches:
            for entry in real_data: real_plus_non_matches.write(f"{entry}\n")
            for entry in ft_non_matches: real_plus_non_matches.write(f"{entry}\n")

    # Real + all
    if f"{job} fine-tuned matches" not in no_data and f"{job} fine-tuned non-matches" not in no_data:
        open(FINE_TUNED_DIR + "real_plus_all.txt", "w").close()
        with open(FINE_TUNED_DIR + "real_plus_all.txt", "a") as real_plus_all:
            for entry in real_data: real_plus_all.write(f"{entry}\n")
            for entry in ft_matches: real_plus_all.write(f"{entry}\n")
            for entry in ft_non_matches: real_plus_all.write(f"{entry}\n")

    
    # Decimated FT
    with open(GENERATED_FT_DIR + "matches_decimated.txt") as generated_decimated_matches_ft:
        ft_decimated_matches = []
        for line in generated_decimated_matches_ft.readlines():
            if line[:3] == "COL": ft_decimated_matches.append(line.replace("\n", " "))
            else: ft_decimated_matches[-1] += line.replace("\n", " ")
    if len(ft_decimated_matches) == 0: no_data.append(f"{job} fine-tuned matches decimated")

    with open(GENERATED_FT_DIR + "non_matches_decimated.txt") as generated_decimated_non_matches_ft:
        ft_decimated_non_matches = []
        for line in generated_decimated_non_matches_ft.readlines():
            if line[:3] == "COL": ft_decimated_non_matches.append(line.replace("\n", " "))
            else: ft_decimated_non_matches[-1] += line.replace("\n", " ")
    if len(ft_decimated_non_matches) == 0: no_data.append(f"{job} fine-tuned non-matches decimated")

    # GEN only
    if f"{job} fine-tuned matches decimated" not in no_data and f"{job} fine-tuned non-matches decimated" not in no_data:
        open(FINE_TUNED_DIR + "gen_only_decimated.txt", "w").close()
        with open(FINE_TUNED_DIR + "gen_only_decimated.txt", "a") as gen_only:
            for entry in ft_decimated_matches: gen_only.write(f"{entry}\n")
            for entry in ft_decimated_non_matches: gen_only.write(f"{entry}\n")
        
    # Real + matches
    if f"{job} fine-tuned matches decimated" not in no_data:
        open(FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "w").close()
        with open(FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "a") as real_plus_matches:
            for entry in decimated_real_data: real_plus_matches.write(f"{entry}\n")
            for entry in ft_decimated_matches: real_plus_matches.write(f"{entry}\n")

    # Real + non-matches
    if f"{job} fine-tuned non-matches decimated" not in no_data:
        open(FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "w").close()
        with open(FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "a") as real_plus_non_matches:
            for entry in decimated_real_data: real_plus_non_matches.write(f"{entry}\n")
            for entry in ft_decimated_non_matches: real_plus_non_matches.write(f"{entry}\n")

    # Real + all
    if f"{job} fine-tuned matches decimated" not in no_data and f"{job} fine-tuned non-matches decimated" not in no_data:
        open(FINE_TUNED_DIR + "real_plus_all_decimated.txt", "w").close()
        with open(FINE_TUNED_DIR + "real_plus_all_decimated.txt", "a") as real_plus_all:
            for entry in decimated_real_data: real_plus_all.write(f"{entry}\n")
            for entry in ft_decimated_matches: real_plus_all.write(f"{entry}\n")
            for entry in ft_decimated_non_matches: real_plus_all.write(f"{entry}\n")


    # Non-fine-tuned
    with open(GENERATED_NFT_DIR + "matches.txt") as generated_matches_nft:
        nft_matches = []
        for line in generated_matches_nft.readlines():
            if line[:3] == "COL": nft_matches.append(line.replace("\n", " "))
            else: nft_matches[-1] += line.replace("\n", " ")
    if len(nft_matches) == 0: no_data.append(f"{job} non-fine-tuned matches")

    with open(GENERATED_NFT_DIR + "non_matches.txt") as generated_non_matches_nft:
        nft_non_matches = []
        for line in generated_non_matches_nft.readlines():
            if line[:3] == "COL": nft_non_matches.append(line.replace("\n", " "))
            else: nft_non_matches[-1] += line.replace("\n", " ")
    if len(nft_non_matches) == 0: no_data.append(f"{job} non-fine-tuned non-matches")

    # GEN only
    if f"{job} non-fine-tuned matches" not in no_data and f"{job} non-fine-tuned non-matches" not in no_data:
        open(NON_FINE_TUNED_DIR + "gen_only.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "gen_only.txt", "a") as gen_only:
            for entry in nft_matches: gen_only.write(f"{entry}\n")
            for entry in nft_non_matches: gen_only.write(f"{entry}\n")
        
    # Real + matches
    if f"{job} non-fine-tuned matches" not in no_data:
        open(NON_FINE_TUNED_DIR + "real_plus_matches.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "real_plus_matches.txt", "a") as real_plus_matches:
            for entry in real_data: real_plus_matches.write(f"{entry}\n")
            for entry in nft_matches: real_plus_matches.write(f"{entry}\n")

    # Real + non-matches
    if f"{job} non-fine-tuned non-matches" not in no_data:
        open(NON_FINE_TUNED_DIR + "real_plus_non_matches.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "real_plus_non_matches.txt", "a") as real_plus_non_matches:
            for entry in real_data: real_plus_non_matches.write(f"{entry}\n")
            for entry in nft_non_matches: real_plus_non_matches.write(f"{entry}\n")

    # Real + all
    if f"{job} non-fine-tuned matches" not in no_data and f"{job} non-fine-tuned non-matches" not in no_data:
        open(NON_FINE_TUNED_DIR + "real_plus_all.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "real_plus_all.txt", "a") as real_plus_all:
            for entry in real_data: real_plus_all.write(f"{entry}\n")
            for entry in nft_matches: real_plus_all.write(f"{entry}\n")
            for entry in nft_non_matches: real_plus_all.write(f"{entry}\n")
    

    # Decimated NFT
    with open(GENERATED_NFT_DIR + "matches_decimated.txt") as generated_decimated_matches_nft:
        nft_decimated_matches = []
        for line in generated_decimated_matches_nft.readlines():
            if line[:3] == "COL": nft_decimated_matches.append(line.replace("\n", " "))
            else: nft_decimated_matches[-1] += line.replace("\n", " ")
    if len(nft_decimated_matches) == 0: no_data.append(f"{job} non-fine-tuned matches decimated")

    with open(GENERATED_NFT_DIR + "non_matches_decimated.txt") as generated_decimated_non_matches_nft:
        nft_decimated_non_matches = []
        for line in generated_decimated_non_matches_nft.readlines():
            if line[:3] == "COL": nft_decimated_non_matches.append(line.replace("\n", " "))
            else: nft_decimated_non_matches[-1] += line.replace("\n", " ")
    if len(nft_decimated_non_matches) == 0: no_data.append(f"{job} non-fine-tuned non-matches decimated")
    
    # GEN only
    if f"{job} non-fine-tuned matches decimated" not in no_data and f"{job} non-fine-tuned non-matches decimated" not in no_data:
        open(NON_FINE_TUNED_DIR + "gen_only_decimated.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "gen_only_decimated.txt", "a") as gen_only:
            for entry in nft_decimated_matches: gen_only.write(f"{entry}\n")
            for entry in nft_decimated_non_matches: gen_only.write(f"{entry}\n")
        
    # Real + matches
    if f"{job} non-fine-tuned matches decimated" not in no_data:
        open(NON_FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "a") as real_plus_matches:
            for entry in decimated_real_data: real_plus_matches.write(f"{entry}\n")
            for entry in nft_decimated_matches: real_plus_matches.write(f"{entry}\n")

    # Real + non-matches
    if f"{job} non-fine-tuned non-matches decimated" not in no_data:
        open(NON_FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "a") as real_plus_non_matches:
            for entry in decimated_real_data: real_plus_non_matches.write(f"{entry}\n")
            for entry in nft_decimated_non_matches: real_plus_non_matches.write(f"{entry}\n")

    # Real + all
    if f"{job} non-fine-tuned matches decimated" not in no_data and f"{job} non-fine-tuned non-matches decimated" not in no_data:
        open(NON_FINE_TUNED_DIR + "real_plus_all_decimated.txt", "w").close()
        with open(NON_FINE_TUNED_DIR + "real_plus_all_decimated.txt", "a") as real_plus_all:
            for entry in decimated_real_data: real_plus_all.write(f"{entry}\n")
            for entry in nft_decimated_matches: real_plus_all.write(f"{entry}\n")
            for entry in nft_decimated_non_matches: real_plus_all.write(f"{entry}\n")

print(no_data)