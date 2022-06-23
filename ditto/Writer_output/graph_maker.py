from matplotlib import pyplot as plt
import numpy as np
import os

def get_best_average_f1(dataset):
    epochs = [0.0 for _ in range(20)]
    for run in os.listdir(dataset):
        with open(dataset + "/" + run) as txt:
            for line in txt.readlines():
                parts = line.split()
                if parts[0] == "epoch":
                    epoch = int(parts[1].replace(":", ""))-1
                    epochs[epoch] += float(parts[3].replace("f1=", "").replace(",", ""))
    for i in range(len(epochs)):
        epochs[i] = epochs[i]/len(os.listdir(dataset))
    return max(epochs)

er_magellan = {
    "Dirty_DBLP-ACM": {},
    "Dirty_DBLP-GoogleScholar": {},
    "Dirty_iTunes-Amazon": {},
    "Dirty_Walmart-Amazon": {},
    "Structured_Amazon-Google": {},
    "Structured_Beer": {},
    "Structured_DBLP-ACM": {},
    "Structured_DBLP-GoogleScholar": {},
    "Structured_Fodors-Zagats": {},
    "Structured_iTunes-Amazon": {},
    "Structured_Walmart-Amazon": {},
    "Textual_Abt-Buy": {}
}

# Gathering the information for plotting
directory_list = list()
for root, dirs, files in os.walk("./", topdown=False):
    for name in dirs:
        if "Xfigures" not in name:
            directory_list.append(os.path.join(root, name))

for directory in directory_list:
    for dataset in er_magellan.keys():
        if dataset in directory:
            avg = get_best_average_f1(directory)
            if avg <= 1:
                name = directory.replace("./", "").replace(dataset, "").replace("__", "_")
                if "baseline" in name: er_magellan[dataset]["Baseline"] = get_best_average_f1(directory)
                else: er_magellan[dataset][name] = get_best_average_f1(directory)

for dataset in er_magellan.keys():
    print(dataset)
    for directory in er_magellan[dataset]:
        print(f"\t{directory}: {er_magellan[dataset][directory]}")
            

def make_plot(plot_type, decimated=True):
    labels = []
    baseline = []
    augmentation = []
    gpt2_ft = []
    gpt2_nft = []
    ctgan = []
    
    for dataset in er_magellan.keys():
        labels.append(dataset.replace("_", " "))
        
        for key in er_magellan[dataset].keys():
            if key == "Baseline": baseline.append(er_magellan[dataset][key])
            if plot_type in key:
                if "Augmentation" in key: augmentation.append(er_magellan[dataset][key])
                if "GPT-2" in key and "nft" in key: gpt2_nft.append(er_magellan[dataset][key])
                if "GPT-2" in key and "nft" not in key: gpt2_ft.append(er_magellan[dataset][key])
                if "CTGAN" in key: ctgan.append(er_magellan[dataset][key])
                

    return



plot_types = [
    "gen_only",
    "real_plus_matches",
    "real_plus_non_matches",
    "real_plus_all"
]

make_plot(plot_types[0])


# scores = {}

# for path in directory_list:
#     print(path)
#     path, dirs, files = next(os.walk(path))
#     runs = len(files)

#     dev_f1 = [[] for _ in range(20)]
#     f1 = [[] for _ in range(20)]
#     best_f1 = [[] for _ in range(20)]
#     for i in range(runs):
#         with open(path + "/run_" + str(i+1) + ".txt") as file:
#             lines = file.readlines()
#             for line in lines:
#                 if "epoch" in line:
#                     place = int(line.split(" ")[1][:-1])-1
#                     parts = line.split(", ")
#                     # Dev_f1
#                     dev_f1[place].append(float(parts[0].split("=")[1]))
#                     # F1
#                     f1[place].append(float(parts[1].split("=")[1]))
#                     # Best F1
#                     best_f1[place].append(float(parts[2].split("=")[1]))

#         file.close()

#     scores[path] = {"dev_f1":dev_f1, "f1":f1, "best_f1":best_f1}

#     bars = []
#     for i in range(len(f1)):
#         f1[i].sort()
#         bars.append((f1[i][-1]-f1[i][0], f1[i][0]))

#     scores[path]["f1_bars"] = bars

#     bars = []
#     for i in range(len(dev_f1)):
#         dev_f1[i].sort()
#         bars.append((dev_f1[i][-1]-dev_f1[i][0], dev_f1[i][0]))
    
#     scores[path]["dev_f1_bars"] = bars

#     bars = []
#     for i in range(len(best_f1)):
#         best_f1[i].sort()
#         bars.append((best_f1[i][-1]-best_f1[i][0], best_f1[i][0]))

#     scores[path]["best_f1_bars"] = bars

# # Defining functions for plotting
# def plot(keys, tag):
#     for key in list(scores.keys()):
#         if key in keys:
#             score = scores[key][tag]
#             bars = scores[key][tag + "_bars"]

#             fig = plt.figure()
#             ax = fig.add_subplot()

#             y = []
#             for i in range(len(score)):
#                 score[i].sort()
#                 if i%2==0: ax.bar(i+1, bars[i][0], bottom=bars[i][1], color="#fabef3")
#                 else: ax.bar(i+1, bars[i][0], bottom=bars[i][1], color="#ad72a7")
#                 avg = 0
#                 for j in range(len(score[i])):
#                     avg += score[i][j]
#                 y.append(avg/len(score[i]))

#             name = key.replace("./", "")
#             ax.set_title(name)
#             ax.set_ylabel("f1")
#             ax.set_xlabel("epochs")
#             plt.ylim(0, 1)
#             plt.xticks(np.arange(0, 21, 1.0))
#             plt.yticks(np.arange(0, 1.1, 0.1))
#             plt.plot(list(range(1, len(score)+1)), y, 'kd-')
#             plt.savefig(f"Xfigures/{name}_{tag}.png")
#             plt.close(fig)

# def comparisons(name, keys, tag):
#     ys = []
#     legend = []
#     for key in list(scores.keys()):
#         if key in keys:
#             string = key.replace("_", " ").replace("f1", "").replace("./", "")
#             legend.append(string)
#             y = []
#             f1 = scores[key][tag]
#             for i in range(len(f1)):
#                 avg = 0
#                 for j in range(len(f1[i])):
#                     avg += f1[i][j]
#                 y.append(avg/len(f1[i]))
#             ys.append(y)

#     fig = plt.figure()
#     ax = plt.subplot(111)
#     plt.ylim(0, 1)
#     plt.xticks(np.arange(0, 21, 1.0))
#     plt.yticks(np.arange(0, 1.1, 0.1))
#     ax.set_xlim(1, 20)
#     for y in ys: plt.plot(list(range(1, len(scores[list(scores.keys())[0]]["f1"])+1)), y)
#     plt.legend(legend, bbox_to_anchor=(1.01, 1), loc="upper left")
#     plt.grid(True)
#     ax.set_ylabel("f1")
#     ax.set_xlabel("epochs")
#     new_name = name.replace("_", " ").lower()
#     plt.title(f"Comparing median {tag} scores from {new_name}")
#     plt.savefig(f"Xfigures/Comparing_{name}_f1.png", bbox_inches="tight")
#     plt.close(fig)
