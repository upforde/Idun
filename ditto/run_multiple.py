from subprocess import call
from random import random

times = 3

print("Running baseline")
for i in range(times):
    print("Times ran:", i+1)
    name = "Writer_output/Ditto_baseline/run_" +str(i+1) + ".txt"
    seed = str(round(random()*2147483647))
    print(seed)
    call(["python", "train_ditto.py",  "--task=Structured/Beer", "--batch_size=12", "--output_name=" + name, "--run_id=" + seed])


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
