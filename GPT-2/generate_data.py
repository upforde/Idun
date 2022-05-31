import os, random, argparse
from transformers import pipeline, GPT2Tokenizer
from ditto_parser import ditto_parser

IDUN_PATH ="/cluster/home/danilasm/masters/Idun/GPT-2/"

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--size", type=str, default=None)
parser.add_argument("--type", type=str, default="matches")
parser.add_argument("--decimate", type=str, default="False")
parser.add_argument("--ft", type=str, default="True")
hp = parser.parse_args()

# Parsing arguments and creating variable names
ENTITY_TYPE = 1 if hp.type == "matches" else 0

SAVE_LOCATION = IDUN_PATH + "Generated/" + hp.dataset
MODEL_NAME = IDUN_PATH + "Models/" + hp.dataset                                         # The name of the model, it's called this
                                                                                        # when saved
if "/" in hp.dataset: 
    train_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/train.txt"        # Train test datasets, depending on if they're 
    valid_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/valid.txt"        # from the er_magellan datasets or the wdc
else:                                                                                   # datasets
    train_data = IDUN_PATH + "Datasets/wdc/" + hp.dataset + "/train.txt." + hp.size
    valid_data = IDUN_PATH + "Datasets/wdc/" + hp.dataset + "/valid.txt." + hp.size

SAVE_NAME = SAVE_LOCATION + f"/{hp.type}"
MODEL_NAME += f"_{hp.type}" 
train_data += f".{hp.type}"
valid_data += f".{hp.type}"

if "/" not in hp.dataset: 
    SAVE_NAME += f"_{hp.size}"
    MODEL_NAME += f"/{hp.size}"

if hp.decimate == "True":               
    SAVE_NAME += "_decimated"                                                   # Adding postfix for if to use the decimated
    MODEL_NAME += "_decimated"                                                          # datasets or not
    train_data += ".decimated"
    valid_data += ".decimated"

if hp.ft == "False":
    MODEL_NAME = "gpt2"
    SAVE_NAME = IDUN_PATH + f"Generated/{hp.dataset}/{hp.size}_{hp.type}"
    if hp.decimate: SAVE_NAME += "_decimated"
    SAVE_NAME += "_nft"

if not os.path.isdir(SAVE_LOCATION): os.makedirs(SAVE_LOCATION)

valid, train = [], []
with open(train_data) as file:
    lines = file.readlines()
    for line in lines: train.append(line)
with open(valid_data) as file:
    lines = file.readlines()
    for line in lines: valid.append(line)

# cut_valid = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid]

# file = open(SAVE_NAME + ".txt", "a")

# tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
# generator = pipeline('text-generation', model=MODEL_NAME, tokenizer='gpt2')

if hp.decimate == "True": amount = len(train) * 9
else: amount = len(train)

for line in train: print(f"{line}\n")
print(amount)

# count = 0
# while count < amount:
#     valid = False
#     text = ""
#     if not hp.ft: 
#         for i in range(5):
#             text += train[random.randint(0, len(train)-1)] + "\n"
#     rand = cut_valid[random.randint(0, len(cut_valid)-1)]
#     prompt = text + rand + "\tCOL"

#     while not valid:
#         generated = generator(prompt, max_length=round(len(tokenizer(prompt)['input_ids'])*3), num_return_sequences=1)
#         generated_text = generated[0]["generated_text"]
#         match = ditto_parser(generated_text)
#         valid = match.isValid()
    
#     print(match.generate_string(ENTITY_TYPE))
#     file.write(f"{match.generate_string(ENTITY_TYPE)}\n")
#     count += 1

# file.close()