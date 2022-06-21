new_gpt2_ft = []
new_gpt2_nft = []

with open("./run_missing.sh") as missing:
    missing_lines = missing.readlines()
    with open("./run_gpt2_ft_jobs.sh") as gpt2:
        for line in gpt2.readlines():
            if line not in missing_lines:
                new_gpt2_ft.append(line)
    with open("./run_gpt2_nft_jobs.sh") as gpt2:
        for line in gpt2.readlines():
            if line not in missing_lines:
                new_gpt2_nft.append(line)


open("./run_gpt2_ft_jobs.sh", "w").close()
with open("./run_gpt2_ft_jobs.sh", "a") as gpt2:
    for line in new_gpt2_ft:
        gpt2.write(line + "\n")

open("./run_gpt2_nft_jobs.sh", "w").close()
with open("./run_gpt2_nft_jobs.sh", "a") as gpt2:
    for line in new_gpt2_ft:
        gpt2.write(line + "\n")
