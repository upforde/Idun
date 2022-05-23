from transformers import AutoModelWithLMHead, AutoTokenizer
from transformers import TextDataset,DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from transformers import pipeline

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

class ftGPT2:
    def __init__(self, train_data, test_data):
        # Setting up the training datasets, tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        train_dataset,test_dataset,data_collator = load_dataset(train_data,test_data,tokenizer)
        self.model = AutoModelWithLMHead.from_pretrained("gpt2")

        training_args = TrainingArguments(
            output_dir="./EMmodel",                                                     #The output directory
            overwrite_output_dir=True,                                                  #overwrite the content of the output directory
            num_train_epochs=3,                                                         # number of training epochs
            per_device_train_batch_size=32,                                             # batch size for training
            per_device_eval_batch_size=32,                                              # batch size for evaluation
            eval_steps = 400,                                                             # Number of update steps between two evaluations.
            save_steps=800,                                                              # after # steps model is saved 
            warmup_steps=500,                                                           # number of warmup steps for learning rate scheduler
            prediction_loss_only=True,
            )


        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            data_collator=data_collator,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
        )

    def train(self):
        self.trainer.train()
        return pipeline('text-generation', model=self.model, tokenizer='gpt2')
    
    def save(self):
        self.model.save_model()



