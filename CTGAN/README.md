# Utilising CTGAN to generate tabular data for use in Entity Matching

#### Preface

Since this is meant to be ran on NTNU's IDUN GPU cluster, slurm jobs are created with helper Python files. However, if consider your own setup to be good enough, you can run the code directly without creating and running slurm jobs. (However, it is highly advised to use IDUN). 

The files for reference are:
[create_jobs.py](./create_jobs.py)
Python script to create .slurm files for training of CTGAN models. Uses CTGAN_training.py
<br>
[create_generation.py](./create_generation.py)
Python script to create .slurm files for the generation of data from CTGAN models. Uses CTGAN_generation.py
<br>
[create_tests.py](./create_tests.py)
Python script to create .slurm files for testing data through the Magellan framework. Uses Magellan_testing.py

For more on running these examples, see the section further below.

### CTGAN: Modeling Tabular data using Conditional GAN

The Conditional Tabular Generative Adversarial Network (CTGAN), sees further development on the Tabular Generative Adversarial Network (tableGAN) where a conditional generator is introduced to better model continuous columns of data. 

The original paper on CTGAN can be found [here](https://arxiv.org/abs/1907.00503).

While the paper outlines its architecture, we utilize the Synthetic Data Vault (SDV)'s implementation of [CTGAN](https://sdv.dev/SDV/user_guides/single_table/ctgan.html). The SDV Project was first created at MIT’s Data to AI Lab in 2016, however today SDV is maintained by DataCebo. 

The files [CTGAN_training.py](./CTGAN_training.py) and [CTGAN_generation.py](./CTGAN_generation.py) are used to train and generate data from the resulting CTGAN models.

### Magellan: Toward Building Entity Matching Management Systems

The Magellan EM system aims to provide a development framework for customized EM systems through its pipeline. With the implementation in Python, it aims to utilize the public ecosystem of python libraries to further its capabilities. It's original approach uses traditional classification methods and similiarity metrics, however has later seen further development with Deep Learning as its matcher. 

The original paper on Magellan can be found [here.](https://pages.cs.wisc.edu/~anhai/papers1/magellan-sigmodrec18.pdf)
The paper on Magellan's DL utilization can be found [here.](https://pages.cs.wisc.edu/~anhai/papers1/deepmatcher-sigmod18.pdf)

We utilize the "py_entitymatching" library developed by the anhaidgroup. You can find the code repository with guides, user manuals and more [here.](https://github.com/anhaidgroup/py_entitymatching)

The file [Magellan_testing.py](./Magellan_testing.py) is used to evaluate the different datasets and its synthetic counterparts generated from our generators. We do not use the blocking features from Magellan, as they are redundant in our experiments. 

<details><summary>Helper files</summary>
<p>

#### [create_parser.py](./create_parser.py)
Magellan and Ditto require different formats for their datasets. This file is used to create .slurm jobs for parsing data. It uses the [parse_data.py](./parse_data.py) script to parse data from text based Ditto formats to dataframe based Magellan formats, and vice versa.

#### [create_datasets.py](./create_datasets.py)
This file is used to combine the real data with the generated data, creating the datasets that are used in experiments in the process.

#### [make_graphs.py](./make_graphs.py)
This file loads in the result files from the "Results" directory, and generate plots based on the files values.

#### [rename_files.py](./rename_files.py)
This file simply renames some of the files from the synthetic datasets. A simple naming convention error on the Augmentation and GPT-2 generated datasets caused the need for this.


</p>
</details>

### How to run these files for yourself:

Some of the scripts contain full-length paths inside of them, thus if anyone wanted to run these files, they would have to edit these paths.

We also did not include the fully-trained CTGAN models, as they're size were limited by Github. 

Lastly, there are some hiccups in the Magellan framework which we've had to fix in order to run our experiments more smoothly. As such, a tiny edit is necessary to run these experiments seamlessly. 

<details><summary><b>1. Paths to edit</b></summary>

#### 1. create_datasets.py
On line 20: 
```IDUN_PATH = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/'```
Change to:
```IDUN_PATH = r'<your_directory>/Idun/CTGAN/'```

#### 2. create_generation.py
On line 4: 
```script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/CTGAN_generation.py"```
Change to:
```script_path = r"<your_directory>/Idun/CTGAN/CTGAN_generation.py"```

On line 54: 
```jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/gen_jobs/'```
Change to:
```jobs_dir = r'<your_directory>/Idun/CTGAN/gen_jobs/'```

On line 88: 
```file.write(f"sbatch {name}.slurm alekssim\n")```
Change to:
```file.write(f"sbatch {name}.slurm <your_IDUN_user>\n")```

#### 3. create_jobs.py
On line 4: 
```script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/CTGAN_training.py"```
Change to:
```script_path = r"<your_directory>/Idun/CTGAN/CTGAN_training.py"```

On line 52: 
```jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/jobs/'```
Change to:
```jobs_dir = r'<your_directory>/Idun/CTGAN/jobs/'```

On line 86: 
```file.write(f"sbatch {name}.slurm alekssim\n")```
Change to:
```file.write(f"sbatch {name}.slurm <your_IDUN_user>\n")```

#### 4. create_parser.py
On line 11: 
```script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/parse_data.py"```
Change to:
```script_path = r"<your_directory>/Idun/CTGAN/parse_data.py"```

On line 62: 
```jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/parse_jobs/'```
Change to:
```jobs_dir = r'<your_directory>/Idun/CTGAN/parse_jobs/'```

On line 99: 
```file.write(f"sbatch {name}.slurm alekssim\n")```
Change to:
```file.write(f"sbatch {name}.slurm <your_IDUN_user>\n")```

#### 5. create_tests.py
On line 24: 
```script_path = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Magellan_testing.py"```
Change to:
```script_path = r"<your_directory>/Idun/CTGAN/Magellan_testing.py"```

On line 90: 
```jobs_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/match_jobs/'```
Change to:
```jobs_dir = r'<your_directory>/Idun/CTGAN/match_jobs/'```

On line 102: 
```file.write(f"sbatch {name}.slurm alekssim\n")```
Change to:
```file.write(f"sbatch {name}.slurm <your_IDUN_user>\n")```

#### 6. CTGAN_generation.py
On line 25: 
```model_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models/'```
Change to:
```model_dir = r'<your_directory>/Idun/CTGAN/Models/'```

On line 28 and 29: 
```datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'```
```synth_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/'```

Change to:
```datasets_dir = r'<your_directory>/Idun/CTGAN/Datasets/'```
```synth_dir = r'<your_directory>/Idun/CTGAN/Datasets_Synth/Magellan/'```

#### 7. CTGAN_training.py
On line 21: 
```model_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models'```
Change to:
```model_dir = r'<your_directory>/Idun/CTGAN/Models/'```

On line 24: 
```datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'```
Change to:
```datasets_dir = r'<your_directory>/Idun/CTGAN/Datasets/'```

#### 8. Magellan_testing.py
On line 44: 
```datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'```
Change to:
```datasets_dir = r'<your_directory>/Idun/CTGAN/Datasets/'```

On line 49-58: 
```synth_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/<generator>/'```
Change to:
```synth_dir = r'<your_directory>/Idun/CTGAN/Datasets_Synth/Magellan/<generator>/'```

On line 384:
```temp_C_dir = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/Temp_Tables"```
Change to:
```temp_C_dir = r"<your_directory>/Idun/CTGAN/Datasets/Temp_Tables"```

On line 572:
```result_dir = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Results/"```
Change to:
```result_dir = r"<your_directory>/Idun/CTGAN/Results/"```

#### 9. make_graphs.py
On line 44: 
```save_score_path = r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Results" + os.sep + plot_type + ".csv"```
Change to:
```save_score_path = r"<your_directory>\Idun\CTGAN\Results" + os.sep + plot_type + ".csv"```

#### 10. make_graphs.py
On line 21: 
```dataset_orig_data = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'```
Change to:
```dataset_orig_data = r'<your_directory>/Idun/CTGAN/Datasets/'```

On line 25-29:
```datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/'```
```datasets_goal_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Ditto/'```

Change to:
```datasets_dir = r'<your_directory>/Idun/CTGAN/Datasets_Synth/Magellan/'```
```datasets_goal_dir = r'<your_directory>/Idun/CTGAN/Datasets_Synth/Ditto/'```

</details>

<details><summary><b>2. Models.</b></summary>

As previously stated, the models trained were too big for GitHub. However, to skip the lengthy procedure of training each model again, the models can be downloaded [here.](https://mega.nz/file/kWFE3RTJ#0RKAPHafFShhNI92084hwpNI4KiRDXUF13hmRUj6JsQ)

Simply un-zip the file, and move the "Models" folder into the "CTGAN" folder.

</details>


<details><summary><b>3. Magellan hiccup.</b></summary>

Magellan needs attribute correspondance for generating feature_tables for its matching procedure. However, this function can sometimes pick up multiple attribute correspondaces and require manual work to be configured correctly. 

We have slightly adjusted a file inside of the py_entitymatching library to combat this. Simply download the file [here.](https://mega.nz/file/lSt2nQrL#zujF_FcPfaoBShViHRse5WvOKXn1ltUdB5hPGMdPbAw), and replace the corresponding file inside of the py_entitymatching library folder. This is usually found in your python directory, in **[../site-packages/py_entitymatching/feature]**.

If this sounds too grevious of a task, simply run Magellan_testing.py until it throws an error pointing to the file in question. It will usually accompany the path to the file required to be replaced. 

</details>