import os

import matplotlib.pyplot as plt
import numpy as np

figure_number = 0


def create_boxplot(data_values, labels, title, suptitle, filename, dir=''):
    global figure_number

    figure_number += 1

    fig, ax = plt.subplots()
    plt.title(title, fontsize=14, y=1.15)
    plt.suptitle(suptitle, fontsize=10, y=0.9)

    ax.boxplot(data_values)
    plt.xticks(np.arange(len(labels)) + 1, labels, fontsize=8)

    plt.gcf().subplots_adjust(top=0.8)


    fig.savefig(f'../data/img/plots/box_plots/{dir}/{filename}')

    plt.show()


