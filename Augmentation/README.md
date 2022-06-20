# Evolution-inspired Data Augmentation 

## Generating non-matches
The generation of non-matching entries is inspired by the crossover method in evolutionary algorithms. In essence, two entries are selected from all non-matching entries in the dataset, and their attributes are swapped at random, thus creating a new entry.

## Generating matches
The generation of matching entries is inspired by the mutation method in evolutionary algorithms. An entry is selected at random from the set of matching entries in the dataset. All letters in the attributes of the entry have a chance of mutating into a different letter.