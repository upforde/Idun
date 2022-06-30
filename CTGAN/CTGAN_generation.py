import argparse
import pandas as pd
import os
from distutils import util
from sdv.tabular import CTGAN
import Levenshtein

pd.options.mode.chained_assignment = None  # default='warn'

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument('--matches', dest='matches', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--decimate", dest='decimate', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--threshold", dest='threshold', type=float)
parser.add_argument("--drop_dupes", dest='drop_dupes', type=lambda x:bool(util.strtobool(x)))
parser.add_argument("--size", type=str, default=None)


hp = parser.parse_args()

# If the data is in DITTO format or not.
ditto_format = True

# Model directory to be loaded from.
model_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Models/'

# Dataset directory to be loaded from and saved at.
datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets/'
synth_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/'

synth_name = ""

# Model name.
job_name = hp.dataset + os.sep

model_name = hp.dataset
model_name = model_name.replace(os.sep, "_") 

if os.sep in hp.dataset:
    datasets_dir += "er_magellan" + os.sep + job_name + "train.txt"
    model_dir += "er_magellan" + os.sep + job_name
    synth_dir += "er_magellan" + os.sep + job_name
    synth_name += "train"
else:
    model_name += "_" + hp.size
    datasets_dir += "wdc" + os.sep + job_name + "train.txt." + hp.size
    model_dir += "wdc" + os.sep + job_name + hp.size + os.sep
    synth_dir += "wdc" + os.sep + job_name
    synth_name +=  "train." + hp.size

if hp.matches:
    datasets_dir += ".matches"
    model_name += "_matches"
    synth_name += ".matches"
else:
    datasets_dir += ".non_matches"
    model_name += "_non_matches"
    synth_name += ".non_matches"

if hp.decimate:
    datasets_dir += ".decimated"
    model_name += "_decimated"
    synth_name += ".decimated"

model_name += ".pkl"
synth_name += ".csv"

# Method to ensure that each attribute is either different (for non-matched cases), or alike (for matched cases).
# Uses the Levhenstein distance between each attribute, and adds it all together.
# Adding it together gives lee-way for somewhat different attributes.
def ensure_data(table, alike = True, threshold = 0.8 ):
    if table is None or len(table.index) == 0:
        return table
    table_columns = list(table.columns)
    total_attr = len(table_columns) - 1 # We do not consider Truth
    half_attr = int(total_attr / 2)


    new_df = pd.DataFrame()
    for row in table.itertuples(index=False):
        similarity_dict = dict()
        for i in range(0, half_attr):
            try:
                similarity_dict[i] = Levenshtein.ratio(row[i], row[half_attr+i])
            except TypeError:
                similarity_dict[i] = threshold
        variance_allowed = (1 - threshold) * (0.5 * (threshold * total_attr))
        new_threshold = (threshold * len(similarity_dict)) + variance_allowed
        total_similarity = 0
        for x in similarity_dict.values():
            total_similarity += x
        if alike:
            if total_similarity > new_threshold:
                temp = pd.Series(row, table_columns)
                new_df = new_df.append(temp, ignore_index=True)
        else:
            if total_similarity < new_threshold:
                temp = pd.Series(row, table_columns)
                new_df = new_df.append(temp, ignore_index=True)

    new_df.rename(columns = {'Index':'_id'}, inplace = True)
    return new_df


train = []

with open(datasets_dir, encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines: train.append(line)

# If decimated, we are makes 9 times the amount of data to fill up the dataset to its original size.
if hp.decimate:
    amount = len(train) * 9
else:
    amount = len(train)

# Make Synthethic data path if it does not exist.
os.makedirs(synth_dir, exist_ok=True)

model_save_path = model_dir + model_name
model = CTGAN.load(model_save_path)

synth_save_path = synth_dir + synth_name


count = 0

# Function to generate data. (obsolete)
def generate_data(matches, drop_dupes):
    if count < amount:
        generated_data = model.sample(num_rows=amount)
    if matches:
        generated_data = ensure_data(generated_data, True, hp.threshold)
    else:
        generated_data = ensure_data(generated_data, False, hp.threshold)
    if hp.drop_dupes:
            if generated_data is not None or len(generated_data.index) != 0:
                generated_data = generated_data.drop_duplicates()
    if generated_data is not None and len(generated_data.index) != 0:
        generated_data.to_csv(synth_save_path, mode='a', header=not os.path.exists(synth_save_path), encoding='utf-8', index=False)
        count += len(generated_data.index)

# We generate data, and use the ensure_data method to toss away unsufficient data.
# We generate until we have the desired amount of data.
while count < amount:
    print("The amount needed to be generated is: " + str(amount - count))
    generated_data = model.sample(num_rows=amount, output_file_path='disable')
    if hp.matches:
        generated_data = ensure_data(generated_data, True, hp.threshold)
    else:
        generated_data = ensure_data(generated_data, False, hp.threshold)
    if hp.drop_dupes:
            if generated_data is not None or len(generated_data.index) != 0:
                generated_data = generated_data.drop_duplicates()
    if generated_data is not None and len(generated_data.index) != 0:
        generated_data.to_csv(synth_save_path, mode='a', header=not os.path.exists(synth_save_path), encoding='utf-8', index=False)
        count += len(generated_data.index)

