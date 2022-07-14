import matplotlib.pyplot as plt

figure_number = 0

def lineplot(x, y, xlabel, ylabel, filename: str, title, suptitle, dir=''):
    global figure_number

    if dir != '':
        dir += '/'

    fig, ax = plt.subplots()
    plt.plot(x, y)
    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    fig.savefig('../data/img/plots/line_plots/' + dir + filename)

    figure_number += 1


def lineplot_multiple_lines(x, y, xlabel, ylabel, filename: str, title, suptitle, dir=''):
    global figure_number

    if dir != '':
        dir += '/'

    fig, ax = plt.subplots()
    plt.plot(x, y)
    plt.title(title, fontsize=13, y=1.05)
    plt.suptitle(suptitle, fontsize=10, y=0.92)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    fig.savefig('../data/img/plots/line_plots/' + dir + filename)

    figure_number += 1