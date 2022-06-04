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

no_data = []

for job in er_magellan:
    FINE_TUNED_DIR = IDUN_PATH + f"GPT-2/processed_generated/{job}/fine_tuned/"
    NON_FINE_TUNED_DIR = IDUN_PATH + f"GPT-2/processed_generated/{job}/non_fine_tuned/"
    os.makedirs(FINE_TUNED_DIR)
    os.makedirs(NON_FINE_TUNED_DIR)
    # Fine tuned
    try:
        # Open the files
        with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt") as real_file:
            real_data = [line for line in real_file.readlines()]
        
        with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches.txt") as generated_matches_ft:
            generated_matches_ft_data = [line for line in generated_matches_ft.readlines()]

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/non_matches.txt") as generated_non_matches_ft:
            generated_non_matches_ft_data = [line for line in generated_non_matches_ft.readlines()]

        # Create datasets
        # GEN only
        gen_only_ft = numpy.concatenate(generated_matches_ft_data, generated_non_matches_ft_data)
        with open(FINE_TUNED_DIR + "gen_only.txt", "a") as file:
            for line in gen_only_ft: file.write(f"{line}\n")

        # Real + matches
        real_plus_matches_ft = numpy.concatenate(real_data, generated_matches_ft_data)
        with open(FINE_TUNED_DIR + "real_plus_matches.txt", "a") as file:
            for line in real_plus_matches_ft: file.write(f"{line}\n")

        # Real + non-matches
        real_plus_non_matches_ft = numpy.concatenate(real_data, generated_non_matches_ft_data)
        with open(FINE_TUNED_DIR + "real_plus_non_matches.txt", "a") as file:
            for line in real_plus_non_matches_ft: file.write(f"{line}\n")

        # Real + all
        real_plus_all_ft = numpy.concatenate(real_data, generated_matches_ft_data, generated_non_matches_ft_data)
        with open(FINE_TUNED_DIR + "real_pluss_all.txt", "a") as file:
            for line in real_plus_all_ft: file.write(f"{line}\n")

    except:
        no_data.append("ft " + job)

    # Non-fine tuned
    try:
        with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt") as real_file:
            real_data = [line for line in real_file.readlines()]

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches.txt") as generated_matches_nft:
            generated_matches_nft_data = [line for line in generated_matches_nft.readlines()]

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/non_matches.txt") as generated_non_matches_nft:
            generated_non_matches_nft_data = [line for line in generated_non_matches_nft.readlines()]

        # GEN only
        gen_only_nft = numpy.concatenate(generated_matches_nft_data, generated_non_matches_nft_data)
        with open(NON_FINE_TUNED_DIR + "gen_only.txt", "a") as file:
            for line in gen_only_nft: file.write(f"{line}\n")

        # Real + matches
        real_plus_matches_nft = numpy.concatenate(real_data, generated_matches_nft_data)
        with open(NON_FINE_TUNED_DIR + "real_plus_matches.txt", "a") as file:
             for line in real_plus_matches_nft: file.write(f"{line}\n")

        # Real + non_matches
        real_plus_non_matches_nft = numpy.concatenate(real_data, generated_non_matches_nft_data)
        with open(NON_FINE_TUNED_DIR + "real_plus_non_matches.txt", "a") as file:
            for line in real_plus_non_matches_nft: file.write(f"{line}\n")

        # Real + all
        real_plus_all_nft = numpy.concatenate(real_data, generated_matches_nft_data, generated_non_matches_nft_data)
        with open(NON_FINE_TUNED_DIR + "real_plus_all.txt", "a") as file:
            for line in real_plus_all_nft: file.write(f"{line}\n")
        
    except:
        no_data.append("nft " + job)

    # Fine tuned decimated
    try:
        with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.matches.decimated") as real_file_decimated:
            real_data_decimated = [line for line in real_file_decimated.reallines()]
        
        with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.non_matches.decimated") as real_file_decimated:
            for line in real_file_decimated.readlines(): real_data_decimated.append(line)

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches_decimated.txt") as generated_matches_decimated_ft:
            generated_matches_decimated_ft_data = [line for line in generated_matches_decimated_ft.readlines()]

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/non_matches_decimated.txt") as generated_non_matches_decimated_ft:
            generated_non_matches_decimated_ft_data = [line for line in generated_non_matches_decimated_ft]

        # GEN only
        gen_only_decimated_ft = numpy.concatenate(generated_matches_decimated_ft_data, generated_non_matches_decimated_ft_data)
        with open(FINE_TUNED_DIR + "gen_only_decimated.txt") as file:
            for line in gen_only_decimated_ft: file.write(f"{line}\n")

        # Real + matches
        real_plus_matches_decimated_ft = numpy.concatenate(real_data_decimated, generated_matches_decimated_ft_data)
        with open(FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "a") as file:
            for line in real_plus_matches_decimated_ft: file.write(f"{line}\n")
        
        # Real + non_matches
        real_plus_non_matches_decimated_ft = numpy.concatenate(real_data_decimated, generated_non_matches_decimated_ft_data)
        with open(FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "a") as file:
            for line in real_plus_non_matches_decimated_ft: file.write(f"{line}\n")

        # Real + all
        real_plus_all_decimated_ft = numpy.concatenate(real_data_decimated, generated_matches_decimated_ft_data, generated_non_matches_decimated_ft_data)
        with open(FINE_TUNED_DIR + "real_plus_all_decimated.txt", "a") as file:
            for line in real_plus_all_decimated_ft: file.write(f"{line}\n")

    except:
        no_data.append("ft " + job + " decimated")

    # Non-fine tuned decimated
    try:
        with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.matches.decimated") as real_file_decimated:
            real_data_decimated = [line for line in real_file_decimated.reallines()]
        
        with open(IDUN_PATH + f"GPT-2/Datasets/er_magellan/{job}/train.txt.non_matches.decimated") as real_file_decimated:
            for line in real_file_decimated.readlines(): real_data_decimated.append(line)

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches_decimated_nft.txt") as generated_matches_decimated_nft:
            generated_matches_decimated_nft_data = [line for line in generated_matches_decimated_nft]

        with open(IDUN_PATH + f"GPT-2/Generated/{job}/non_matches_decimated_nft.txt") as generated_non_matches_decimated_nft:
            generated_non_matches_decimated_nft_data = [line for line in generated_non_matches_decimated_nft.readlines()]

        # GEN only
        gen_only_decimated_nft = numpy.concatenate(generated_matches_decimated_nft_data, generated_non_matches_decimated_nft_data)
        with open(NON_FINE_TUNED_DIR + "gen_only_decimated.txt") as file:
            for line in gen_only_decimated_nft: file.write(f"{line}\n")

        # Real + matches
        real_plus_matches_decimated_nft = numpy.concatenate(real_data_decimated, generated_matches_decimated_nft_data)
        with open(NON_FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "a") as file:
            for line in real_plus_matches_decimated_nft: file.write(f"{line}\n")

        # Real + non_matches
        real_plus_non_matches_decimated_nft = numpy.concatenate(real_data_decimated, generated_non_matches_decimated_nft_data)
        with open(NON_FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "a") as file:
            for line in real_plus_non_matches_decimated_nft: file.write(f"{line}\n")

        # Real + all
        real_plus_all_decimated_nft = numpy.concatenate(real_data_decimated, generated_matches_decimated_nft_data, generated_non_matches_decimated_nft_data)
        with open(NON_FINE_TUNED_DIR + "real_plus_all_decimated.txt", "a") as file:
            for line in real_plus_all_decimated_nft: file.write(f"{line}\n")

    except:
        no_data.append("nft " + job + " decimated")

for job in wdc:
    for size in sizes:
        FINE_TUNED_DIR = IDUN_PATH + f"GPT-2/processed_generated/{job}/{size}/fine_tuned/"
        NON_FINE_TUNED_DIR = IDUN_PATH + f"GPT-2/processed_generated/{job}/{size}/non_fine_tuned/"
        os.makedirs(FINE_TUNED_DIR)
        os.makedirs(NON_FINE_TUNED_DIR)
        # Fine tuned
        try:
            # Open the files
            with open(IDUN_PATH + f"GPT-2/Datasets/wdc/{job}/train.txt.{size}") as real_file:
                real_data = [line for line in real_file.readlines()]
            
            with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches_{size}.txt") as generated_matches_ft:
                generated_matches_ft_data = [line for line in generated_matches_ft.readlines()]

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/non_matches_{size}.txt") as generated_non_matches_ft:
                generated_non_matches_ft_data = [line for line in generated_non_matches_ft.readlines()]

            # Create datasets
            # GEN only
            gen_only_ft = numpy.concatenate(generated_matches_ft_data, generated_non_matches_ft_data)
            with open(FINE_TUNED_DIR + "gen_only.txt", "a") as file:
                for line in gen_only_ft: file.write(f"{line}\n")

            # Real + matches
            real_plus_matches_ft = numpy.concatenate(real_data, generated_matches_ft_data)
            with open(FINE_TUNED_DIR + "real_plus_matches.txt", "a") as file:
                for line in real_plus_matches_ft: file.write(f"{line}\n")

            # Real + non-matches
            real_plus_non_matches_ft = numpy.concatenate(real_data, generated_non_matches_ft_data)
            with open(FINE_TUNED_DIR + "real_plus_non_matches.txt", "a") as file:
                for line in real_plus_non_matches_ft: file.write(f"{line}\n")

            # Real + all
            real_plus_all_ft = numpy.concatenate(real_data, generated_matches_ft_data, generated_non_matches_ft_data)
            with open(FINE_TUNED_DIR + "real_pluss_all.txt", "a") as file:
                for line in real_plus_all_ft: file.write(f"{line}\n")

        except:
            no_data.append("ft " + job + "_" + size)

        # Non-fine tuned
        try:
            with open(IDUN_PATH + f"GPT-2/Datasets/wdc/{job}/train.txt.{size}") as real_file:
                real_data = [line for line in real_file.readlines()]

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches_{size}_nft.txt") as generated_matches_nft:
                generated_matches_nft_data = [line for line in generated_matches_nft.readlines()]

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/non_matches{size}_nft.txt") as generated_non_matches_nft:
                generated_non_matches_nft_data = [line for line in generated_non_matches_nft.readlines()]

            # GEN only
            gen_only_nft = numpy.concatenate(generated_matches_nft_data, generated_non_matches_nft_data)
            with open(NON_FINE_TUNED_DIR + "gen_only.txt", "a") as file:
                for line in gen_only_nft: file.write(f"{line}\n")

            # Real + matches
            real_plus_matches_nft = numpy.concatenate(real_data, generated_matches_nft_data)
            with open(NON_FINE_TUNED_DIR + "real_plus_matches.txt", "a") as file:
                for line in real_plus_matches_nft: file.write(f"{line}\n")

            # Real + non_matches
            real_plus_non_matches_nft = numpy.concatenate(real_data, generated_non_matches_nft_data)
            with open(NON_FINE_TUNED_DIR + "real_plus_non_matches.txt", "a") as file:
                for line in real_plus_non_matches_nft: file.write(f"{line}\n")

            # Real + all
            real_plus_all_nft = numpy.concatenate(real_data, generated_matches_nft_data, generated_non_matches_nft_data)
            with open(NON_FINE_TUNED_DIR + "real_plus_all.txt", "a") as file:
                for line in real_plus_all_nft: file.write(f"{line}\n")

        except:
            no_data.append("nft " + job + "_" + size)

        # Fine tuned decimated
        try:
            with open(IDUN_PATH + f"GPT-2/Datasets/wdc/{job}/train.txt.{size}.matches.decimated") as real_file_decimated:
                real_data_decimated = [line for line in real_file_decimated.reallines()]
            
            with open(IDUN_PATH + f"GPT-2/Datasets/wdc/{job}/train.txt.{size}.non_matches.decimated") as real_file_decimated:
                for line in real_file_decimated.readlines(): real_data_decimated.append(line)

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/{size}_matches_decimated.txt") as generated_matches_decimated_ft:
                generated_matches_decimated_ft_data = [line for line in generated_matches_decimated_ft.readlines()]

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/{size}_non_matches_decimated.txt") as generated_non_matches_decimated_ft:
                generated_non_matches_decimated_ft_data = [line for line in generated_non_matches_decimated_ft]

            # GEN only
            gen_only_decimated_ft = numpy.concatenate(generated_matches_decimated_ft_data, generated_non_matches_decimated_ft_data)
            with open(FINE_TUNED_DIR + "gen_only_decimated.txt") as file:
                for line in gen_only_decimated_ft: file.write(f"{line}\n")

            # Real + matches
            real_plus_matches_decimated_ft = numpy.concatenate(real_data_decimated, generated_matches_decimated_ft_data)
            with open(FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "a") as file:
                for line in real_plus_matches_decimated_ft: file.write(f"{line}\n")

            # Real + non_matches
            real_plus_non_matches_decimated_ft = numpy.concatenate(real_data_decimated, generated_non_matches_decimated_ft_data)
            with open(FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "a") as file:
                for line in real_plus_non_matches_decimated_ft: file.write(f"{line}\n")

            # Real + all
            real_plus_all_decimated_ft = numpy.concatenate(real_data_decimated, generated_matches_decimated_ft_data, generated_non_matches_decimated_ft_data)
            with open(FINE_TUNED_DIR + "real_plus_all_decimated.txt", "a") as file:
                for line in real_plus_all_decimated_ft: file.write(f"{line}\n")

        except:
            no_data.append("ft " + job + "_" + size + " decimated")

        # Non-fine tuned decimated
        try:
            with open(IDUN_PATH + f"GPT-2/Datasets/wdc/{job}/train.txt.{size}.matches.decimated") as real_file_decimated:
                real_data_decimated = [line for line in real_file_decimated.reallines()]
            
            with open(IDUN_PATH + f"GPT-2/Datasets/wdc/{job}/train.txt.{size}.non_matches.decimated") as real_file_decimated:
                for line in real_file_decimated.readlines(): real_data_decimated.append(line)

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/matches_{size}_decimated_nft.txt") as generated_matches_decimated_nft:
                generated_matches_decimated_nft_data = [line for line in generated_matches_decimated_nft]

            with open(IDUN_PATH + f"GPT-2/Generated/{job}/{size}_non_matches_decimated_nft.txt") as generated_non_matches_decimated_nft:
                generated_non_matches_decimated_nft_data = [line for line in generated_non_matches_decimated_nft.readlines()]

            # GEN only
            gen_only_decimated_nft = numpy.concatenate(generated_matches_decimated_nft_data, generated_non_matches_decimated_nft_data)
            with open(NON_FINE_TUNED_DIR + "gen_only_decimated.txt") as file:
                for line in gen_only_decimated_nft: file.write(f"{line}\n")

            # Real + matches
            real_plus_matches_decimated_nft = numpy.concatenate(real_data_decimated, generated_matches_decimated_nft_data)
            with open(NON_FINE_TUNED_DIR + "real_plus_matches_decimated.txt", "a") as file:
                for line in real_plus_matches_decimated_nft: file.write(f"{line}\n")

            # Real + non_matches
            real_plus_non_matches_decimated_nft = numpy.concatenate(real_data_decimated, generated_non_matches_decimated_nft_data)
            with open(NON_FINE_TUNED_DIR + "real_plus_non_matches_decimated.txt", "a") as file:
                for line in real_plus_non_matches_decimated_nft: file.write(f"{line}\n")

            # Real + all
            real_plus_all_decimated_nft = numpy.concatenate(real_data_decimated, generated_matches_decimated_nft_data, generated_non_matches_decimated_nft_data)
            with open(NON_FINE_TUNED_DIR + "real_plus_all_decimated.txt", "a") as file:
                for line in real_plus_all_decimated_nft: file.write(f"{line}\n")
                
        except:
            no_data.append("nft " + job + "_" + size + " decimated")

print(no_data)
    
