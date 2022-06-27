import argparse
from numpy import NaN
import pandas as pd
import os
import py_entitymatching as em


pd.options.mode.chained_assignment = None  # default='warn'

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--job_type", type=int, default=0)
parser.add_argument("--generator_type", type=int, default=0)


hp = parser.parse_args()

# Lists for naming conventions
generator_name = [
    r"CTGAN",
    r"GPT-2_ft",
    r"GPT-2_nft",
    r"Augmentation"
]

dataset_scenario_name = [
        r"Baseline",
        r"matches_non-matches",
        r"real_data_matches",
        r"real_data_non-matches",
        r"real_data_matches_non-matches",
        r"decimate_Baseline",
        r"decimate_matches_non-matches",
        r"decimate_real_data_matches",
        r"decimate_real_data_non-matches",
        r"decimate_real_data_matches_non-matches"
    ]

# Grab appropriate parameters.
job_type = hp.job_type
job_name = hp.dataset + os.sep
dataset_name = hp.dataset.replace(os.sep, "_")

# Real dataset directory
datasets_dir = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets' + os.sep

# What type of generator created our data
# CTGAN
if hp.generator_type == 0:
    synth_dir = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets_Synth\Magellan\CTGAN' + os.sep
# GPT-2 ft
elif hp.generator_type == 1:
    synth_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/GPT-2_ft/'
# GPT-2 non_ft
elif hp.generator_type == 2:
    synth_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/GPT-2_nft/'
# Augmentation
elif hp.generator_type == 3:
    synth_dir = r'/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Datasets_Synth/Magellan/Augmentation/'

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

def create_index_as_id_for_dataframe (table):
    cols = table.columns.values.tolist()
    if 'ID' in cols:
        print("ID already exists!")
        return table
    else:
        table['ID'] = table.index + 1
        print("Creating indices...")
        # Move ID column to first position. 
        table = table[ ['ID'] + [ col for col in table.columns if col != 'ID' ] ]
        return table
# 1. Take in the correct datasets depending on scenario, and if we are testing CTGAN or GPT-2 structured data.

# Baseline
if job_type == 0:
    real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt"

    with open(real_path, 'r', encoding='utf-8') as file:
            real_data = file.read()
        
    real_l_data, real_r_data, real_truth_data = ditto_reformater(real_data)
    
    table1 = real_l_data.add_prefix("ltable_")
    table2 = real_r_data.add_prefix("rtable_")
    training_data = pd.concat([table1, table2, real_truth_data], axis=1)

# Matches + Non-Matches
elif job_type == 1:
    match_synth_path = synth_dir + job_name + "train.matches.csv"
    non_match_synth_path = synth_dir + job_name + "train.non_matches.csv"

    match_synth_data = pd.read_csv(match_synth_path, encoding="utf-8")
    non_match_synth_data = pd.read_csv(non_match_synth_path, encoding="utf-8")

    training_data = pd.concat([match_synth_data, non_match_synth_data], ignore_index=True) # NOTE: Coorect?

# Real data + Matches
elif job_type == 2:
    match_synth_path = synth_dir + job_name + "train.matches.csv"
    real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt"

    match_synth_data = pd.read_csv(match_synth_path, encoding="utf-8")
    
    with open(real_path, 'r', encoding='utf-8') as file:
            real_data = file.read()
        
    real_l_data, real_r_data, real_truth_data = ditto_reformater(real_data)
    
    table1 = real_l_data.add_prefix("ltable_")
    table2 = real_r_data.add_prefix("rtable_")
    real_table = pd.concat([table1, table2, real_truth_data], axis=1)

    training_data = pd.concat([match_synth_data, real_table], ignore_index=True) 

# Real data + Non-Matches
elif job_type == 3:
    non_match_synth_path = synth_dir + job_name + "train.non_matches.csv"
    real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt"

    non_match_synth_data = pd.read_csv(non_match_synth_path, encoding="utf-8")
    
    with open(real_path, 'r', encoding='utf-8') as file:
            real_data = file.read()
        
    real_l_data, real_r_data, real_truth_data = ditto_reformater(real_data)
    
    table1 = real_l_data.add_prefix("ltable_")
    table2 = real_r_data.add_prefix("rtable_")
    real_table = pd.concat([table1, table2, real_truth_data], axis=1)

    training_data = pd.concat([non_match_synth_data, real_table], ignore_index=True) 

# Real data + Matches + Non-Matches
elif job_type == 4:
    match_synth_path = synth_dir + job_name + "train.matches.csv"
    non_match_synth_path = synth_dir + job_name + "train.non_matches.csv"
    real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt"

    match_synth_data = pd.read_csv(match_synth_path, encoding="utf-8")
    non_match_synth_data = pd.read_csv(non_match_synth_path, encoding="utf-8")
    
    with open(real_path, 'r', encoding='utf-8') as file:
            real_data = file.read()
        
    real_l_data, real_r_data, real_truth_data = ditto_reformater(real_data)
    
    table1 = real_l_data.add_prefix("ltable_")
    table2 = real_r_data.add_prefix("rtable_")
    real_table = pd.concat([table1, table2, real_truth_data], axis=1)

    training_data = pd.concat([match_synth_data, non_match_synth_data, real_table], ignore_index=True) 

# decimate Baseline
elif job_type == 5:
    match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.matches.decimated"
    non_match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.non_matches.decimated"

    with open(match_real_path, 'r', encoding='utf-8') as file:
            match_real_data = file.read()
        
    match_real_l_data, match_real_r_data, match_real_truth_data = ditto_reformater(match_real_data)

    match_table1 = match_real_l_data.add_prefix("ltable_")
    match_table2 = match_real_r_data.add_prefix("rtable_")
    match_real_table = pd.concat([match_table1, match_table2, match_real_truth_data], axis=1)

    with open(non_match_real_path, 'r', encoding='utf-8') as file:
            non_match_real_data = file.read()
        
    non_match_real_l_data, non_match_real_r_data, non_match_real_truth_data = ditto_reformater(non_match_real_data)

    non_match_table1 = non_match_real_l_data.add_prefix("ltable_")
    non_match_table2 = non_match_real_r_data.add_prefix("rtable_")
    non_match_real_table = pd.concat([non_match_table1, non_match_table2, non_match_real_truth_data], axis=1)

    training_data = pd.concat([match_real_table, non_match_real_table], ignore_index=True) 

# decimate Matches + Non-Matches
elif job_type == 6:
    match_synth_path = synth_dir + job_name + "train.matches.decimated.csv"
    non_match_synth_path = synth_dir + job_name + "train.non_matches.decimated.csv"

    match_synth_data = pd.read_csv(match_synth_path, encoding="utf-8")
    non_match_synth_data = pd.read_csv(non_match_synth_path, encoding="utf-8")

    training_data = pd.concat([match_synth_data, non_match_synth_data], ignore_index=True) 

# decimate Real data + Matches
elif job_type == 7:
    match_synth_path = synth_dir + job_name + "train.matches.decimated.csv"
    match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.matches.decimated"
    non_match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.non_matches.decimated"

    match_synth_data = pd.read_csv(match_synth_path, encoding="utf-8")

    with open(match_real_path, 'r', encoding='utf-8') as file:
            match_real_data = file.read()
        
    match_real_l_data, match_real_r_data, match_real_truth_data = ditto_reformater(match_real_data)

    match_table1 = match_real_l_data.add_prefix("ltable_")
    match_table2 = match_real_r_data.add_prefix("rtable_")
    match_real_table = pd.concat([match_table1, match_table2, match_real_truth_data], axis=1)

    with open(non_match_real_path, 'r', encoding='utf-8') as file:
            non_match_real_data = file.read()
        
    non_match_real_l_data, non_match_real_r_data, non_match_real_truth_data = ditto_reformater(non_match_real_data)

    non_match_table1 = non_match_real_l_data.add_prefix("ltable_")
    non_match_table2 = non_match_real_r_data.add_prefix("rtable_")
    non_match_real_table = pd.concat([non_match_table1, non_match_table2, non_match_real_truth_data], axis=1)

    training_data = pd.concat([match_synth_data, match_real_table, non_match_real_table], ignore_index=True) 

# decimate Real data + Non-Matches
elif job_type == 8:
    non_match_synth_path = synth_dir + job_name + "train.non_matches.decimated.csv"
    match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.matches.decimated"
    non_match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.non_matches.decimated"

    non_match_synth_data = pd.read_csv(non_match_synth_path, encoding="utf-8")

    with open(match_real_path, 'r', encoding='utf-8') as file:
            match_real_data = file.read()
        
    match_real_l_data, match_real_r_data, match_real_truth_data = ditto_reformater(match_real_data)

    match_table1 = match_real_l_data.add_prefix("ltable_")
    match_table2 = match_real_r_data.add_prefix("rtable_")
    match_real_table = pd.concat([match_table1, match_table2, match_real_truth_data], axis=1)

    with open(non_match_real_path, 'r', encoding='utf-8') as file:
            non_match_real_data = file.read()
        
    non_match_real_l_data, non_match_real_r_data, non_match_real_truth_data = ditto_reformater(non_match_real_data)

    non_match_table1 = non_match_real_l_data.add_prefix("ltable_")
    non_match_table2 = non_match_real_r_data.add_prefix("rtable_")
    non_match_real_table = pd.concat([non_match_table1, non_match_table2, non_match_real_truth_data], axis=1)

    training_data = pd.concat([non_match_synth_data, match_real_table, non_match_real_table], ignore_index=True) 

# decimate Real data + Matches + Non-Matches
elif job_type == 9:
    match_synth_path = synth_dir + job_name + "train.matches.decimated.csv"
    non_match_synth_path = synth_dir + job_name + "train.non_matches.decimated.csv"
    match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.matches.decimated"
    non_match_real_path = datasets_dir + "er_magellan" + os.sep + job_name + "train.txt.non_matches.decimated"

    match_synth_data = pd.read_csv(match_synth_path, encoding="utf-8")
    non_match_synth_data = pd.read_csv(non_match_synth_path, encoding="utf-8")

    with open(match_real_path, 'r', encoding='utf-8') as file:
            match_real_data = file.read()
        
    match_real_l_data, match_real_r_data, match_real_truth_data = ditto_reformater(match_real_data)

    match_table1 = match_real_l_data.add_prefix("ltable_")
    match_table2 = match_real_r_data.add_prefix("rtable_")
    match_real_table = pd.concat([match_table1, match_table2, match_real_truth_data], axis=1)

    with open(non_match_real_path, 'r', encoding='utf-8') as file:
            non_match_real_data = file.read()
        
    non_match_real_l_data, non_match_real_r_data, non_match_real_truth_data = ditto_reformater(non_match_real_data)

    non_match_table1 = non_match_real_l_data.add_prefix("ltable_")
    non_match_table2 = non_match_real_r_data.add_prefix("rtable_")
    non_match_real_table = pd.concat([non_match_table1, non_match_table2, non_match_real_truth_data], axis=1)

    training_data = pd.concat([match_synth_data, non_match_synth_data, match_real_table, non_match_real_table], ignore_index=True) 

# 2. Add matching valid data for the scenario sent in by the arguments. Save cutoff index.

cutoff = len(training_data.index)

valid_path = datasets_dir + "er_magellan" + os.sep + job_name + "valid.txt"

with open(valid_path, 'r', encoding='utf-8') as file:
            valid_data_text = file.read()
        
valid_l_data, valid_r_data, valid_truth_data = ditto_reformater(valid_data_text)

valid_table1 = valid_l_data.add_prefix("ltable_")
valid_table2 = valid_r_data.add_prefix("rtable_")
valid_data = pd.concat([valid_table1, valid_table2, valid_truth_data], axis=1)

magellan_data = pd.concat([training_data, valid_data], ignore_index=True)

# 3. Set up table A and B with IDs as index, then load it into Magellan.

split_index = int((len(magellan_data.columns) - 1) / 2)
truth_table = magellan_data.iloc[:,-1]
magellan_data = magellan_data.iloc[:,:-1]
table_A = magellan_data.iloc[:, :-split_index]
table_B = magellan_data.iloc[:,-split_index:]

table_A.columns = table_A.columns.str.replace('ltable_', "")
table_B.columns = table_B.columns.str.replace('rtable_', "")

A_meta = create_index_as_id_for_dataframe(table_A)
B_meta = create_index_as_id_for_dataframe(table_B)

em.set_key(A_meta, 'ID')
em.set_key(B_meta, 'ID')

# 4. Concat all tables together to form table C, and save it to temporary directory. 

table1 = A_meta.add_prefix("ltable_")
table2 = B_meta.add_prefix("rtable_")
table_C = pd.concat([table1, table2, truth_table], axis=1)

temp_C_dir = r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets\Temp_Tables" + os.sep

path_to_table_C = temp_C_dir
path_to_table_C += generator_name[hp.generator_type] + os.sep
path_to_table_C += dataset_scenario_name[hp.job_type] + os.sep

os.makedirs(path_to_table_C, exist_ok=True)

path_to_table_C += dataset_name + "_table_C.csv"
table_C.to_csv(path_to_table_C, encoding="utf-8", index_label="_id")

# 5. Take care of attribute correspondance in Magellan.
def check_priority(attribute):
    if attribute == "boolean":
        return 6
    elif attribute == "numeric":
        return 5
    elif attribute == "str_gt_10w":
        return 4
    elif attribute == "str_bt_5w_10w":
        return 3
    elif attribute == "str_bt_1w_5w":
        return 2
    elif attribute == "str_eq_1w":
        return 1
    else:
        return 0

def convert_from_p_to_attr(priority):
    if priority == 6:
        return "boolean"
    elif priority == 5:
        return "numeric"
    elif priority == 4:
        return "str_gt_10w"
    elif priority == 3:
        return "str_bt_5w_10w"
    elif priority == 2:
        return "str_bt_1w_5w"
    elif priority == 1:
        return "str_eq_1w"
    else:
        return "str_eq_1w"

def check_attr_corresp():
    A_attr_dict = em.get_attr_types(A_meta)
    B_attr_dict = em.get_attr_types(B_meta)
    all_attr = list(A_attr_dict.keys())
    del all_attr[-1]
    unsolved_attr = []
    for attribute in all_attr:
        if A_attr_dict[attribute] != B_attr_dict[attribute]:
            unsolved_attr.append(attribute)
    if len(unsolved_attr) != 0:
        for unsolved in unsolved_attr:
            a_p = check_priority(A_attr_dict[unsolved])
            b_p = check_priority(B_attr_dict[unsolved])
            if a_p < b_p:
                A_attr_dict[unsolved] = B_attr_dict[unsolved]
            else:
                B_attr_dict[unsolved] = A_attr_dict[unsolved]
    return A_attr_dict, B_attr_dict
    
# str_eq_1w, str_bt_1w_5w, str_bt_5w_10w, str_gt_10w, boolean or numeric
# Remember to update Magellan attributeutils...
atypes1, atypes2 = check_attr_corresp()


# 6. Generate necessary embedding tables. Tokenizer, Sim, Feature Table.
block_t = em.get_tokenizers_for_blocking()
block_s = em.get_sim_funs_for_blocking()
block_c = em.get_attr_corres(A_meta, B_meta)
feature_table  = em.get_features(A_meta, B_meta, atypes1, atypes2, block_c, block_t, block_s )

# 7. Load the temporary table in as Table C. 

# A_meta.fillna(0)
# B_meta.fillna(0)
C_meta = em.read_csv_metadata(path_to_table_C, key='_id',
                                    fk_ltable='ltable_ID', fk_rtable='rtable_ID',
                                    ltable=A_meta, rtable=B_meta)


dataset_train = C_meta.iloc[:cutoff,:]
dataset_test = C_meta.iloc[cutoff:,:]
# Update catalog
em.catalog.catalog_manager.init_properties(dataset_train)
em.catalog.catalog_manager.copy_properties(C_meta, dataset_train)

em.catalog.catalog_manager.init_properties(dataset_test)
em.catalog.catalog_manager.copy_properties(C_meta, dataset_test)

print(" ========= Training =========")
print("Number of matches: " + str(sum(dataset_train['Truth'] > 0)))
print("Number of non-matches: " + str(sum(dataset_train['Truth'] < 1)))
print(" ========= Validation =========")
print("Number of matches: " + str(sum(dataset_test['Truth'] > 0)))
print("Number of non-matches: " + str(sum(dataset_test['Truth'] < 1)))

# 8. Set up necessary tables for Table C and load matchers. 

# Convert the labeled data to feature vectors using the feature table
feature_vector_table_train = em.extract_feature_vecs(dataset_train, 
                            feature_table=feature_table, 
                            attrs_after='Truth',
                            show_progress=False)

# Handle missing data. Inplace is required to keep correct object type, and maintaining "Meta-Data".
feature_vector_table_train.fillna(value=0, inplace=True)

rf = em.RFMatcher()

# Get the attributes to be projected while training
attrs_to_be_excluded = []
attrs_to_be_excluded.extend(['_id', 'ltable_ID', 'rtable_ID'])

# Train using feature vectors from the labeled data.
rf.fit(table=feature_vector_table_train, exclude_attrs=attrs_to_be_excluded, target_attr='Truth')

feature_vector_table_test = em.extract_feature_vecs(dataset_test, feature_table=feature_table,
                             attrs_after='Truth',
                             show_progress=False)

# Handle NaN values.
feature_vector_table_test.fillna(value=0, inplace=True)

# Get the attributes to be excluded while predicting
attrs_to_be_excluded = []
attrs_to_be_excluded.extend(['_id', 'ltable_ID', 'rtable_ID', 'Truth'])

# Predict the matches
predictions = rf.predict(table=feature_vector_table_test, exclude_attrs=attrs_to_be_excluded,                          
              append=True, target_attr='predicted', inplace=False)

# Project the attributes
# predictions.head(10)

# Show only rows which are predicted as "matched".
# df_only_matched = predictions.loc[predictions['predicted'] == 1]
# df_only_matched.head(100)

# Evaluate prediction results.
eval_result = em.eval_matches(predictions, 'Truth', 'predicted')
# em.print_eval_summary(eval_result)
f_score = eval_result['f1']

datasets_paths = [
    r"Dirty_DBLP-ACM",
    r"Dirty_DBLP-GoogleScholar",
    r"Dirty_iTunes-Amazon",
    r"Dirty_Walmart-Amazon",
    r"Structured_Amazon-Google",
    r"Structured_Beer",
    r"Structured_DBLP-ACM",
    r"Structured_DBLP-GoogleScholar",
    r"Structured_Fodors-Zagats",
    r"Structured_iTunes-Amazon",
    r"Structured_Walmart-Amazon",
    r"Textual_Abt-Buy"
    ]

dataset_scenario_path = [
        r"matches_non-matches",
        r"real_data_matches",
        r"real_data_non-matches",
        r"real_data_matches_non-matches",
        r"decimate_matches_non-matches",
        r"decimate_real_data_matches",
        r"decimate_real_data_non-matches",
        r"decimate_real_data_matches_non-matches"
    ]

generator_type_name = [
    r"Baseline",
    r"CTGAN",
    r"GPT-2_ft",
    r"GPT-2_nft",
    r"Augmentation"
]

result_dir = r"/cluster/home/alekssim/Documents/IDUN/Idun/CTGAN/Results/"

# Make result directories
for i in range(0, 8):
    save_score_path = result_dir + dataset_scenario_path[i] + os.sep
    os.makedirs(dataset_scenario_path[i], exist_ok=True)

# TODO: If the file bugs out from multiple processes, use a while_loop which checks for last time of modification to the result file.
# If one of the baseline scenarios, create the baseline across every <data_scenario> data_set.
if job_type == 0:
    for i in range(0, 8):
        save_score_path = result_dir + dataset_scenario_path[i] + os.sep + "result.csv"
        if os.path.exists(save_score_path):
            result_table = pd.read_csv(save_score_path, encoding="utf-8")
            if result_table.loc["Baseline", dataset_name] is not NaN:
                continue
        else:
            if i < 4:
                result_table = pd.DataFrame(columns = datasets_paths, index = generator_type_name)
            else:
                d_generator_type_name = list(generator_type_name)
                d_generator_type_name.insert(1, "d_Baseline")
                result_table = pd.DataFrame(columns = datasets_paths, index = d_generator_type_name)
        new_result = pd.DataFrame([f_score], columns=dataset_name, index="Baseline")
        result_table = pd.concat([result_table, new_result])
        result_table.to_csv(save_score_path, mode='w', encoding='utf-8')
elif job_type == 5:
    for i in range(4, 8):
        save_score_path = result_dir + dataset_scenario_path[i] + os.sep + "result.csv"
        if os.path.exists(save_score_path):
            result_table = pd.read_csv(save_score_path, encoding="utf-8")
            if result_table.loc["d_Baseline", dataset_name] is not NaN:
                continue
        else:
            d_generator_type_name = list(generator_type_name)
            d_generator_type_name.insert(1, "d_Baseline")
            result_table = pd.DataFrame(columns = datasets_paths, index = d_generator_type_name)
        new_result = pd.DataFrame([f_score], columns=dataset_name, index="d_Baseline")
        result_table = pd.concat([result_table, new_result])
        result_table.to_csv(save_score_path, mode='w', encoding='utf-8')
else:
    save_score_path = result_dir + dataset_scenario_name[job_type] + os.sep + "result.csv"
    result_table = pd.read_csv(save_score_path, encoding="utf-8")
    new_result = pd.DataFrame([f_score], columns=dataset_name, index=generator_name[hp.generator_type])
    result_table = pd.concat([result_table, new_result])
    result_table.to_csv(save_score_path, mode='w', encoding='utf-8')