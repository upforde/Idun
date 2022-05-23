import os, random, time
from ftgpt2 import ftGPT2
from ditto_parser import ditto_data_maker

save_location = "Generated/er_magellan/Structured/Beer/"
if not os.path.isdir(save_location): os.makedirs(save_location)

train = "Datasets/er_magellan/Structured/Beer/train.txt.matches"
test = "Datasets/er_magellan/Structured/Beer/test.txt.matches"

# Getting validation set
valid_matches = []
with open("Datasets/er_magellan/Structured/Beer/valid.txt") as file:
  lines = file.readlines()
  for line in lines:
    arr = line.split("\t")
    if "1" in arr[-1]: valid_matches.append(line.strip())

# Cutting the right half off from the validation set to make prompts
cut_valid_matches = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid_matches]

gpt2 = ftGPT2(train, test)
generator = gpt2.train()

generated_matches = []

with open("Datasets/er_magellan/Structured/Beer/train.txt.matches") as file:
  lines = file.readlines()
  train_len = len(lines)

start = time.time()

while len(generated_matches) != train_len:
  print(f"Generating example: {len(generated_matches) + 1} of {train_len}")
  valid = False
  while not valid:
    text = cut_valid_matches[random.randint(0, len(cut_valid_matches)-1)]
    generated = generator(text)[0]['generated_text']
    match = ditto_data_maker(generated)
    valid = match.isValid()
  generated_matches.append(match.generate_string(1))

end = time.time()

print(f"Time elapsed: {end-start}s")

file = open(save_location + "fine_tuned_matches.txt", "a")
for match in generated_matches:
    file.write(match)
    file.write("\n")
file.close()
