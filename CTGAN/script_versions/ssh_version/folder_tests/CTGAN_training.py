import argparse
import pandas as pd
import os
from distutils import util
from sdv.tabular import CTGAN

pd.options.mode.chained_assignment = None  # default='warn'

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument('--matches', dest='matches', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--decimate", dest='decimate', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--size", type=str, default=None)

hp = parser.parse_args()

# If the data is in DITTO format or not.
ditto_format = True

# Model directory to be saved at.
model_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models/'

# Dataset directory.
datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'

# Model name.
job_name = hp.dataset + os.sep

model_name = hp.dataset
model_name = model_name.replace(os.sep, "_") # Might have to change this later.

if os.sep in hp.dataset :
    datasets_dir += "er_magellan" + os.sep + job_name + "train.txt"
    model_dir += "er_magellan" + os.sep + job_name
else:
    model_name += "_" + hp.size
    datasets_dir += "wdc" + os.sep + job_name + "train.txt." + hp.size
    model_dir += "wdc" + os.sep + job_name + hp.size + os.sep

if hp.matches:
    datasets_dir += ".matches"
    model_name += "_matches"
else:
    datasets_dir += ".non_matches"
    model_name += "_non_matches"

if hp.decimate:
    datasets_dir += ".decimated"
    model_name += "_decimated"

model_name += ".pkl"

# Model training parameters.
epochs = 3000
batch_total = 1000

# If the model should trained on "matched" or "non-matched" examples.
train_on_matched = hp.matches



def ditto_reformater(data):
    columns = []
    values = []
    value_writer = ""
    sentence_order = 0
    table_order = 0
    table1 = pd.DataFrame()
    table2 = pd.DataFrame()
    table3 = pd.DataFrame()
    starting_row = True

    for line in data.splitlines():
        table_order = 0
        for side in line.split("\t"):
            for word in side.split(" "):
                if word == "COL":
                    if value_writer != "" and value_writer != " ":
                        values.append(value_writer)
                    elif not starting_row:
                        values.append(float("NaN"))
                    else:
                        starting_row = False
                    read_column = True
                    read_values = False
                elif word == "VAL":
                    read_column = False
                    read_values = True
                    first_word = True
                    value_writer = ""
                else:
                    if read_column:
                        columns.append(word)
                    elif read_values:
                        if first_word:
                            value_writer = word
                            first_word = False
                        else:
                            value_writer += " " + word
            values.append(value_writer)
            value_writer = ""
            starting_row = True
            res = dict(zip(columns, values))
            if sentence_order == 0:
                if table_order == 0:
                    table1 = pd.DataFrame.from_dict([res])
                    table_order = 1
                elif table_order == 1:
                    table2 = pd.DataFrame.from_dict([res])
                    table_order = 2
                elif table_order == 2:
                    table3 = pd.DataFrame([word], columns=['Truth'])
                    table_order = 0
                    values = []
                    sentence_order = sentence_order + 1
            else:
                if table_order == 0:
                    table1 = table1.append(res, ignore_index=True)
                    table_order = 1
                elif table_order == 1:
                    table2 = table2.append(res, ignore_index=True)
                    table_order = 2
                elif table_order == 2:
                    table3 = table3.append({'Truth': word}, ignore_index=True)
                    table_order = 0
                    values = []
    
    table3["Truth"] = pd.to_numeric(table3["Truth"])
    return table1, table2, table3

if ditto_format:
    ditto_data_path = datasets_dir
    
    print("====================")
    print("Checking path...")
    print(datasets_dir)
    exists = os.path.exists(ditto_data_path)
    print(hp.decimate)
    print(hp.matches)
    if exists:
        print("Found!")
    else:
        print("NOT FOUND!!!")

else:
    magellan_data_path = datasets_dir
    table = pd.read_csv(magellan_data_path)

if exists:
    os.makedirs(model_dir, exist_ok=True)
    model_save_path = model_dir + model_name
    print("Model path: ")
    print(model_save_path)
    f = open(model_save_path + ".txt", "w")