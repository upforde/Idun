import py_entitymatching as em
import pandas as pd
import os
from sdv.tabular import CTGAN
from utils.utils import *

pd.options.mode.chained_assignment = None  # default='warn'

# If the data is in DITTO format or not.
ditto_format = False

# Data table directory and name.
datasets_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/GPT-2'
name_of_table = "new_sample_set.csv"

# Model training parameters.
epochs = 500
batch_total = 500

# Model directory and name to be saved. 
model_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/GPT-2'
model_name = "testind_IDUN.pkl"

# If the model should trained on "matched" or "non-matched" examples.
train_on_matched = True

if ditto_format:
    ditto_data_path = datasets_dir + os.sep + name_of_table
    
    with open(ditto_data_path, 'r', encoding='utf-8') as file:
        data = file.read()

    table_A, table_B, truth_table = ditto_reformater(data)
    
    # Conjoin tables together with Truth
    table_A = table_A.add_prefix("ltable_")
    table_B = table_B.add_prefix("rtable_")
    table = pd.concat([table_A, table_B, truth_table], axis=1)

else:
    print("Please perform the Magellan Sampling pipeline before proceeding.") 
    magellan_data_path = datasets_dir + os.sep + name_of_table
    table = pd.read_csv(magellan_data_path)

if train_on_matched:
    table_for_training = table[table['Truth'] > 0]
else:
    table_for_training = table[table['Truth'] < 1]

model = CTGAN(primary_key='_id', epochs=epochs, batch_size=batch_total)
model.fit(table_for_training)
model_save_path = model_dir + os.sep + model_name
model.save(model_save_path)