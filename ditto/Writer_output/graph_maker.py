from matplotlib import pyplot as plt
import numpy as np
import os

def get_best_average_f1(dataset):
    # Setting up the 20 epochs that ditto does
    f1 = 0
    # Adding up the f1 scores throughout all runs of ditto for each epoch
    for run in os.listdir(dataset):
        with open(dataset + "/" + run) as txt:
            for line in txt.readlines():
                # Split up each run
                parts = line.split()
                # Read only the lines that start with 'epoch'
                if parts[0] == "epoch":
                    # Add this epochs f1 score to the corresponding epoch sum in the array
                    epoch = int(parts[1].replace(":", ""))-1
                    if epoch == 19: f1 += float(parts[3].replace("f1=", "").replace(",", ""))

    f1 = f1/len(os.listdir(dataset))
    
    return f1

def make_plot(plot_type, title, decimated=True):
    # Setting up the arrays for the columns
    labels = [dataset for dataset in er_magellan.keys()]        # Labels of the datasets
    baseline = [0.05 for _ in range(len(labels))]               # 100% Real data baseline measurements
    baseline_decimated = [0.05 for _ in range(len(labels))]     # 10% Real data baseline measurements
    augmentation = [0.05 for _ in range(len(labels))]           # Augmentation method
    gpt2_ft = [0.05 for _ in range(len(labels))]                # GPT-2 fine-tuned method
    gpt2_nft = [0.05 for _ in range(len(labels))]               # GPT-2 non-fine-tuned method
    ctgan = [0.05 for _ in range(len(labels))]                  # CTGAN method
    
    # For each dataset
    for i in range(len(labels)):
        # For each permutation of datasets
        for key in er_magellan[labels[i]]:
            if "Baseline" in key and "decimated" not in key: baseline[i] = er_magellan[labels[i]][key]
            if "Baseline decimated" in key: baseline_decimated[i] = er_magellan[labels[i]][key]
            # Select the correct permutation to plot
            if plot_type in key:
                # Decimated interaction
                if decimated:
                    # Select only the decimated permutation
                    if "decimated" in key:
                        # Insert the values of the columns into the columns
                        if "Augmentation" in key: augmentation[i] = er_magellan[labels[i]][key]
                        if "GPT-2" in key and "nft" in key: gpt2_nft[i] = er_magellan[labels[i]][key]
                        if "GPT-2" in key and "nft" not in key: gpt2_ft[i] = er_magellan[labels[i]][key]
                        if "CTGAN" in key: ctgan[i] = er_magellan[labels[i]][key]
                else:
                    # Select only the non-decimated permutation
                    if "decimated" not in key:
                        # Insert the values of the columns into the columns
                        if "Augmentation" in key: augmentation[i] = er_magellan[labels[i]][key]
                        if "GPT-2" in key and "nft" in key: gpt2_nft[i] = er_magellan[labels[i]][key]
                        if "GPT-2" in key and "nft" not in key: gpt2_ft[i] = er_magellan[labels[i]][key]
                        if "CTGAN" in key: ctgan[i] = er_magellan[labels[i]][key]

    # initiating the plots
    fig, ax = plt.subplots(figsize=(17, 6))
    # Make graph span the entire image
    fig.tight_layout()

    # Labels and titles
    ax.set_ylabel('f1 scores', fontsize=12)
    ax.set_title(title)
    
    # Limiting the y-axis
    ax.set_ylim([0, 1])

    # Slight formatting of the labels to make the graphs sexy
    for i in range(len(labels)): labels[i] = labels[i].replace("_", " ")
    # Dataset labels
    x = np.arange(len(labels))
    fig.autofmt_xdate()         # Making the labels slanted for readability
    ax.set_xticks(x, labels, fontsize=7)

    # Populating the plots
    if decimated:
        # Drawing the columns
        width = 0.14    # Width has to be slightly smaller than (1/num_columns) to make space between datasets)

        # Actual columns for each dataset
        baseline_decimated_rects =  ax.bar(x- 2 * width - width/2, baseline_decimated, width, label="10% Real data")
        augmentation_rects =        ax.bar(x - width - width/2, augmentation, width, label='Augmentation')
        gpt2_nft_rects =            ax.bar(x - width/2, gpt2_nft, width, label='GPT-2 non-fine-tuned')
        gpt2_ft_rects =             ax.bar(x + width/2, gpt2_ft, width, label='GPT-2 fine-tuned')
        ctgan_rects =               ax.bar(x + width + width/2, ctgan, width, label='CTGAN')
        baseline_rects =            ax.bar(x + 2 * width + width/2, baseline, width, label='Real data')
        
        # The values of each of the columns shown above the columns for readability
        ax.bar_label(baseline_decimated_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(augmentation_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(gpt2_nft_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(gpt2_ft_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(ctgan_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(baseline_rects, padding=1, fmt="%.2f", fontsize=6)

        # Legend
        ax.legend(bbox_to_anchor =(0.5,-0.28), loc='lower center', fontsize='small', ncol=6)
    else:
        # Drawing the columns
        width = 0.15    # Width has to be slightly smaller than (1/num_columns) to make space between datasets)

        # Actual columns for each dataset
        baseline_rects =        ax.bar(x - 2*width, baseline, width, label='Real data')
        augmentation_rects =    ax.bar(x - width, augmentation, width, label='Augmentation')
        gpt2_nft_rects =        ax.bar(x, gpt2_nft, width, label='GPT-2 non-fine-tuned')
        gpt2_ft_rects =         ax.bar(x + width, gpt2_ft, width, label='GPT-2 fine-tuned')
        ctgan_rects =           ax.bar(x + 2*width, ctgan, width, label='CTGAN')

        # The values of each of the columns shown above the columns for readability
        ax.legend(bbox_to_anchor =(0.5,-0.28), loc='lower center', fontsize='small', ncol=5)
        ax.bar_label(baseline_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(augmentation_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(gpt2_nft_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(gpt2_ft_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(ctgan_rects, padding=1, fmt="%.2f", fontsize=6)

    # Saving the plot to the Xfigures forled (Called Xfigures to appear at the end of the work tree)
    name = f"Xfigures/{plot_type}"
    if decimated: name += "_decimated"
    plt.savefig(name + ".png", bbox_inches="tight")


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
                if "baseline" in name: 
                    if "_decimated" in name:
                        er_magellan[dataset]["Baseline decimated"] = get_best_average_f1(directory)
                    else: er_magellan[dataset]["Baseline"] = get_best_average_f1(directory)
                else: er_magellan[dataset][name] = get_best_average_f1(directory)

for dataset in er_magellan.keys():
    print(dataset)
    for directory in er_magellan[dataset]:
        print(f"\t{directory}: {er_magellan[dataset][directory]}")
            

# Setting up the dataset permutations to plot graphs for those permutations
plot_types = [
    "gen_only",
    "real_plus_matches",
    "real_plus_non_matches",
    "real_plus_all"
]

titles = [
    "Generated data only",
    "Real data with generated matches",
    "Real data with generated non-matches",
    "Real data with all generated data"
]

for i in range(len(plot_types)):
    # Plotting the real data graph
    make_plot(plot_types[i], titles[i], True)
    # Plotting the decimated data graph
    make_plot(plot_types[i], titles[i], False)