import random

class ditto_data_maker():
  def __init__(self, data_string):
    '''
      Takes in the generated strig, splits it up and creates a dictionary that contains the original columns from the left side, and the data from both left and right in those columns
    '''

    sides = data_string.split("\t")

    self.data = {}
    for field in sides[0].split("COL"):                                         # Setting up the left side
      if "VAL" not in field: continue                                           # Error handling
      col, val = field.split("VAL")                                             # Getting the column and value data
      self.data[col.strip()] = [val.strip()]                                    # Inserting data into internal dictionary to aggregate the true columns

    if "COL" not in sides[1]: return                                            # Error handling

    for field in sides[1].split("COL"):                                         # Setting up the right side
      if "VAL" not in field: continue                                           # Error handling

      colval = field.split("VAL")                                               # Finding the data in the string
      col = colval[0]                                                           # Since this is the generated part, it needs some more error handling
      val = colval[1]
      for category in list(self.data.keys()):                                   # Since the category might be slightly misspelled due to generation mishaps in GPT-2
        if category.lower() in col.strip().lower():                             # some error handling / data processing is needed. A better method for this might be
          self.data[category].append(val.strip())                               # out there, but I'm not willing to find it right now

    for col in list(self.data.keys()):                                          # Error handling
      if len(self.data[col]) <= 2: continue                                     # Due to the way generated strings might generate more than one "VAL" field after a COL
      new = []                                                                  # one of the fiends generated is chosen at random to be the field used. Out of experience
      new.append(self.data[col][0])                                             # I can say that they tend to be similar if not identical, so this shouldn't affect the string
      new.append(self.data[col][random.randint(1, len(self.data[col])-1)])
      self.data[col] = new
    
  def isValid(self):
    '''
      Validates the string, checking wether the amount of data is correct or not
    '''

    valid = True                                                                # Just checking wether each field has 2 entries
    for col in list(self.data.keys()):                                          # If more or less, then the string won't work, and thus
      if len(self.data[col]) != 2:                                              # the generated string is invalid
        valid = False
        break
    return valid

  def generate_string(self, matching_index):
    '''
      Generates a Ditto string out of the data in the dictionary, and puts the matching index at the back
    '''

    string = ""

    for key in list(self.data.keys()):                                          # Doing the left side
      if string != "": string += " "
      string += "COL " + key + " VAL " + self.data[key][0]
    
    string += '\t'

    for key in list(self.data.keys()):                                          # Doing the right side
      if not string.endswith('\t'): string += " "
      string += "COL " + key + " VAL " + self.data[key][1]
    
    string += '\t'
    string += str(matching_index)                                               # Adding the match index (0 or 1)

    return string