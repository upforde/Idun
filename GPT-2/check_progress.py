import os, shutil
import numpy

# IDUN_PATH = "/cluster/home/danilasm/masters/Idun/"
IDUN_PATH = "../"

if not os.path.exists(IDUN_PATH + "GPT-2/Processed_Generated"):
    os.makedirs(IDUN_PATH + "GPT-2/Processed_Generated")

if len(os.listdir(IDUN_PATH + "GPT-2/Processed_Generated")) != 0:
    shutil.rmtree(IDUN_PATH + "GPT-2/Processed_Generated")
    os.makedirs(IDUN_PATH + "GPT-2/Processed_Generated")

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

progress = []

for job in er_magellan:
    GENERATED_FT_DIR = IDUN_PATH + f"GPT-2/Generated/{job}/fine_tuned/"
    GENERATED_NFT_DIR = IDUN_PATH + f"GPT-2/Generated/{job}/non_fine_tuned/"

    with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt") as real_file:
        real_data = [line.replace("\n", "") for line in real_file.readlines()]

    real_matches, real_non_matches = [], []
    for data in real_data:
        if str(1) in data.split("\t")[2]:
            real_matches.append(data)
        else: real_non_matches.append(data)
        

    with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.matches.decimated") as real_file_decimated:
        decimated_real_data = [line.replace("\n", "") for line in real_file_decimated.readlines()]
    with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.non_matches.decimated") as real_file_decimated:
        for line in real_file_decimated.readlines():
            decimated_real_data.append(line.replace("\n", ""))

    real_matches_decimated, real_non_matches_decimated = [], []
    for data in decimated_real_data:
        if str(1) in data.split("\t")[2]:
            real_matches_decimated.append(data)
        else: real_non_matches_decimated.append(data)

    # Fine-tuned
    with open(GENERATED_FT_DIR + "matches.txt") as generated_matches_ft:
        ft_matches = []
        for line in generated_matches_ft.readlines():
            if line[:3] == "COL": ft_matches.append(line.replace("\n", " "))
            else: ft_matches[-1] += line.replace("\n", " ")
    if len(ft_matches) < len(real_matches): progress.append(f"{job} fine-tuned matches progress:\t{round(len(ft_matches)/len(real_matches)*100, 2)}%")

    with open(GENERATED_FT_DIR + "non_matches.txt") as generated_non_matches_ft:
        ft_non_matches = []
        for line in generated_non_matches_ft.readlines():
            if line[:3] == "COL": ft_non_matches.append(line.replace("\n", " "))
            else: ft_non_matches[-1] += line.replace("\n", " ")
    if len(ft_non_matches) < len(real_non_matches): progress.append(f"{job} fine-tuned non-matches progress:\t{round(len(ft_non_matches)/len(real_non_matches)*100, 2)}%")
    
    # Decimated FT
    with open(GENERATED_FT_DIR + "matches_decimated.txt") as generated_decimated_matches_ft:
        ft_decimated_matches = []
        for line in generated_decimated_matches_ft.readlines():
            if line[:3] == "COL": ft_decimated_matches.append(line.replace("\n", " "))
            else: ft_decimated_matches[-1] += line.replace("\n", " ")
    if len(ft_decimated_matches) < len(real_matches): progress.append(f"{job} fine-tuned decimated matches progress:\t{round(len(ft_decimated_matches)/len(real_matches)*100, 2)}%")

    with open(GENERATED_FT_DIR + "non_matches_decimated.txt") as generated_decimated_non_matches_ft:
        ft_decimated_non_matches = []
        for line in generated_decimated_non_matches_ft.readlines():
            if line[:3] == "COL": ft_decimated_non_matches.append(line.replace("\n", " "))
            else: ft_decimated_non_matches[-1] += line.replace("\n", " ")
    if len(ft_decimated_non_matches) < len(real_non_matches): progress.append(f"{job} fine-tuned decimated non-matches progress:\t{round(len(ft_decimated_non_matches)/len(real_non_matches)*100, 2)}%")


    # Non-fine-tuned
    with open(GENERATED_NFT_DIR + "matches.txt") as generated_matches_nft:
        nft_matches = []
        for line in generated_matches_nft.readlines():
            if line[:3] == "COL": nft_matches.append(line.replace("\n", " "))
            else: nft_matches[-1] += line.replace("\n", " ")
    if len(nft_matches) < len(real_matches): progress.append(f"{job} non-fine-tuned matches progress:\t{round(len(nft_matches)/len(real_matches)*100, 2)}%")


    with open(GENERATED_NFT_DIR + "non_matches.txt") as generated_non_matches_nft:
        nft_non_matches = []
        for line in generated_non_matches_nft.readlines():
            if line[:3] == "COL": nft_non_matches.append(line.replace("\n", " "))
            else: nft_non_matches[-1] += line.replace("\n", " ")
    if len(nft_non_matches) < len(real_non_matches): progress.append(f"{job} non-fine-tuned non-matches progress:\t{round(len(nft_non_matches)/len(real_non_matches)*100, 2)}%")

    # Decimated NFT
    with open(GENERATED_NFT_DIR + "matches_decimated.txt") as generated_decimated_matches_nft:
        nft_decimated_matches = []
        for line in generated_decimated_matches_nft.readlines():
            if line[:3] == "COL": nft_decimated_matches.append(line.replace("\n", " "))
            else: nft_decimated_matches[-1] += line.replace("\n", " ")
    if len(nft_decimated_matches) < len(real_matches): progress.append(f"{job} non-fine-tuned decimated matches progress:\t{round(len(nft_decimated_matches)/len(real_matches)*100, 2)}%")

    with open(GENERATED_NFT_DIR + "non_matches_decimated.txt") as generated_decimated_non_matches_nft:
        nft_decimated_non_matches = []
        for line in generated_decimated_non_matches_nft.readlines():
            if line[:3] == "COL": nft_decimated_non_matches.append(line.replace("\n", " "))
            else: nft_decimated_non_matches[-1] += line.replace("\n", " ")
    if len(nft_decimated_non_matches) < len(real_non_matches): progress.append(f"{job} non-fine-tuned decimated non-matches progress:\t{round(len(nft_decimated_non_matches)/len(real_non_matches)*100, 2)}%")
    
for name in progress:
    print(name)