from typing import List

from matplotlib import pyplot as plt

figure_number = 0

def create_scatter_plot(x: List, y: List, filename: str, title: str = '', suptitle: str = '', xlabel: str = '', ylabel: str = '', directory: str = ''):
    global figure_number

    plt.figure(figure_number)
    figure_number += 1
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, '.', color='black')
    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    dir = '../data/img/plots/scatter_plots/'
    if directory != '':
        dir += f'{directory}/'
    plt.savefig(dir + filename)
    plt.show()
    plt.close()