from utils import *
from IPython.display import display, HTML
import pandas as pd
import os

# If the data is in DITTO format or not.
ditto_format = True

# Data table directory and name.
datasets_dir = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets\er_magellan\Dirty\DBLP-ACM'
name_of_table = "check.txt"

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

# Cleaning table B ...
# table_B = clean_ABV_value(table_B)

# Display table
#display(HTML(table.to_html()))
