from random import seed, random
import os, time, string, copy, argparse

def pair_to_string(pair):
    '''
    Takes in the pair dictionary and returns the string version of the pair dictionary in ditto format
    '''
    string = ""

    for key in pair.keys():
        if key == "Match": continue
        string += "COL " + key + " VAL " + pair[key][0]
    
    string += "\t"

    for key in pair.keys():
        if key == "Match": continue
        string += "COL " + key + " VAL " + pair[key][1]
    
    string += "\t" + str(pair["Match"])

    return string

def current_milli_time():
    return round(time.time() * 1000)

def create_new_pair(pair1, pair2):
    '''
    Makes a new pair out of two other pairs.
    '''
    new_pair = {}

    for key in pair1.keys():
        if key == "Match": new_pair[key] = 0
        else: 
            if random() > 0.5: new_pair[key] = [pair1[key][round(random())], pair2[key][round(random())]]
            else: new_pair[key] = pair1[key]

    return new_pair

def create_new_match(parent):
    '''
    Creates a new match by mutating some letters in a previous match
    '''
    # Copy the parent to not mutate
    new_match = copy.deepcopy(parent)
    # Start mutation of n elements
    for _ in range(5):
        # Pick a random letter of a random element from the parent to replace
        rand_key = list(new_match.keys())[round((len(new_match.keys())-2)*random())]
        rand_string = round(random())
        rand_letter = round((len(new_match[rand_key][rand_string])-1)*random())

        # Replace one letter from the chosen element
        new_string = ""
        for i in range(len(list(new_match[rand_key][rand_string]))):
            if i != rand_letter: new_string += str((list(new_match[rand_key][rand_string])[i]))
            else: new_string += str(list(alphabet_list)[round((len(alphabet_list)-1)*random())])
        new_match[rand_key][rand_string] = new_string

    return new_match

IDUN_PATH ="/cluster/home/danilasm/masters/Idun/Augmentation/"

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str, default="Structured/Beer")
parser.add_argument("--size", type=str, default=None)
parser.add_argument("--decimate", type=str, default="False")
hp = parser.parse_args()

# Parsing arguments and creating variable names
SAVE_LOCATION = IDUN_PATH + "Generated/" + hp.dataset

if "/" in hp.dataset: 
    train_data = IDUN_PATH + "Datasets/er_magellan/" + hp.dataset + "/train.txt"        # Train dataset, depending on if they're 
else:                                                                                   # from the er_magellan datasets or the wdc datasets
    train_data = IDUN_PATH + "Datasets/wdc/" + hp.dataset + "/train.txt." + hp.size


if "/" not in hp.dataset: 
    SAVE_LOCATION += f"_{hp.size}"

if hp.decimate == "True":
    SAVE_LOCATION += "_decimated/"                                                   # Adding postfix for if to use the decimated
    train_data += ".decimated"

if not os.path.isdir(SAVE_LOCATION): os.makedirs(SAVE_LOCATION)

non_matches = []
matches = []

with open(train_data) as file:
    lines = file.readlines()
    
    for line in lines:
        pair = {}
        # Each item of the pair is split up by a \t
        parts = line.split("\t")
        
        # First item
        first = parts[0].split("COL ")
        for part in first:
            if part == '': continue
            colval = part.split(" VAL ")
            pair[colval[0]] = [colval[1]]

        # Second item
        second = parts[1].split("COL ")
        for part in second:
            if part == '': continue
            colval = part.split(" VAL ")
            pair[colval[0]].append(colval[1])

        # Adding match parameter
        pair["Match"] = int(parts[2])

        if pair["Match"] == 1: matches.append(pair)
        else: non_matches.append(pair)
    file.close()

new_non_matches = []
new_matches = []

seed(current_milli_time())

alphabet_list = list(string.ascii_lowercase) + list(string.digits)

for _ in range(len(matches)):
    # Pick a random parent from matches
    parent = matches[round((len(matches)-1)*random())]

    # Create and append the new match
    new_matches.append(create_new_match(parent))  

for _ in range(len(non_matches)):
    # Getting two random pairs to make a new pair with
    # There can never be two pairs that are matches, but there can be two non-match pairs
    if random() > 0.5:
        pair1 = non_matches[round((len(non_matches)-1)*random())]
        if random() > 0.5: pair2 = non_matches[round((len(non_matches)-1)*random())]
        else: pair2 = matches[round((len(matches)-1)*random())]
    else: 
        pair1 = matches[round((len(matches)-1)*random())]
        pair2 = non_matches[round((len(non_matches)-1)*random())]
    
    # Append the new pair into the new pairs array
    new_non_matches.append(create_new_pair(pair1, pair2))


with open(SAVE_LOCATION + "augmented_only.txt", "a") as file:
    for match in new_matches: file.write(pair_to_string(match) + "\n")
    for non_match in new_non_matches: file.write(pair_to_string(non_match) + "\n")

with open(SAVE_LOCATION + "real_pluss_all.txt", "a") as file:
    for match in matches: file.write(pair_to_string(match) + "\n")
    for match in new_matches: file.write(pair_to_string(match) + "\n")
    for non_match in non_matches: file.write(pair_to_string(non_match) + "\n")
    for non_match in new_non_matches: file.write(pair_to_string(non_match) + "\n")

with open(SAVE_LOCATION + "real_pluss_match.txt", "a") as file:
    for match in matches: file.write(pair_to_string(match) + "\n")
    for match in new_matches: file.write(pair_to_string(match) + "\n")
    for non_match in non_matches: file.write(pair_to_string(non_match) + "\n")

with open(SAVE_LOCATION + "real_pluss_non_match.txt", "a") as file:
    for match in matches: file.write(pair_to_string(match) + "\n")
    for non_match in non_matches: file.write(pair_to_string(non_match) + "\n")
    for non_match in new_non_matches: file.write(pair_to_string(non_match) + "\n")
