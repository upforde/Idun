import os, random, argparse
from transformers import pipeline, GPT2Tokenizer
from ditto_parser import ditto_parser

IDUN_PATH ="/cluster/home/danilasm/masters/Idun/GPT-2/"

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--type", type=str, default="matches")
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

generated_data = open(SAVE_NAME + ".txt", "a")

count = 0
while count < amount:
    valid = False
    text = ""

    rand = cut_valid[random.randint(0, len(cut_valid)-1)]
    while len(tokenizer(text)['input_ids']) + len(tokenizer(rand)['input_ids'])*2 < 512:
        text += train[random.randint(0, len(train)-1)] + "\n"
    prompt = text + rand

    print(prompt)
    print()
    print(round(len(tokenizer(rand)['input_ids'])))

    # while not valid:
    #     generated = generator(prompt)
    #     generated_text = generated[0]["generated_text"].replace(text, "")
    #     print(generated_text)
    #     match = ditto_parser(generated_text)
    #     valid = match.isValid()
    
    # generated_data.write(f"{match.generate_string(ENTITY_TYPE)}\n")
    count += 1
    break

generated_data.close()