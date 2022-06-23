new_gpt2_ft = []
new_gpt2_nft = []

missing = open("./run_missing.sh").readlines()

with open("./run_gpt2_ft_jobs.sh") as gpt2:
    for line in gpt2.readlines():
        if line not in missing:
            new_gpt2_ft.append(line)

with open("./run_gpt2_nft_jobs.sh") as gpt2:
    for line in gpt2.readlines():
        if line not in missing:
            new_gpt2_nft.append(line)


open("./run_gpt2_ft_jobs.sh", "w").close()
with open("./run_gpt2_ft_jobs.sh", "a")as ft: ft.write("#!/bin/sh\n")
with open("./run_gpt2_ft_jobs.sh", "a") as gpt2:
    for line in new_gpt2_ft:
        gpt2.write(line)

open("./run_gpt2_nft_jobs.sh", "w").close()
with open("./run_gpt2_nft_jobs.sh", "a")as nft: nft.write("#!/bin/sh\n")
with open("./run_gpt2_nft_jobs.sh", "a") as gpt2:
    for line in new_gpt2_nft:
        gpt2.write(line)
