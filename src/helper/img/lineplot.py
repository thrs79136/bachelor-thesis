import matplotlib.pyplot as plt
import numpy as np

figure_number = 0

def lineplot(x, y, xlabel, ylabel, filename: str, title='', suptitle='', dir='', dot_coordinates=None, dot_legend=''):
    global figure_number

    if dir != '':
        dir += '/'

    plt.figure(figure_number)
    fig, ax = plt.subplots()
    plt.plot(x, y)

    # dots
    if dot_coordinates is not None:
        dot_x_values = [tupl[0] for tupl in dot_coordinates]
        dot_y_values = [tupl[1] for tupl in dot_coordinates]

        plt.plot(dot_x_values, dot_y_values, 'D', color='black', label=dot_legend)

    plt.legend(loc='upper right')

    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # plt.ylim([0, 1.])
    plt.show()
    fig.savefig('../data/img/plots/line_plots/' + dir + filename)

    figure_number += 1


def lineplot_multiple_lines(x, y_lists, legend, xlabel, ylabel, filename: str, title, suptitle='', dir=''):
    global figure_number

    if dir != '':
        dir += '/'

    fig, ax = plt.subplots()

    for i, y_values in enumerate(y_lists):
        plt.plot(x, y_values, label=legend[i])
    plt.legend(loc='upper right')

    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    fig.savefig('../data/img/plots/line_plots/' + dir + filename)

    figure_number += 1


def stacked_area_plot(x, y_lists, legend, xlabel, ylabel, filename, title, suptitle='', dir=''):

    if dir != '':
        dir += '/'

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ylist_len = len(list(y_lists)[0])
    area_base_line = [0] * ylist_len

    for index, y_list in enumerate(y_lists):
        area_upper_line = [sum(elts) for elts in zip(area_base_line, y_list)]
        ax1.fill_between(x, area_base_line, area_upper_line, label=legend[index])
        area_base_line = area_upper_line

    plt.legend(loc='upper right')

    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.show()
    fig.savefig('../data/img/plots/line_plots/' + dir + filename)
