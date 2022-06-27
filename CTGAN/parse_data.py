import argparse
import pandas as pd
import os
from distutils import util

pd.options.mode.chained_assignment = None  # default='warn'

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument('--matches', dest='matches', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--decimate", dest='decimate', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--ditto_parse", dest='ditto_parse', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--generator_type", type=int, default=1)

hp = parser.parse_args()

# If the data should be converted to Ditto Format
ditto_format = hp.ditto_parse

dataset_orig_data = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'

# If the dataset should be parsed to Ditto or Magellan format.
if ditto_format:
    datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/'
    datasets_goal_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Ditto/'
else:
    datasets_goal_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/'
    datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Ditto/'

if hp.generator_type == 1:
    datasets_dir += "/CTGAN/"
    datasets_goal_dir += "/CTGAN/"
if hp.generator_type == 2:
    datasets_dir += "/GPT-2_ft/"
    datasets_goal_dir += "/GPT-2_ft/"
if hp.generator_type == 3:
    datasets_dir += "/GPT-2_nft/"
    datasets_goal_dir += "/GPT-2_nft/"
if hp.generator_type == 4:
    datasets_dir += "/Augmentation/"
    datasets_goal_dir += "/Augmentation/"

job_name = hp.dataset + os.sep

datasets_dir += job_name + "train"
datasets_goal_dir += job_name + "train"

dataset_orig_data += "er_magellan" + os.sep + job_name + "train.txt"

if hp.matches:
    datasets_dir += ".matches"
    datasets_goal_dir += ".matches"

    dataset_orig_data += ".matches"
else:
    datasets_dir += ".non_matches"
    datasets_goal_dir += ".non_matches"
    dataset_orig_data += ".non-matches"

if hp.decimate:
    datasets_dir += ".decimated"
    datasets_goal_dir += ".decimated"
    dataset_orig_data += ".decimated"

if ditto_format:
    datasets_dir += ".csv"
    datasets_goal_dir += ".txt"
else:
    datasets_goal_dir += ".csv"
    datasets_dir += ".txt"


def gather_columns(path):
    with open(path, 'r', encoding='utf-8') as file:
        data = file.readline().rstrip()

    values = []
    value_writer = ""
    for side in data.split("\t"):
        for word in side.split(" "):
            if word == "COL":
                if value_writer != "" and value_writer != " ":
                    values.append(value_writer)
                    value_writer = ""
                read_column = True
            elif word == "VAL":
                read_column = False
            else:
                if read_column:
                    value_writer += word
    if value_writer != "":
        values.append(value_writer)
    values.append("Truth")
    return values


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

def magellan_reformater(table):
    table_columns = list(table.columns)
    total_attr = len(table_columns) - 1
    half_attr = int(total_attr / 2)


    ditto_formatted = ""
    for row in table.itertuples(False):
        value_writer = ""
        for i in range(0, half_attr):
            value_writer += "COL " + str(table_columns[i]) + " VAL " + str(row[i]) + " "
        value_writer += "\t"
        for i in range(half_attr, total_attr):
            value_writer += "COL " + str(table_columns[i]) + " VAL " + str(row[i]) + " "
        value_writer += "\t" + str(row[total_attr]) + "\n"
        ditto_formatted += value_writer

    return ditto_formatted


if ditto_format:
    magellan_data_path = datasets_dir
    table = pd.read_csv(magellan_data_path, encoding="utf-8")
    correct_columns = gather_columns(dataset_orig_data)
    table.columns = correct_columns
    finale_data = magellan_reformater(table)
else:
    ditto_data_path = datasets_dir
    
    with open(ditto_data_path, 'r', encoding='utf-8') as file:
        data = file.read()

    table_A, table_B, truth_table = ditto_reformater(data)
    
    # Conjoin tables together with Truth
    table_A = table_A.add_prefix("ltable_")
    table_B = table_B.add_prefix("rtable_")
    finale_data = pd.concat([table_A, table_B, truth_table], axis=1)

check_dir = datasets_goal_dir.split("train")[0]
os.makedirs(check_dir, exist_ok=True)

if ditto_format:
    with open(datasets_goal_dir, "a", encoding="utf-8") as file:
        file.write(finale_data)
else:
    finale_data.to_csv(datasets_goal_dir)
