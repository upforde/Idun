import os, random
from gpt2 import generator
from ditto_parser import ditto_data_maker
from ftgpt2 import ftGPT2

save_location = "./Generated/er_magellan/Structured/Beer/"
if not os.path.isdir(save_location): os.makedirs(save_location)

# train_matches = []
# with open("./Datasets/er_magellan/Structured/Beer/train.txt.matches") as file:
#   lines = file.readlines()
#   for line in lines:
#     arr = line.split("\t")
#     if "1" in arr[-1]: train_matches.append(line.strip())

# Getting validation set
valid_matches = []
with open("./Datasets/er_magellan/Structured/Beer/valid.txt") as file:
  lines = file.readlines()
  for line in lines:
    arr = line.split("\t")
    if "1" in arr[-1]: valid_matches.append(line.strip())

# Cutting the right half off from the validation set to make prompts
cut_valid_matches = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid_matches]

file = open(save_location + "fine_tuned_matches.txt", "a")

# valid = False
# while not valid:
#   text = ""
#   for i in range(5): 
#     text += valid_matches[random.randint(0, len(valid_matches)-1)] + "\n"
#   rand = cut_valid_matches[random.randint(0, len(cut_valid_matches)-1)]

#   prompt = text + rand + "\tCOL"

#   generated = generator(prompt, max_length=500, num_return_sequences=1)
#   generated_text = generated[0]["generated_text"]
#   print(generated_text)
#   match = ditto_data_maker(generated_text)
#   valid = match.isValid()
  
#   file.write(f"{valid}: {generated_text}")

train_data = "./Datasets/er_magellan/Structured/Beer/train.txt.matches"
test_data = "./Datasets/er_magellan/Structured/Beer/test.txt.matches"

model = ftGPT2(train_data, test_data)
tokenizer = model.getTokenizer()
generator = model.pipeline()

valid = False
prompt = cut_valid_matches[random.randint(0, len(cut_valid_matches)-1)]
print(prompt)
while not valid:
  generated = generator(prompt, max_length=round(len(tokenizer(prompt)['input_ids'])*3), num_return_sequences=1)
  generated_text = generated[0]["generated_text"]
  print(generated_text)
  match = ditto_data_maker(generated_text)
  valid = match.isValid()

file.write(match.generate_string(1))
file.write("\n")

file.close()
