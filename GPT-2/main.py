import os, random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from transformers import pipeline
from ditto_parser import ditto_data_maker

# Function for creating the train-test datasets for the model
def load_dataset(train_path,test_path,tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=train_path,
        block_size=32)
    
    test_dataset = TextDataset(
        tokenizer=tokenizer,
        file_path=test_path,
        block_size=32)   
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False,
    )
    return train_dataset,test_dataset,data_collator

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

# Setting up the training datasets, tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
train_dataset,test_dataset,data_collator = load_dataset(train_data,test_data,tokenizer)
model = GPT2LMHeadModel.from_pretrained("gpt2")

training_args = TrainingArguments(
    output_dir="./EMmodel",                                                     #The output directory
    overwrite_output_dir=True,                                                  #overwrite the content of the output directory
    num_train_epochs=5,                                                         # number of training epochs
    per_device_train_batch_size=32,                                             # batch size for training
    per_device_eval_batch_size=32,                                              # batch size for evaluation
    eval_steps = 400,                                                           # Number of update steps between two evaluations.
    save_steps=800,                                                             # after # steps model is saved 
    warmup_steps=500,                                                           # number of warmup steps for learning rate scheduler
    prediction_loss_only=True,
    )


trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()
trainer.save_model()

generator = pipeline('text-generation', model="./EMmodel", tokenizer='gpt2')

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
