from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd

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

small_datasets = [
    "Dirty_iTunes-Amazon",
    "Structured_Beer",
    "Structured_Fodors-Zagats",
    "Structured_iTunes-Amazon"
]


def make_plot(plot_type, title, decimated=True):
    # Setting up the arrays for the columns
    labels = []
    for dataset in er_magellan.keys():
        if decimated: 
            if dataset not in small_datasets: labels.append(dataset)
        else: labels.append(dataset)
    baseline = [0.01 for _ in range(len(labels))]               # 100% Real data baseline measurements
    baseline_decimated = [0.01 for _ in range(len(labels))]     # 10% Real data baseline measurements
    augmentation = [0.01 for _ in range(len(labels))]           # Augmentation method
    gpt2_ft = [0.01 for _ in range(len(labels))]                # GPT-2 fine-tuned method
    gpt2_nft = [0.01 for _ in range(len(labels))]               # GPT-2 non-fine-tuned method
    ctgan = [0.01 for _ in range(len(labels))]                  # CTGAN method
    
    if decimated: plot_type = "decimate_" + plot_type
    save_score_path = r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Results" + os.sep + plot_type + ".csv"
    data_table = pd.read_csv(save_score_path, encoding="utf-8", index_col="Generator")
    for i in range(len(labels)):
        baseline[i] = data_table.at["Baseline", labels[i]]
        ctgan[i] = data_table.at["CTGAN", labels[i]]
        gpt2_ft[i] = data_table.at["GPT-2_ft", labels[i]]
        gpt2_nft[i] = data_table.at["GPT-2_nft", labels[i]]
        augmentation[i] = data_table.at["Augmentation", labels[i]]
        if decimated:
            baseline_decimated[i] = data_table.at["d_Baseline", labels[i]]

    # initiating the plots
    fig, ax = plt.subplots(figsize=(17, 6))
    # Make graph span the entire image
    fig.tight_layout()

    # Labels and titles
    ax.set_ylabel('f1 scores', fontsize=12)
    
    # Limiting the y-axis
    ax.set_ylim([0, 1.1])

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
        ax.legend(loc='upper center', fontsize='small', ncol=6)
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
        ax.bar_label(baseline_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(augmentation_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(gpt2_nft_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(gpt2_ft_rects, padding=1, fmt="%.2f", fontsize=6)
        ax.bar_label(ctgan_rects, padding=1, fmt="%.2f", fontsize=6)

        ax.legend(loc='upper center', fontsize='small', ncol=5)

    # Saving the plot to the Xfigures forled (Called Xfigures to appear at the end of the work tree)
    name = f"plots/{plot_type}"
    
    plt.savefig(r"C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN" + os.sep + name + ".pdf", bbox_inches="tight")


# "Textual_Abt-Buy": {"CTGAN":F1, "GPT2":F1}
# C:\Users\aleks\Desktop\Master Thesis\Idun\CTGAN\Results


plot_types = [
    r"matches_non-matches",
    r"real_data_matches",
    r"real_data_non-matches",
    r"real_data_matches_non-matches"
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