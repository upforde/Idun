import os

val1 = input("Rename Augmenentation or GPT-2? [a/g]")
if val1 == "g":
    val2 = input("Fine-tuned or Non-Fine-tuned? [f/n]")
    if val2 == "f":
        path = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets_Synth\Ditto\GPT-2_ft' + os.sep
    elif val2 == "n":
        path = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets_Synth\Ditto\GPT-2_nft' + os.sep
    else:
        print("Darn, so close.")
elif val1 == "a":
    path = r'C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Datasets_Synth\Ditto\Augmentation' + os.sep
else:
    print("Nope.")

root_dir = os.listdir(path)

if val1 == "g":
    for folder1 in root_dir:
        folder1 = os.path.join(path, folder1)
        for folder2 in os.listdir(folder1):
            folder2 = os.path.join(folder1, folder2)
            for file in os.listdir(folder2):
                if "non_matches" in file:
                    new_name = file.split("non_matches")
                    new_name = "train" + ".non_matches" + new_name[1]
                else:
                    new_name = file.split("matches")
                    new_name = "train" + ".matches" + new_name[1]
                os.rename(os.path.join(folder2, file), os.path.join(folder2, new_name))

elif val1 == "a":
    names_to_be = [
        r"train.matches.txt",
        r"train.non_matches.txt",
        r"train.matches.decimated.txt",
        r"train.non_matches.decimated.txt"
    ]

    names_to_be_gone = [
        r"generated_matches.txt",
        r"generated_non_matches.txt",
        r"generated_matches_decimated.txt",
        r"generated_non_matches_decimated.txt"
    ]

    for folder1 in root_dir:
        folder1 = os.path.join(path, folder1)
        for folder2 in os.listdir(folder1):
            folder2 = os.path.join(folder1, folder2)
            for file in os.listdir(folder2):
                rename = False
                for i in range(0, 4):
                    if file == names_to_be_gone[i]:
                        new_name = names_to_be[i]
                        rename = True
                if rename:
                    os.rename(os.path.join(folder2, file), os.path.join(folder2, new_name))

    for folder1 in root_dir:
        folder1 = os.path.join(path, folder1)
        for folder2 in os.listdir(folder1):
            folder2 = os.path.join(folder1, folder2)
            for file in os.listdir(folder2):
                if file not in names_to_be:
                    os.remove(os.path.join(folder2, file))

else:
    print("Nothing happened. Bye.")