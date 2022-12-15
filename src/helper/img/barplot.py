from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

def addlabels(x,y):
    for i in range(len(x)):
        text = f'{"{0:.3f}".format(y[i])}'
        plt.text(i, y[i] + 0.015, text, ha = 'center')


# def addlabels(x,y):
#     for i in range(len(x)):
#         plt.text(i, y[i]//2, y[i], ha = 'center')


def create_barplot(bar_values, labels, ylabel, filename, title, subtitle='', ylim=None, horizontal_line=None, directory='', figsize=(6.4,4.8)):

    fig = plt.figure(figsize=figsize)
    # fig = plt.figure(figsize=())
    fig.subplots_adjust(bottom=0.32, left=0.15)

    y_pos = np.arange(len(labels))

    plt.bar(y_pos, bar_values, align='center', alpha=0.7, width=0.75)

    if horizontal_line:
        plt.axhline(y=horizontal_line, linewidth=1, color='red')

    if ylim:
        plt.ylim(0, ylim)

    addlabels(labels, bar_values)

    plt.xticks(y_pos, labels, rotation=90)
    plt.ylabel(ylabel)
    plt.title(title, fontsize=14, y=1.05)
    plt.suptitle(subtitle, fontsize=10, y=0.92)

    if directory != '':
        directory = f'{directory}/'
    path = f'../data/img/plots/bar_plots/{directory}'
    Path(path).mkdir(parents=True, exist_ok=True)
    fig.savefig(path + filename)

    plt.show()

    # # creating the dataset
    # fig = plt.figure(figsize=(9, 5))
    #
    # bar_width = 0.1
    #
    # # creating the bar plot
    # # plt.bar(labels, bar_values, color='maroon',
    # #         width=0.4)
    #
    # for i in range(len(bar_values)):
    #     plt.bar(i*bar_width, [bar_values[i]], color='r', width=bar_width, label=labels[i])
    #
    # plt.ylabel("Genauigkeit")
    # plt.title(title)
    #
    # plt.legend()
    # fig.savefig('../data/img/plots/bar_plots/' + filename)
    #
    # plt.show()


def create_stacked_barplot(bar_values, labels, legend, title, suptitle, filename, directory=''):

    fig = plt.figure()
    ax = plt.subplot(111)

    # bar_values.reverse()
    for i, values in enumerate(bar_values):
        bar_values[i] = np.array(values)


    color_palette = sns.color_palette("icefire", n_colors=len(legend))

    # plot bars in stack manner
    for i, values in enumerate(bar_values):
        j = len(bar_values) - i -1
        low = j+1

        test1 = len(bar_values)
        test2 = bar_values[low:]
        test3 = sum(test2)
        parameter = sum(bar_values[low:]) if j != len(bar_values)-1 else None

        plt.bar(labels, bar_values[j], bottom=sum(bar_values[low:]) if j != len(bar_values)-1 else None, label=legend[j], color=color_palette[j])

    plt.ylabel("Anteil der Lieder")

    box = ax.get_position()
    if len(legend[0]) >= 10 and len(legend) <= 2:
        # bottom
        ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
        # Put a legend to the right of the current axis
        ax.legend(legend, loc='lower left', bbox_to_anchor=(0, -0.3))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='lower left', bbox_to_anchor=(0, -0.3))
    else:
        # right
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(legend, loc='center left', bbox_to_anchor=(1, 0.65))
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.65))

    plt.suptitle(suptitle)
    plt.title(title)

    plt.show()

    if directory != '':
        directory = f'{directory}/'
    path = f'../data/img/plots/bar_plots/{directory}'
    Path(path).mkdir(parents=True, exist_ok=True)

    fig.savefig(path + filename)


def create_grouped_barplot(bar_values, labels, legend, filename, title, subtitle='', ylabel='', directory=''):

    fig = plt.figure(figsize=(8, 5))
    x = [i for i in range(12)]
    bar_values = [x] * 5

    y1 = [34, 56, 12, 89, 12, 10, 10]*2
    # create data
    # x = np.arange(len(bar_values))
    x = np.arange(len(y1))


    width = 0.05

    # plot data in grouped manner of bar type
    for i in range(len(y1)):
        plt.bar(x - width + i * width, y1, width)

    plt.title(title, fontsize=14, y=1.05)
    plt.suptitle(subtitle, fontsize=10, y=0.92)

    # plt.xticks(x, labels)
    # plt.xlabel("Teams")
    plt.ylabel(ylabel)
    # plt.legend(legend)

    path = f'../data/img/plots/bar_plots/{directory}'
    Path(path).mkdir(parents=True, exist_ok=True)

    fig.savefig(path + filename)
    plt.show()
