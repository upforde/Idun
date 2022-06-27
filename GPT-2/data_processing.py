import random, os
from os import listdir
from os.path import isfile, join

PATH = ["Datasets/er_magellan/Dirty/DBLP-ACM",
        "Datasets/er_magellan/Dirty/DBLP-GoogleScholar",
        "Datasets/er_magellan/Dirty/iTunes-Amazon",
        "Datasets/er_magellan/Dirty/Walmart-Amazon",
        "Datasets/er_magellan/Structured/Amazon-Google/",
        "Datasets/er_magellan/Structured/Beer/", 
        "Datasets/er_magellan/Structured/DBLP-ACM/",
        "Datasets/er_magellan/Structured/DBLP-GoogleScholar/",
        "Datasets/er_magellan/Structured/Fodors-Zagats/",
        "Datasets/er_magellan/Structured/iTunes-Amazon/",
        "Datasets/er_magellan/Structured/Walmart-Amazon/",
        "Datasets/er_magellan/Textual/Abt-Buy",
        "Datasets/wdc/all",
        "Datasets/wdc/cameras",
        "Datasets/wdc/computers",
        "Datasets/wdc/shoes",
        "Datasets/wdc/watches"]

endings = ["txt", "small", "medium", "large", "xlarge"]

file_paths = []
for path in PATH:
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    for f in files: 
        if f.split(".")[-1] in endings: file_paths.append(f)
        else: os.remove(f)

for path in file_paths:
    print(path)
    matches, non_matches = [], []
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            arr = line.split("\t")
            if "1" in arr[-1]: matches.append(line.strip())
            else: non_matches.append(line.strip())

    decimated_matches, decimated_non_matches = [], []

    while len(decimated_matches) < round(len(matches)*.1):
        temp = matches[random.randint(0, len(matches)-1)]
        if temp in decimated_matches: continue
        decimated_matches.append(temp)

    while len(decimated_non_matches) < round(len(non_matches)*.1):
        temp = non_matches[random.randint(0, len(non_matches)-1)]
        if temp in decimated_non_matches: continue
        decimated_non_matches.append(temp)

    open(path+".matches", "w").close()
    with open(path+".matches", "a") as file:
        for match in matches:
            file.write(match)
            file.write("\n")

    open(path+".non_matches", "w").close()
    with open(path+".non_matches", "a") as file:
        for non_match in non_matches:
            file.write(non_match)
            file.write("\n")

    open(path+".matches.decimated", "w").close()
    with open(path+".matches.decimated", "a") as file:
        for match in decimated_matches:
            file.write(match)
            file.write("\n")

    open(path+".non_matches.decimated", "w").close()
    with open(path+".non_matches.decimated", "a") as file:
        for non_match in decimated_non_matches:
            file.write(non_match)
            file.write("\n")
