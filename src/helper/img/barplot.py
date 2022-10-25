import numpy as np
from matplotlib import pyplot as plt


def addlabels(x,y):
    for i in range(len(x)):
        text = f'{"{0:.3f}".format(y[i])}'
        plt.text(i, y[i] + 0.015, text, ha = 'center')


def create_barplot(bar_values, labels, filename, title, subtitle=''):

    fig = plt.figure(figsize=(5, 5))

    y_pos = np.arange(len(labels))

    plt.bar(y_pos, bar_values, align='center', alpha=0.7, width=0.75)
    plt.ylim(0, 1.05)

    addlabels(labels, bar_values)

    plt.xticks(y_pos, labels)
    plt.ylabel('Genauigkeit')
    plt.title(title, fontsize=14, y=1.05)
    plt.suptitle(subtitle, fontsize=10, y=0.92)
    fig.savefig('../data/img/plots/bar_plots/' + filename)

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
