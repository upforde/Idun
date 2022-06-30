import pandas as pd
import Levenshtein

# Function to asure tables have IDs for the Magellan pipeline.
def create_index_as_id (path):
    df = pd.read_csv(path)
    cols = df.columns.values.tolist()
    if 'ID' in cols:
        print("ID already exists!")
        return
    else:
        df['ID'] = df.index + 1
        print("Creating indices...")
        # Move ID column to first position. 
        df = df[ ['ID'] + [ col for col in df.columns if col != 'ID' ] ]
        df.to_csv(path, index=False)
        print("Indicies created succesfully!")

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

# Blackbox function for the blackbox blocker in Magellan.
def is_year_year(x, y):
    # x, y will be of type pandas series
    
    # get year attribute
    x = x['Year'] # Consists of multiple Years
    y = y['Year']

    x = x.split()

    if len(x) == 1:
        if x[0] == y:
            return False
        else:
            return True
    else:
        for year in x:
            if str(year) == str(y):
                return False
        return True

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

def clean_ABV_value(table):
    new_values = []
    for row in table.itertuples():
        new_values.append(row[4].split("%")[0] + " %")
    for i in range(0, len(new_values)):
        if "-" in new_values[i]:
            new_values[i] = "-"
    temp = pd.DataFrame(new_values, columns=["ABV"])
    table['ABV'] = temp
    return table

def magellan_reformater(table):
    table_columns = list(table.columns)
    total_attr = len(table_columns) - 1
    half_attr = total_attr / 2


    ditto_formatted = ""
    for row in table.itertuples(False):
        value_writer = ""
        for i in range(0, half_attr):
            value_writer += "COL " + table_columns[i] + " VAL " + row[i] + " "
        value_writer += "\t"
        for i in range(half_attr, total_attr):
            value_writer += "COL " + table_columns[i] + " VAL " + row[i] + " "
        value_writer += "\t" + row[total_attr] + "\n"
        ditto_formatted += value_writer

    return ditto_formatted

# For careful data ensuring.
def ensure_data(table, alike = True, threshold = 0.8 ):
    table_columns = list(table.columns)
    total_attr = len(table_columns) - 1
    half_attr = int(total_attr / 2)


    new_df = pd.DataFrame()
    for row in table.itertuples(index=False):
        similarity_dict = dict()
        for i in range(0, half_attr):
            try:
                similarity_dict[i] = Levenshtein.ratio(row[i], row[half_attr+i])
            except TypeError:
                similarity_dict[i] = 1
        if alike:
            if all(x > threshold for x in similarity_dict.values()):
                temp = pd.Series(row, table_columns)
                new_df = new_df.append(temp, ignore_index=True)
        else:
            if all(x < threshold for x in similarity_dict.values()):
                temp = pd.Series(row, table_columns)
                new_df = new_df.append(temp, ignore_index=True)

    new_df.rename(columns = {'Index':'_id'}, inplace = True)
    return new_df