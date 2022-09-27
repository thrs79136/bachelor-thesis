import sys
from collections import defaultdict
from typing import List

import numpy as np
import pandas as pd
from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QGridLayout, QSlider, QLabel, QHBoxLayout
from matplotlib import ticker, figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import mplcursors
import random


# main window
# which inherits QDialog
from qtrangeslider import QRangeSlider, QLabeledRangeSlider

from src.dimension_reduction.common import parallel_coordinates_feature_list
from src.models.song_feature import SongFeature
from src.shared import song_features
from src.shared.song_features import init_song_features


from PyQt5.QtCore import QRunnable, Qt, QThreadPool
import sys
import matplotlib
import matplotlib.figure


class Line:
    def __init__(self, line, year):
        self.line = line
        self.year = year


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal()

    def __init__(self, figure, lines_dict, year_min, year_max):
        super().__init__()

        self.figure = figure
        self.lines_dict = lines_dict
        self.mini = year_min
        self.maxi = year_max

        # self.lines_dict = defaultdict(list)

    def run(self):
        """Long-running task."""
        # TODO change figure
        self.set_lines()
        self.progress.emit()

    def set_lines(self):
        x = 42
        for i, ax in enumerate(self.figure.axes):
            ax.lines = [line.line for line in self.lines_dict[i] if self.mini <= line.year <= self.maxi]
        a = 42

    def plot(self):
        x = self.figure
        self.figure.clf()
        # self.figure = figure.Figure()

        axes = []

        df = self.data_frame.copy(True)

        # categorize decades
        df = df.drop(df[df.year < self.mini].index)
        df = df.drop(df[df.year > self.maxi].index)

        cols = parallel_coordinates_feature_list
        song_features2: List[SongFeature] = [song_features.song_features_dict[feature] for feature in
                                             parallel_coordinates_feature_list]

        feature_labels = []
        description_text = ''

        for index, feature in enumerate(song_features2):
            label = f'F{index + 1}'
            feature_labels.append(label)
            description_text += f'{label} - {feature.feature_display_name}\n'

        n = len(parallel_coordinates_feature_list)
        for i in range(n - 1):
            ax = self.figure.add_subplot(1, n - 1, i + 1)
            axes.append(ax)

        colours = (['green', 'red', 'orange', 'purple', 'blue', 'yellow'])

        colours = {df['decade'].cat.categories[i]: colours[i] for i, _ in enumerate(df['decade'].cat.categories)}

        x = [i for i, _ in enumerate(parallel_coordinates_feature_list)]

        # TODO save lines somewhere
        # lines_dict = defaultdict(list)
        # lines_dict[subplot_index] = lines

        for i, ax in enumerate(axes):
            for idx in df.index:
                year = df.loc[index, 'year']
                mpg_category = df.loc[idx, 'decade']
                ax.plot(x, df.loc[idx, parallel_coordinates_feature_list], colours[mpg_category])
                # lines_dict[i].append(Line(ax.lines[-1], year))
            ax.set_xlim([x[i], x[i + 1]])

        def set_ticks_for_axis(dim, ax, ticks):
            min_val, max_val, val_range = self.min_max_range[cols[dim]]
            step = val_range / float(ticks - 1)
            tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
            norm_min = df[cols[dim]].min()
            norm_range = np.ptp(df[cols[dim]])
            norm_step = norm_range / float(ticks - 1)
            ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
            ax.yaxis.set_ticks(ticks)
            ax.set_yticklabels(tick_labels)

        for dim, ax in enumerate(axes):
            ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
            set_ticks_for_axis(dim, ax, ticks=6)
            ax.set_xticklabels([feature_labels[dim]])

        # Move the final axis' ticks to the right-hand side
        ax = plt.twinx(axes[-1])

        dim = len(axes)
        ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
        set_ticks_for_axis(dim, ax, ticks=6)

        ax.set_xticklabels([feature_labels[-2], feature_labels[-1]])

        self.figure.subplots_adjust(wspace=0)

        # fig.text(0.1, 0.02, description_text,
        #          horizontalalignment='left', wrap=True)

        # # TODO save lines somewhere
        # lines_dict = defaultdict(list)
        # # lines_dict[subplot_index] = lines
        # for ax in axes:

        v = axes
        for i in range(len(axes[0].lines) - 1):
            axes[0].lines.pop(0)

        plt.legend(
            [plt.Line2D((0, 1), (0, 0), color=colours[cat]) for cat in df['decade'].cat.categories],
            ['1950s', '1960s', '1970s', '1980s', '1990s'],
            bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=0.)

        v = self.figure
        x = 42
        # self.canvas.draw_idle()

class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.data_frame = pd.read_csv('../../data/csv/year_features.csv')
        self.data_frame['decade'] = pd.cut(self.data_frame['decade'], [1940, 1950, 1960, 1970, 1980, 1990, 2000])

        min_max_range = {}
        for col in parallel_coordinates_feature_list:
            min_max_range[col] = [self.data_frame[col].min(), self.data_frame[col].max(), np.ptp(self.data_frame[col])]
            self.data_frame[col] = np.true_divide(self.data_frame[col] - self.data_frame[col].min(), np.ptp(self.data_frame[col]))

        self.label = QLabel('0', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter |
                                Qt.AlignmentFlag.AlignVCenter)
        self.label.setMinimumWidth(80)

        self.min_max_range = min_max_range
        self.figure = None
        self.setGeometry(400, 200, 1000, 600)

        self.mini = 1958
        self.maxi = 1991

        #self.figure = None

        self.lines_dict = defaultdict(list)
        self.create_figure()

        self.annotations = []

        for i, ax in enumerate(self.figure.axes):
            annot = ax.annotate("test", xy=(0, 0), xytext=(5, 5), textcoords="offset points")
            annot.set_visible(False)
            self.annotations.append(annot)


        self.draw()

        self.count = 0


    def create_figure(self):
        self.figure = figure.Figure()

        axes = []

        #df = self.data_frame.copy(True)
        df = self.data_frame

        # categorize decades
        # df = df.drop(df[df.year < self.mini].index)
        # df = df.drop(df[df.year > self.maxi].index)

        cols = parallel_coordinates_feature_list
        song_features2: List[SongFeature] = [song_features.song_features_dict[feature] for feature in
                                             parallel_coordinates_feature_list]

        feature_labels = []
        description_text = ''

        self.annotation_texts = []

        for index, feature in enumerate(song_features2):
            label = f'F{index + 1}'
            feature_labels.append(label)
            description_text += f'{label} - {feature.feature_display_name}\n'
            self.annotation_texts.append(f'{label} - {feature.feature_display_name}')

        n = len(parallel_coordinates_feature_list)
        for i in range(n - 1):
            ax = self.figure.add_subplot(1, n - 1, i + 1)
            axes.append(ax)

        colours = (['green', 'red', 'orange', 'purple', 'blue', 'yellow'])

        colours = {df['decade'].cat.categories[i]: colours[i] for i, _ in enumerate(df['decade'].cat.categories)}

        x = [i for i, _ in enumerate(parallel_coordinates_feature_list)]

        for i, ax in enumerate(axes):
            for idx in df.index:
                year = df.loc[idx, 'year']
                mpg_category = df.loc[idx, 'decade']
                ax.plot(x, df.loc[idx, parallel_coordinates_feature_list], colours[mpg_category])
                self.lines_dict[i].append(Line(ax.lines[-1], year))
            ax.set_xlim([x[i], x[i + 1]])

        def set_ticks_for_axis(dim, ax, ticks):
            min_val, max_val, val_range = self.min_max_range[cols[dim]]
            step = val_range / float(ticks - 1)
            tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
            norm_min = df[cols[dim]].min()
            norm_range = np.ptp(df[cols[dim]])
            norm_step = norm_range / float(ticks - 1)
            ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
            ax.yaxis.set_ticks(ticks)
            ax.set_yticklabels(tick_labels)

        for dim, ax in enumerate(axes):
            ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
            set_ticks_for_axis(dim, ax, ticks=6)
            ax.set_xticklabels([feature_labels[dim]])

        # Move the final axis' ticks to the right-hand side
        ax = plt.twinx(axes[-1])

        dim = len(axes)
        ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
        set_ticks_for_axis(dim, ax, ticks=6)

        ax.set_xticklabels([feature_labels[-2], feature_labels[-1]])

        self.figure.subplots_adjust(wspace=0)

        # fig.text(0.1, 0.02, description_text,
        #          horizontalalignment='left', wrap=True)

        # # TODO save lines somewhere
        # lines_dict = defaultdict(list)
        # # lines_dict[subplot_index] = lines
        # for ax in axes:

        plt.legend(
            [plt.Line2D((0, 1), (0, 0), color=colours[cat]) for cat in df['decade'].cat.categories],
            ['1950s', '1960s', '1970s', '1980s', '1990s'],
            bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=0.)

        v = self.figure
        x = 42
        # self.canvas.draw_idle()

    def valuechange(self):
        print(self.range_slider.value())
        value = self.range_slider.value()
        self.mini = value[0] + 1958
        self.maxi = value[1] + 1958
        # plot(self.figure, self.mini, self.maxi)
        self.start_plot_thread()
        self.canvas.draw_idle()
        # self.plot()


    def hover(self, event):

        for i, ax in enumerate(self.figure.axes):
            ext = ax.get_window_extent()
            if ext is None or event is None:
                continue


            add_annotation = False

            # 15
            if i == len(self.figure.axes)-1:
                # last ax
                if (ext.x0 + ext.x1) / 2 < event.x < ext.x1 and ext.y0 < event.y < ext.y1:
                    add_annotation = True
            elif i == 0:
                # first ax
                if ext.x0 < event.x < (ext.x0 + ext.x1)/2 and ext.y0 < event.y < ext.y1:
                    add_annotation = True
            else:
                prev_ext = self.figure.axes[i - 1].get_window_extent()
                if (prev_ext.x0 + prev_ext.x1)/2 <= event.x < (ext.x0 + ext.x1)/2 and ext.y0 < event.y < ext.y1:
                    add_annotation = True

            # elif ext.x0 < event.x < ext.x1 and ext.y0 < event.y < ext.y1:
            #     print('i: ' + str(i))
            #     print(event.x)
            #     print(ext.x0, ext.x1)
            #     annotation_text = self.annotation_texts[i]
            #     self.canvas.setToolTip(annotation_text)

            if add_annotation:
                annotation_text = self.annotation_texts[i]
                self.canvas.setToolTip(annotation_text)


        # self.canvas.setToolTip("This is a button widget !" + str(self.count))

        # self.canvas.draw_idle()

        # ext2 = self.figure.axes[0].get_window_extent()
        # ext = self.figure.get_window_extent()
        #
        # x = self.figure.mouseover
        #
        # geo = self.figure
        # print('hover event')
        # print(event.xdata, event.ydata)

        # x = self.figure
        # cont, ind = self.figure.contains(event)
        # print('figure')
        # print(cont)
        # print(ind)
        #
        # print('subplot')
        # cont, ind = self.figure.axes[0].contains(event)
        # print(cont)
        # print(ind)


    def draw(self):
        self.range_slider = QRangeSlider(Qt.Horizontal)

        #RangeSlider.setObjectName("RangeSlider")
        self.range_slider.resize(1000, 100)

        self.range_slider.setMinimum(0)
        self.range_slider.setMaximum(1991-1958)

        self.range_slider.setMaximumSize(QtCore.QSize(16777215, 30))
        self.range_slider.sliderReleased.connect(self.valuechange)

        print(type(self.figure))

        # a figure instance to plot on
        # self.figure, axes = plt.subplots(1, len(parallel_coordinates_feature_list)-1, sharey=False)

        # self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__


        self.canvas = FigureCanvas(self.figure)


        # self.annot = self.figure.annotate("", xy=(0, 0), xytext=(5, 5), textcoords="offset points")
        # self.annot.set_visible(False)

        self.canvas.mpl_connect('motion_notify_event', self.hover)
        # self.canvas.mouseMoveEvent(self.hover)

        self.valuechange()
        # self.canvas.draw_idle()


        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        # self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to 'plot' method
        # self.button = QPushButton('Plot')

        # adding action to the button
        # self.button.clicked.connect(self.plot)

        # creating a Vertical Box layout
        self.layout = QVBoxLayout()

        # adding tool bar to the layout
        # layout.addWidget(self.toolbar)

        # adding canvas to the layout
        # hbox = QHBoxLayout()


        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.range_slider)

        # adding push button to the layout
        # layout.addWidget(self.button)

        # setting layout to the main window
        self.setLayout(self.layout)

        # self.start_plot_thread()

    def start_plot_thread(self):

        for i, ax in enumerate(self.figure.axes):
            ax.lines = [line.line for line in self.lines_dict[i] if self.mini <= line.year <= self.maxi]

    def update_canvas(self):
        self.canvas.draw_idle()


# driver code
if __name__ == '__main__':
    # creating apyqt5 application
    init_song_features()
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())
