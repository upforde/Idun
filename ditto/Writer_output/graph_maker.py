from matplotlib import pyplot as plt
import numpy as np
import os

# Gathering the information for plotting

directory_list = list()
for root, dirs, files in os.walk("./", topdown=False):
    for name in dirs:
        if "Xfigures" not in name:
            directory_list.append(os.path.join(root, name))

scores = {}

for path in directory_list:
    print(path)
    path, dirs, files = next(os.walk(path))
    runs = len(files)

    dev_f1 = [[] for _ in range(20)]
    f1 = [[] for _ in range(20)]
    best_f1 = [[] for _ in range(20)]
    for i in range(runs):
        with open(path + "/run_" + str(i+1) + ".txt") as file:
            lines = file.readlines()
            for line in lines:
                if "epoch" in line:
                    place = int(line.split(" ")[1][:-1])-1
                    parts = line.split(", ")
                    # Dev_f1
                    dev_f1[place].append(float(parts[0].split("=")[1]))
                    # F1
                    f1[place].append(float(parts[1].split("=")[1]))
                    # Best F1
                    best_f1[place].append(float(parts[2].split("=")[1]))

        file.close()

    scores[path] = {"dev_f1":dev_f1, "f1":f1, "best_f1":best_f1}

    bars = []
    for i in range(len(f1)):
        f1[i].sort()
        bars.append((f1[i][-1]-f1[i][0], f1[i][0]))

    scores[path]["f1_bars"] = bars

    bars = []
    for i in range(len(dev_f1)):
        dev_f1[i].sort()
        bars.append((dev_f1[i][-1]-dev_f1[i][0], dev_f1[i][0]))
    
    scores[path]["dev_f1_bars"] = bars

    bars = []
    for i in range(len(best_f1)):
        best_f1[i].sort()
        bars.append((best_f1[i][-1]-best_f1[i][0], best_f1[i][0]))

    scores[path]["best_f1_bars"] = bars

# Defining functions for plotting
def plot(keys, tag):
    for key in list(scores.keys()):
        if key in keys:
            score = scores[key][tag]
            bars = scores[key][tag + "_bars"]

            fig = plt.figure()
            ax = fig.add_subplot()

            y = []
            for i in range(len(score)):
                score[i].sort()
                if i%2==0: ax.bar(i+1, bars[i][0], bottom=bars[i][1], color="#fabef3")
                else: ax.bar(i+1, bars[i][0], bottom=bars[i][1], color="#ad72a7")
                avg = 0
                for j in range(len(score[i])):
                    avg += score[i][j]
                y.append(avg/len(score[i]))

            name = key.replace("./", "")
            ax.set_title(name)
            ax.set_ylabel("f1")
            ax.set_xlabel("epochs")
            plt.ylim(0, 1)
            plt.xticks(np.arange(0, 21, 1.0))
            plt.yticks(np.arange(0, 1.1, 0.1))
            plt.plot(list(range(1, len(score)+1)), y, 'kd-')
            plt.savefig(f"Xfigures/{name}_{tag}.png")
            plt.close(fig)

def comparisons(name, keys, tag):
    ys = []
    legend = []
    for key in list(scores.keys()):
        if key in keys:
            string = key.replace("_", " ").replace("f1", "").replace("./", "")
            legend.append(string)
            y = []
            f1 = scores[key][tag]
            for i in range(len(f1)):
                avg = 0
                for j in range(len(f1[i])):
                    avg += f1[i][j]
                y.append(avg/len(f1[i]))
            ys.append(y)

    fig = plt.figure()
    ax = plt.subplot(111)
    plt.ylim(0, 1)
    plt.xticks(np.arange(0, 21, 1.0))
    plt.yticks(np.arange(0, 1.1, 0.1))
    ax.set_xlim(1, 20)
    for y in ys: plt.plot(list(range(1, len(scores[list(scores.keys())[0]]["f1"])+1)), y)
    plt.legend(legend, bbox_to_anchor=(1.01, 1), loc="upper left")
    plt.grid(True)
    ax.set_ylabel("f1")
    ax.set_xlabel("epochs")
    new_name = name.replace("_", " ").lower()
    plt.title(f"Comparing median {tag} scores from {new_name}")
    plt.savefig(f"Xfigures/Comparing_{name}_f1.png", bbox_inches="tight")
    plt.close(fig)

def variance():
    # TODO: Write variance comparison graph maker
    return

# PLotting

# All keys together, copy this and remove for easier setup of experiment
all_tags = [
    './GPT-2_augmented_all',
    './Prelim_augmented_with_matches', 
    './GPT-2_augmented_with_matches_only', 
    './Prelim_synth_only', 
    './GPT-2_synth_only', 
    './GPT-2_matches_ditto_prelim_non_matches', 
    './Prelim_augmented_all', 
    './Prelim_augmented_no_matches', 
    './Ditto_baseline', 
    './GPT-2_augmented_no_matches'
]

experiment_1_gpt = [
    "./Ditto_baseline", 
    "./GPT-2_augmented_all",
    "./GPT-2_augmented_with_matches_only",
    "./GPT-2_synth_only",
    "./GPT-2_augmented_no_matches"
]

experiment_1_non_ft_gpt = [
    "./Ditto_baseline", 
    "./non_ft_GPT-2_augmented_all",
    "./non_ft_GPT-2_augmented_with_matches_only",
    "./non_ft_GPT-2_synth_only",
    "./non_ft_GPT-2_augmented_no_matches"
]

experiment_1_prelim = [
    './Prelim_augmented_with_matches',
    './Prelim_synth_only',
    './Prelim_augmented_all', 
    './Prelim_augmented_no_matches', 
    './Ditto_baseline'
]

experiment_2 = [
    "./GPT-2_augmented_with_matches_only",
    './Prelim_augmented_no_matches', 
    "./GPT-2_matches_prelim_non_matches",
    "./Ditto_baseline"
]



experiment_2_plot = [
    "./non_ft_GPT-2_augmented_all",
    "./non_ft_GPT-2_augmented_with_matches_only",
    "./non_ft_GPT-2_synth_only",
    "./non_ft_GPT-2_augmented_no_matches"
]

# plot(all_tags, "f1")
# plot(all_tags, "dev_f1")
# plot(all_tags, "best_f1")
plot(experiment_2_plot, "f1")
plot(experiment_2_plot, "dev_f1")
plot(experiment_2_plot, "best_f1")

comparisons("Experiment_1_GPT-2", experiment_1_gpt, "f1")
comparisons("Experiment_1_non_ft_GPT-2", experiment_1_non_ft_gpt, "f1")
comparisons("Experiment_1_Prelim", experiment_1_prelim, "f1")
comparisons("Experiment_2", experiment_2, "f1")