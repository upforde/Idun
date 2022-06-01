import pandas as pd
import os
from sdv.tabular import CTGAN

pd.options.mode.chained_assignment = None  # default='warn'

# If the data is in DITTO format or not.
ditto_format = True

# Data table directory and name.
# datasets_dir = r'Datasets/er_magellan/Structured/Amazon-Google'
name_of_table = "train.txt"

# Model training parameters.
batch_total = 500
epochs = 200


# Model directory and name to be saved. 
model_name = "structured_um_500_200.pkl"

# If the model should trained on "matched" or "non-matched" examples.
train_on_matched = False

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
    ditto_data_path = name_of_table
    
    with open(ditto_data_path, 'r', encoding='utf-8') as file:
        data = file.read()

    table_A, table_B, truth_table = ditto_reformater(data)
    
    # Conjoin tables together with Truth
    table_A = table_A.add_prefix("ltable_")
    table_B = table_B.add_prefix("rtable_")
    table = pd.concat([table_A, table_B, truth_table], axis=1)

else:
    # print("Please perform the Magellan Sampling pipeline before proceeding.") 
    magellan_data_path = name_of_table
    table = pd.read_csv(magellan_data_path)

if train_on_matched:
    table_for_training = table[table['Truth'] > 0]
else:
    table_for_training = table[table['Truth'] < 1]

model = CTGAN(epochs=epochs, batch_size=batch_total)
model.fit(table_for_training)
model_save_path = model_name
model.save(model_save_path)