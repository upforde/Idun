# Utilising GPT-2 to generate tabular textual data for use in Entity Matching

#### Preface
Before running anything, manke sure that the datasets have been pre-processed. This is done by running [data_processing.py](./data_processing.py).

Since this is meant to be ran on the Idun GPU cluster, slurm jobs are created with [cnft_jobs](./cnft_jobs.py) and [cg_jobs](./cg_jobs.py) files. If you have good enough hardware, you can run the code directly without creating and running slurm jobs.

## Non-fine-tuned GPT-2
The file [cnft.py](./cnft.py) is used to generate data using the non-fine-tuned GPT-2 model. 

By selecting several examples of an entry (matching or non-matching) and feeding them together with a prompt. The model gets the needed context and generates a new entry based on it.

## Fine-tuned GPT-2
The file [cg.py](./cg.py) is used to fine-tune GPT-2 and generate data using that fine-tuned model.

By fine-tuning the model on the training data, the model learns to mimic the entry structure. When supplied with a new entity prompt, it uses what it learned from the fine-tuning to create a new entry.

<details><summary>Helper files</summary>
<p>

### [check_progress.py](./check_progress.py)
This file is used to check which data has yet to be generated, and the progress of the generation.

### [create_datasets.py](./create_datasets.py)
This file is used to combine the real data with the generated data, creating the datasets that are used in experiments in the process.

### [ditto_parser.py](./ditto_parser.py)
The ditto parser is used to parse and validate the output of the GPT-2 model. Since GPT-2 is a language model, somethimes the data it outputs is not in the format that we need, meaning it needs to be parsed and validated.

</p>
</details>
