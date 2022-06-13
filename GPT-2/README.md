# Utilising GPT-2 to generate tabular textual data for use in Entity Matching

#### Preface
Before running anything, manke sure that the datasets have been pre-processed. This is done by running [data_processing.py](./data_processing.py).

Since this is meant to be ran on the Idun GPU cluster, slurm jobs are created. If you have good enough hardware, you can run the code directly without creating and running slurm jobs.

## Non-fine-tuned GPT-2
The file [cnft.py](./cnft.py) is used to generate data using the non-fine-tuned GPT-2 model. 

By selecting several examples of an entry (matching or non-matching) and feeding them together with a prompt. The model gets the needed context and generates a new entry based on it.

## Fine-tuned GPT-2
The file [cg.py](./cg.py) is used to fine-tune GPT-2 and generate data using that fine-tuned model.

By fine-tuning the model on the training data, the model learns to mimic the entry structure. When supplied with a new entity prompt, it uses what it learned from the fine-tuning to create a new entry.