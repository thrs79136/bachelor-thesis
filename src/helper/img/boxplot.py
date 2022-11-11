import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

figure_number = 0


def create_boxplot(data_values, labels, title, suptitle, filename, dir='', ylabel=''):
    global figure_number

    figure_number += 1

    fig, ax = plt.subplots()
    ax.grid(False)
    plt.title(title, fontsize=12, y=1.15)
    plt.suptitle(suptitle, fontsize=9, y=0.9)

    ax.boxplot(data_values)
    plt.xticks(np.arange(len(labels)) + 1, labels, fontsize=8)
    plt.ylabel(ylabel)

    plt.gcf().subplots_adjust(top=0.8)

    dir = f'../data/img/plots/box_plots/{dir}'
    path = f'{dir}/{filename}'
    Path(dir).mkdir(parents=True, exist_ok=True)
    fig.savefig(path)

    plt.show()


