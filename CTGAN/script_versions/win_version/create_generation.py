import os

def make_text(output, dataset, matches, decimate, size=None, threshold=0.7, drop_dupes=False):
    script_path = r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\CTGAN_generation.py"
    python_line = f"py \"{script_path}\" --dataset=\"{dataset}\" --matches={matches} --decimate={decimate} --threshold={threshold} --drop_dupes={drop_dupes}"
    if size != None: python_line += " --size=" + size
    decimate_text = "decimate" if decimate else ""
    size_text = size if size != None else ""
    matched_text = "matched" if matches else "non_matched"
    drop_text = "drop dupes" if drop_dupes else ""
    text = [
        "#!/bin/sh",
        python_line
    ]
    return text


er_magellan = [
    r"Dirty\DBLP-ACM",
    r"Dirty\DBLP-GoogleScholar",
    r"Dirty\iTunes-Amazon",
    r"Dirty\Walmart-Amazon",
    r"Structured\Amazon-Google",
    r"Structured\Beer",
    r"Structured\DBLP-ACM",
    r"Structured\DBLP-GoogleScholar",
    r"Structured\Fodors-Zagats",
    r"Structured\iTunes-Amazon",
    r"Structured\Walmart-Amazon",
    r"Textual\Abt-Buy"
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

names = []

jobs_dir = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\gen_jobs' + os.sep

for job in er_magellan:
    name = jobs_dir + job.replace(os.sep, "_") + "_matches"
    names.append(name)
    text = make_text(name + ".out", job, True, False)
    with open(name + ".sh", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = jobs_dir + job.replace(os.sep, "_") + "_non_matches"
    names.append(name)
    text = make_text(name + ".out", job, False, False)
    with open(name + ".sh", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = jobs_dir + job.replace(os.sep, "_") + "_matches_decimated"
    names.append(name)
    text = make_text(name + ".out", job, True, True)
    with open(name + ".sh", "a") as file:
        for line in text:
            file.write(f"{line}\n")

    name = jobs_dir + job.replace(os.sep, "_") + "_non_matches_decimated"
    names.append(name)
    text = make_text(name + ".out", job, False, True)
    with open(name + ".sh", "a") as file:
        for line in text:
            file.write(f"{line}\n")

for job in wdc:
    for size in sizes:
        name = jobs_dir + job.replace(os.sep, "") + "_matches_" + size
        names.append(name)
        text = make_text(name + ".out", job, True, False, size)
        with open(name + ".sh", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = jobs_dir + job.replace(os.sep, "") + "_non_matches_" + size
        names.append(name)
        text = make_text(name + ".out", job, False, False, size)
        with open(name + ".sh", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = jobs_dir + job.replace(os.sep, "") + "_matches_decimated_" + size
        names.append(name)
        text = make_text(name + ".out", job, True, True, size)
        with open(name + ".sh", "a") as file:
            for line in text:
                file.write(f"{line}\n")

        name = jobs_dir + job.replace(os.sep, "") + "_non_matches_decimated_" + size
        names.append(name)
        text = make_text(name + ".out", job, False, True, size)
        with open(name + ".sh", "a") as file:
            for line in text:
                file.write(f"{line}\n")

with open("run_gen_jobs.sh", "a") as file:
    file.write("#!/bin/sh\n")
    for name in names:
        file.write(f"sh \"{name}.sh\" \n")