from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

figure_number = 0


def lineplot(x, y, xlabel, ylabel, filename: str, title='', suptitle='', directory='', dot_coordinates=None, dot_legend=''):
    global figure_number

    plt.style.use('seaborn-whitegrid')

    path = f'../data/img/plots/{directory}'
    Path(path).mkdir(parents=True, exist_ok=True)


    plt.figure(figure_number)
    fig, ax = plt.subplots()
    plt.plot(x, y)

    try:
        color_palette = sns.color_palette("icefire", n_colors=len(dot_legend))
    except Exception:
        x = 42
    #color_palette = ['red', 'blue'] * 5

    # dots
    if dot_coordinates is not None:
        for i, dot_coordinate_list in enumerate(dot_coordinates):
            dot_x_values = [tupl[0] for tupl in dot_coordinate_list]
            dot_y_values = [tupl[1] for tupl in dot_coordinate_list]

            plt.plot(dot_x_values, dot_y_values, 'D', color=color_palette[i], label=dot_legend[i])
        plt.legend(loc='upper right')

    plt.title(title, fontsize=20, y=1.15, wrap=True)
    plt.suptitle(suptitle, fontsize=16, y=0.82)
    plt.xlabel(xlabel, fontsize=18)
    plt.ylabel(ylabel, fontsize=18)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    plt.subplots_adjust(top=0.75, left=0.17)

    # plt.ylim([0, 1.])
    plt.show()
    fig.savefig(path + filename)

    figure_number += 1


def lineplot_multiple_lines(x, y_lists, legend, xlabel, ylabel, filename: str, title, suptitle='', directory='', dot_coordinates=None, dot_legend=None, dot_labels=None, figsize=(6.4,4.8), ylim=None):
    global figure_number

    if directory != '':
        directory += '/'

    fig, ax = plt.subplots(figsize=figsize)

    for i, y_values in enumerate(y_lists):
        plt.plot(x, y_values, label=legend[i])
    plt.legend(loc='upper right')

    if dot_coordinates is not None:
        for i, dot_coordinate_list in enumerate(dot_coordinates):
            dot_x_values = [tupl[0] for tupl in dot_coordinate_list]
            dot_y_values = [tupl[1] for tupl in dot_coordinate_list]

            plt.plot(dot_x_values, dot_y_values, 'D', color='red', label=dot_legend[i])
            if dot_labels:
                for j, dot_coordinate in enumerate(dot_coordinate_list):
                    if i < len(dot_labels) and j < len(dot_labels[i]):
                        ax.annotate(dot_labels[i][j], (dot_coordinate[0], dot_coordinate[1] + 1))

        plt.legend(loc='upper right')

    if ylim is not None:
        plt.ylim(ylim)
    plt.subplots_adjust(bottom=0.15)
    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

    path = f'../data/img/plots/line_plots/{directory}'
    Path(path).mkdir(parents=True, exist_ok=True)

    fig.savefig(path + filename)

    figure_number += 1


def stacked_area_plot(x, y_lists, legend, xlabel, ylabel, filename, title, suptitle='', dir=''):

    if dir != '':
        dir += '/'

    fig = plt.figure(figsize=(7, 4.08))
    ax = fig.add_subplot(111)

    ylist_len = len(list(y_lists)[0])
    area_base_line = [0] * ylist_len

    colors = sns.color_palette("Spectral", n_colors=len(legend))
    # colors = sns.color_palette('magma', n_colors=len(legend))
    coeff = 1
    colors[2] = (coeff*0.9971549404075356**2, coeff*0.9118031526336025**2, coeff*0.6010765090349866**2)


    for index, y_list in enumerate(y_lists):
        area_upper_line = [sum(elts) for elts in zip(area_base_line, y_list)]
        ax.fill_between(x, area_base_line, area_upper_line, label=legend[index], color=colors[index])
        area_base_line = area_upper_line

    box = ax.get_position()
    # right
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(legend, loc='center left', bbox_to_anchor=(1, 0.65))
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.65))

    fontsize = 11

    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)

    plt.subplots_adjust(bottom=0.2, right=0.8)

    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)

    plt.show()
    fig.savefig('../data/img/plots/line_plots/' + dir + filename)
