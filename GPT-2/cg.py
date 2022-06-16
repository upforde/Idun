import argparse, os, random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from transformers import pipeline
from ditto_parser import ditto_parser

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--type", type=str, default="matches")
parser.add_argument("--decimate", type=str, default="False")
hp = parser.parse_args()

# Parsing arguments and creating variable names
IDUN_PATH ="/cluster/home/danilasm/masters/Idun/GPT-2/"
IDUN_PATH = "./"
MODEL_NAME = IDUN_PATH + "Models/" + hp.dataset + "_" + hp.type
SAVE_LOCATION = f"{IDUN_PATH}Generated/{hp.dataset}/fine_tuned/"
if not os.path.exists(SAVE_LOCATION): os.makedirs(SAVE_LOCATION)

train_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/train.txt"        # Train test valid datasets 
test_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/test.txt"          # from the er_magellan datasets
valid_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/valid.txt"

train_data += f".{hp.type}"
test_data += f".{hp.type}"
valid_data += f".{hp.type}"
FILE_NAME = SAVE_LOCATION + f"{hp.type}"

if hp.decimate == "True":                                                       # Adding suffix for if to use the decimated
    train_data += ".decimated"                                                  # datasets or not
    test_data += ".decimated"
    valid_data += ".decimated"
    MODEL_NAME += "_decimated"
    FILE_NAME += "_decimated"

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

# Setting up the training datasets, tokenizer, model and trainer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
train_dataset,test_dataset,data_collator = load_dataset(train_data,test_data,tokenizer)
model = GPT2LMHeadModel.from_pretrained("gpt2")

training_args = TrainingArguments(
    output_dir=MODEL_NAME,                                                      # The output directory
    overwrite_output_dir=True,                                                  # overwrite the content of the output directory
    num_train_epochs=3,                                                         # number of training epochs
    per_device_train_batch_size=64,                                             # batch size for training
    per_device_eval_batch_size=64,                                              # batch size for evaluation
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

# Training and saving the model
trainer.train()
trainer.save_model()

ENTITY_TYPE = 1 if hp.type == "matches" else 0

valid = []
with open(valid_data) as valid_file:
    for line in valid_file.readlines():
        valid.append(line)

cut_valid = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid]

generator = pipeline('text-generation', model=MODEL_NAME, tokenizer='gpt2')

if hp.decimate == "True": amount = len(open(train_data).readlines()) * 9
else: amount = len(open(train_data).readlines())

count = 0
for line in open(FILE_NAME + ".txt").readlines():
    if "COL" in line: count += 1

while count < amount:
    with open(FILE_NAME + ".txt", "a") as generated_data:
        valid = False
        prompt = cut_valid[random.randint(0, len(cut_valid)-1)]

        if round(len(tokenizer(prompt)['input_ids'])*2.5) <= 512: 
            max_length = round(len(tokenizer(prompt)['input_ids'])*2.5)
        else: max_length = 512

        while not valid:
            generated = generator(prompt, max_length=max_length)
            generated_text = generated[0]["generated_text"]
            match = ditto_parser(generated_text)
            valid = match.isValid()
        
        generated_data.write(f"{match.generate_string(ENTITY_TYPE)}\n")

    count += 1