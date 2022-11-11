from pathlib import Path
from typing import List

from matplotlib import pyplot as plt

figure_number = 0

def create_scatter_plot(x: List, y: List, filename: str, title: str = '', suptitle: str = '', xlabel: str = '', ylabel: str = '', directory: str = ''):
    global figure_number

    plt.figure(figure_number)

    figure_number += 1
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, '.', color='black')
    plt.title(title, fontsize=20, y=1.15, wrap=True)
    plt.suptitle(suptitle, fontsize=16, y=0.82)
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=18)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.subplots_adjust(top=0.75, left=0.17)


    dir = '../data/img/plots/scatter_plots/'
    if directory != '':
        dir += f'{directory}/'

    Path(dir).mkdir(parents=True, exist_ok=True)

    plt.savefig(dir + filename)
    plt.show()
    plt.close()
