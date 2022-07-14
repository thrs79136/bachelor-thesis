import os

import matplotlib.pyplot as plt
import numpy as np

figure_number = 0


def create_boxplot(data_values, labels, title, suptitle, filename):
    global figure_number

    figure_number += 1

    fig, ax = plt.subplots()
    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)

    ax.boxplot(data_values)
    plt.xticks(np.arange(len(labels)) + 1, labels, fontsize=8)

    fig.savefig('../data/img/plots/box_plots/' + filename)

    plt.show()


