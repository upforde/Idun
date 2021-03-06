import os, random, argparse
import time
from transformers import pipeline, GPT2Tokenizer
from ditto_parser import ditto_parser

IDUN_PATH ="/cluster/home/danilasm/masters/Idun/GPT-2/"

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--type", type=str, default="non_matches")
parser.add_argument("--decimate", type=str, default="False")
hp = parser.parse_args()

# Parsing arguments and creating variable names
ENTITY_TYPE = 1 if hp.type == "matches" else 0

SAVE_LOCATION = f"{IDUN_PATH}Generated/{hp.dataset}/non_fine_tuned/"
if not os.path.exists(SAVE_LOCATION): os.makedirs(SAVE_LOCATION)
                                
train_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/train.txt"        # Train and valid datasets
valid_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/valid.txt"

SAVE_NAME = SAVE_LOCATION + f"{hp.type}"
train_data += f".{hp.type}"
valid_data += f".{hp.type}"

if hp.decimate == "True":
    SAVE_NAME += "_decimated"
    train_data += ".decimated"
    valid_data += ".decimated"

valid, train = [], []
with open(train_data) as file:
    lines = file.readlines()
    for line in lines: train.append(line)
with open(valid_data) as file:
    lines = file.readlines()
    for line in lines: valid.append(line)

cut_valid = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid]

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
generator = pipeline('text-generation', model='gpt2', tokenizer='gpt2')

if hp.decimate == "True": amount = len(train) * 9
else: amount = len(train)

count = 0
if os.path.exists(SAVE_NAME + ".txt"):
    for line in open(SAVE_NAME + ".txt").readlines():
        if line[:3] == "COL": count += 1

generating_start = time.time()

while count < amount:
    valid = False
    text = ""
    rand = cut_valid[random.randint(0, len(cut_valid)-1)]

    while len(tokenizer(text)['input_ids']) + round(len(tokenizer(rand)['input_ids'])*2.5) < 512:
        add = train[random.randint(0, len(train)-1)] + "\n"
        if len(tokenizer(text)['input_ids']) + (len(tokenizer(rand)['input_ids'])*2) + len(tokenizer(add)['input_ids']) <= 512:
            text += add
        else: break

    prompt = text + rand

    while not valid:
        generated = generator(prompt, max_length=512)
        generated_text = generated[0]["generated_text"].replace(text, "")
        match = ditto_parser(generated_text)
        valid = match.isValid()

    with open(SAVE_NAME + ".txt", "a") as generated_data:
        generated_data.write(f"{match.generate_string(ENTITY_TYPE)}\n")

    count += 1

generating_end = time.time()

open(SAVE_NAME + "_elapsed_time.txt", "w").close()
with open(SAVE_NAME + "_elapsed_time.txt", "a") as time:
    time.write(f"Generating time: {generating_end - generating_start}\n")