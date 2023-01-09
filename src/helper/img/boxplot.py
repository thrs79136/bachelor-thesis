import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

figure_number = 0


def create_boxplot(data_values, labels, title, suptitle, filename, dir='', ylabel='', figsize=(6.4,48)):
    global figure_number

    figure_number += 1

    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(bottom=0.25, left=0.2)

    ax.grid(False)
    plt.title(title, fontsize=12, y=1.15)
    plt.suptitle(suptitle, fontsize=9, y=0.88)

    ax.boxplot(data_values)

    rotation = 90
    if len(list(labels)[0]) > 10:
        rotation = 15
    plt.xticks(np.arange(len(labels)) + 1, labels, fontsize=9, rotation=rotation)
    plt.ylabel(ylabel, fontsize=11)

    plt.gcf().subplots_adjust(top=0.8)

    dir = f'../data/img/plots/box_plots/{dir}'
    path = f'{dir}/{filename}'
    Path(dir).mkdir(parents=True, exist_ok=True)
    fig.savefig(path)

    plt.show()

