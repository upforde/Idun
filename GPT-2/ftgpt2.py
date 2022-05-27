import os, random, argparse
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from transformers import pipeline
from ditto_parser import ditto_parser

print("parsing")
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

MODEL_NAME = hp.dataset
INSTANCE_TYPE = 0 if hp.type == "non_matches" else 1

if hp.dataset in er_magellan: DATASET = "./Datasets/er_magellan/" + hp.dataset
else: DATASET = "./Datasets/wdc/" + hp.dataset

SAVE_LOCATION = "./Generated/" + hp.dataset if hp.size == None else "./Generated" + hp.dataset + "/" + hp.size
if not os.path.isdir(SAVE_LOCATION): os.makedirs(SAVE_LOCATION)

print("getting validation data")
# Getting validation set
valid = []
with open(DATASET + "/valid.txt") as file:
  lines = file.readlines()
  for line in lines: valid.append(line.strip())

# Cutting the right half off from the validation set to make prompts
cut_valid = [item.split("\t")[0] + "\t" + item.split("\t")[1].split(" ")[0] for item in valid]

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

if os.path.exists("./Models/" + MODEL_NAME):
    print("Using model")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    generator = pipeline('text-generation', model="./Models/" + MODEL_NAME, tokenizer='gpt2')
else:
    print("Training model")
    train_data = DATASET + "/train.txt." + hp.type if hp.amount == "double" else DATASET + "/train.txt." + hp.type + ".decimated"
    test_data = DATASET + "/test.txt." + hp.type

    # Setting up the training datasets, tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    train_dataset,test_dataset,data_collator = load_dataset(train_data,test_data,tokenizer)
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    training_args = TrainingArguments(
        output_dir="./Models/" + MODEL_NAME,                                        #The output directory
        overwrite_output_dir=True,                                                  # overwrite the content of the output directory
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

    generator = pipeline('text-generation', model="./Models/" + MODEL_NAME, tokenizer='gpt2')

print("checking amount")

if hp.amount == "double":
    with open(DATASET + "/train.txt." + hp.type) as file:
        amount = len(file.readlines())
if hp.amount == "decimate":
    with open(DATASET + "/train.txt." + hp.type) as file:
        amount = round(len(file.readlines())*0.9)

print("opening file")
file = open(SAVE_LOCATION + "/fine_tuned.txt." + hp.type, "a")

print("what the fuck")
count = 0
while count < amount:
    valid = False
    prompt = cut_valid[random.randint(0, len(cut_valid)-1)]
    print("n")
    while not valid:
        print("nani")
        generated = generator(prompt, max_length=round(len(tokenizer(prompt)['input_ids'])*2.5), num_return_sequences=1)
        generated_text = generated[0]["generated_text"]
        print(generated_text)
        match = ditto_parser(generated_text)
        valid = match.isValid()

    file.write(f"{match.generate_string(INSTANCE_TYPE)}\n")
    count += 1
    print(f"Created {count} out of {amount}")

print("done")
file.close()