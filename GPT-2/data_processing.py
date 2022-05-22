import sys
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

file_paths = []
for path in PATH:
    files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    for f in files: file_paths.append(f)

for path in file_paths:
    print(path)
    matches, non_matches = [], []
    
    with open(path) as file:
        lines = file.readlines()
        for line in lines:
            arr = line.split("\t")
            if "1" in arr[-1]: matches.append(line.strip())
            else: non_matches.append(line.strip())

    file = open(path+".matches", "a")
    for match in matches:
        file.write(match)
        file.write("\n")
    file.close()

    file = open(path+".non_matches", "a")
    for non_match in non_matches:
        file.write(non_match)
        file.write("\n")
    file.close()
