import os, argparse, random
from transformers import pipeline, GPT2Tokenizer
from ditto_parser import ditto_parser

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--size", type=str, default=None)
parser.add_argument("--type", type=str, default="matches")
parser.add_argument("--amount", type=str, default="double")
hp = parser.parse_args()

er_magellan = [
    "Dirty/DBLP-ACM",
    "Dirty/DBLP-GoogleScholar",
    "Dirty/iTunes-Amazon",
    "Dirty/Walmart-Amazon",
    "Structured/Amazon-Google/",
    "Structured/Beer/", 
    "Structured/DBLP-ACM/",
    "Structured/DBLP-GoogleScholar/",
    "Structured/Fodors-Zagats/",
    "Structured/iTunes-Amazon/",
    "Structured/Walmart-Amazon/",
    "Textual/Abt-Buy"
    ]

wdc = [
    "all",
    "cameras",
    "computers",
    "shoes",
    "watches"
]

TYPE = 0 if hp.type == "non_matches" else 1

if hp.dataset in er_magellan: DATASET = "./Datasets/er_magellan/" + hp.dataset
else: DATASET = "./Datasets/wdc/" + hp.dataset

SAVE_LOCATION = "./Generated/" + hp.dataset if hp.size == None else "./Generated" + hp.dataset + "/" + hp.size
if not os.path.isdir(SAVE_LOCATION): os.makedirs(SAVE_LOCATION)

DATASET_NAME = DATASET + "/train.txt" + hp.type 
if hp.amount == "decimated": DATASET_NAME  + ".decimated"
train = []
with open(DATASET_NAME) as file:
    lines = file.readLines()
    for line in lines: train.append(line.strip())

# Getting validation set
valid = []
with open(DATASET + "/valid.txt") as file:
  lines = file.readlines()
  for line in lines: valid.append(line.strip())

# Cutting the right half off from the validation set to make prompts
cut_valid = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid]


tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
generator = pipeline('text-generation', model='gpt2')

count = 0
while count < len(train):
    valid = False
    while not valid:
        text = ""
        for i in range(5): text += train[random.randint(0, len(train)-1)] + "\n"
        rand = cut_valid[random.randint(0, len(cut_valid)-1)]

        prompt = text + rand + "\tCOL"

        generated = generator(prompt, max_length=round(len(tokenizer(prompt))*2.5), num_return_sequences=1)
        generated_text = generated[0]["generated_text"]
        match = ditto_parser(generated_text)
        valid = match.isValid()
    
    file.write(f"{match.generate_string(TYPE)}\n")
    count += 1
    
file.close()