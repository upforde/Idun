import argparse
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

IDUN_PATH ="/cluster/home/danilasm/masters/Idun/GPT-2/"

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--size", type=str, default=None)
parser.add_argument("--type", type=str, default="matches")
parser.add_argument("--decimate", type=str, default="False")
hp = parser.parse_args()

# Parsing arguments and creating variable names
MODEL_NAME = IDUN_PATH + "Models/" + hp.dataset + "_" + hp.type                         # The name of the model, it's called this
                                                                                        # when saved
if "/" in hp.dataset: 
    train_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/train.txt"          # Train test datasets, depending on if they're 
    test_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/test.txt"            # from the er_magellan datasets or the wdc
else:                                                                                     # datasets
    MODEL_NAME += f"/{hp.size}"
    train_data = IDUN_PATH + "Datasets/wdc/" + hp.dataset + "/train.txt." + hp.size
    test_data = IDUN_PATH + "Datasets/wdc/" + hp.dataset + "/test.txt"

train_data += f".{hp.type}"
test_data += f".{hp.type}"

if hp.decimate == "True":                                                       # Adding postfix for if to use the decimated
    train_data += ".decimated"                                                  # datasets or not
    test_data += ".decimated"
    MODEL_NAME += "_decimated"

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

# Training and saving the model
trainer.train()
trainer.save_model()