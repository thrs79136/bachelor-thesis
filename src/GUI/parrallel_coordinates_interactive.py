import sys
from collections import defaultdict
from threading import Thread
from typing import List

import numpy as np
import pandas as pd
from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QGridLayout, QSlider, QLabel, QHBoxLayout, \
    QComboBox, QSizePolicy, QWidget, QStackedWidget, QMainWindow
import seaborn as sns
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

from src.dimension_reduction.common import feature_lists
from src.models.song_feature import SongFeature
from src.shared import shared
from src.shared.shared import init_song_features


from PyQt5.QtCore import QRunnable, Qt, QThreadPool
import sys
import matplotlib
import matplotlib.figure


genre_to_color = {
    'rock': 'blue',
    'pop-rock': 'green',
    'pop': 'yellow',
    'soul': 'red',
    'funk-soul': 'orange'
}

# TODO put into helper
def human_format(num_list):
    results = []
    for num in num_list:
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        num = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])
        results.append(num)
    return results

class Line:
    def __init__(self, line, year):
        self.line = line
        self.year = year


median_path = '../data/csv/year_features.csv'
songs_path = '../data/csv/song_features.csv'

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super(LoadingWidget, self).__init__(parent)

        self.label = QLabel()

        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)

        self.movie = QMovie("./GUI/spinner2.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)

        self.setLayout(self.layout)


class ParallelCoordinatesWidget(QWidget):
    def __init__(self, parent=None):
        super(ParallelCoordinatesWidget, self).__init__(parent)

        self.figure_p = matplotlib.figure.Figure()
        self.figure_p.set_facecolor('#f0f0f0')

        self.mini = 1958
        self.maxi = 1991

        self.label = QLabel(str(self.mini), self)
        self.label.setVisible(False)
        self.label2 = QLabel(str(self.maxi), self)
        self.label2.setVisible(False)
        
        # self.feature_list = ['acousticness', 'v_to_i', 'root_distances', 'bass_distances', 'major_chords', 'tonic_chords', 'seventh_chords', 'circle_of_fifths', 'circle_of_fifths_max', 'different_notes', 'different_chords', 'different_progressions', 'minor_chords', 'duration_ms', 'different_sections', 'chorus_repetitions', 'danceability', 'energy', 'neither_chords', 'non_triad_chords']
        self.feature_list = feature_lists['year']

        self.df_dict = {
            "Alle Lieder": None,
            "Lieder mit Chartposition 1": None,
            "Feature-Median pro Jahr": None
        }

        self.draw()


    def init(self):
        self.init_figures()

    def init_figures(self):
        self.figure_num = 0

        self.data_frame = shared.mcgill_df.copy(True)
        self.data_frame['decade'] = pd.cut(self.data_frame['decade'], [1940, 1950, 1960, 1970, 1980, 1990, 2000])

        median_df = shared.median_df.copy(True)

        self.min_max_range = {}
        for col in self.feature_list:
            self.min_max_range[col] = [self.data_frame[col].min(), self.data_frame[col].max(), np.ptp(self.data_frame[col])]
            self.data_frame[col] = np.true_divide(self.data_frame[col] - self.data_frame[col].min(), np.ptp(self.data_frame[col]))
            median_df[col] = np.true_divide(median_df[col] - median_df[col].min(), np.ptp(median_df[col]))

        self.data_frame_most_successful = self.data_frame.loc[self.data_frame['chart_pos'] == 1]

        self.selected_dataframe = self.data_frame_most_successful
        self.selected_dataframe_id = list(self.df_dict.keys())[0]

        self.df_dict["Alle Lieder"] = self.data_frame
        self.df_dict["Lieder mit Chartposition 1"] = self.data_frame_most_successful
        self.df_dict["Feature-Median pro Jahr"] = median_df

        # self.df_dict = {
        #     "Alle Lieder": self.data_frame,
        #     # "Lieder mit Chartposition 1": self.data_frame_most_successful,
        #     # "Feature-Median pro Jahr": median_df
        # }

        # self.figure_dict = {}
        self.df_lines_dict = {}
        # self.canvas_dict = {}


            # for df in self.df_dict.values():
            #     df[col] = np.true_divide(self.data_frame[col] - self.data_frame[col].min(), np.ptp(self.data_frame[col]))


        self.created_figure = False

        # self.lines_dict = defaultdict(list)
        self.init_figure(list(self.df_dict.values())[0])


        for key, value in self.df_dict.items():

            figure = self.create_figure(key, value)
            if key == "Erfolgreiche Lieder":
                self.figure_p = figure
            print(f'create figure {key}')

        self.count = 0


    def show_labels(self):
        self.label.setVisible(True)
        self.label2.setVisible(True)


    def init_figure(self, dataframe):


        cols = self.feature_list

        feature_labels = []
        description_text = ''

        self.annotation_texts = []

        song_features2: List[SongFeature] = [shared.song_features_dict[feature] for feature in
                                             cols]
        x = [i for i, _ in enumerate(cols)]

        for index, feature in enumerate(song_features2):
            label = f'$F_{{{feature.latex_id}}}$'
            feature_labels.append(label)
            description_text += f'{label} - {feature.display_name}\n'
            self.annotation_texts.append(f'{feature.display_name}')

        if not self.created_figure:
            self.axes = []
            n = len(self.feature_list)
            for i in range(n - 1):
                ax = self.figure_p.add_subplot(1, n - 1, i + 1)
                ax.set_facecolor('#f0f0f0')
                self.axes.append(ax)

        def set_ticks_for_axis(dim, ax, ticks):
            min_val, max_val, val_range = self.min_max_range[cols[dim]]
            step = val_range / float(ticks - 1)
            tick_labels = human_format([round(min_val + step * i, 2) for i in range(ticks)])
            norm_min = self.data_frame[cols[dim]].min()
            norm_range = np.ptp(self.data_frame[cols[dim]])
            norm_step = norm_range / float(ticks - 1)
            ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
            ax.yaxis.set_ticks(ticks)
            ax.set_yticklabels(tick_labels)

        if not self.created_figure:
            for dim, ax in enumerate(self.axes):
                ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
                set_ticks_for_axis(dim, ax, ticks=6)
                # ax.set_xticklabels([feature_labels[dim]])

            # Move the final axis' ticks to the right-hand side
            ax = plt.twinx(self.axes[-1])

            dim = len(self.axes)
            ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
            set_ticks_for_axis(dim, ax, ticks=6)

            # ax.set_xticklabels([feature_labels[-2], feature_labels[-1]])

            self.figure_p.subplots_adjust(wspace=0)

            plt.legend(
                [plt.Line2D((0, 1), (0, 0), color='blue') for cat in dataframe['decade'].cat.categories],
                ['1950s', '1960s', '1970s', '1980s', '1990s'],
                bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=0.)

            return self.figure_p


    def create_figure(self, dict_key, dataframe):
        self.df_lines_dict[dict_key] = defaultdict(list)

        cols = self.feature_list
        song_features2: List[SongFeature] = [shared.song_features_dict[feature] for feature in
                                             self.feature_list]



        x = [i for i, _ in enumerate(self.feature_list)]

        for i, ax in enumerate(self.axes):
            for idx in dataframe.index:
                year = dataframe.loc[idx, 'year']

                ax.plot(x, dataframe.loc[idx, self.feature_list], color='navy', alpha=0.4)
                self.df_lines_dict[dict_key][i].append(Line(ax.lines[-1], year))
            ax.set_xlim([x[i], x[i + 1]])

        self.created_figure = True


    def update_year(self):
        value = self.range_slider.value()
        self.mini = value[0] + 1958
        self.maxi = value[1] + 1958

        self.label.setText(str(self.mini))
        self.label2.setText(str(self.maxi))


    def on_df_select(self):
        self.selected_dataframe_id = self.combo_box.currentText()
        self.selected_dataframe = self.df_dict[self.selected_dataframe_id]
        print(f'selected {self.selected_dataframe_id}')


        self.start_plot_thread()
        # self.canvas = self.canvas_dict[self.selected_dataframe_id]
        # self.canvas.figure = self.figure_dict[self.selected_dataframe_id]
        self.canvas.draw_idle()



    def valuechange(self):
        self.update_year_labels()

        # plot(self.figure, self.mini, self.maxi)
        self.start_plot_thread()
        self.canvas.draw_idle()
        # self.plot()


    def update_year_labels(self):
        print(self.range_slider.value())
        value = self.range_slider.value()
        self.mini = value[0] + 1958
        self.maxi = value[1] + 1958

        self.label.setText(str(self.mini))
        self.label2.setText(str(self.maxi))


    def hover(self, event):

        for i, ax in enumerate(self.figure_p.axes):
            ext = ax.get_window_extent()
            if ext is None or event is None:
                continue

            add_annotation = False

            # 15
            if i == len(self.figure_p.axes) - 1:
                # last ax
                if (ext.x0 + ext.x1) / 2 < event.x < ext.x1 and ext.y0 < event.y < ext.y1:
                    add_annotation = True
            elif i == 0:
                # first ax
                if ext.x0 < event.x < (ext.x0 + ext.x1) / 2 and ext.y0 < event.y < ext.y1:
                    add_annotation = True
            else:
                prev_ext = self.figure_p.axes[i - 1].get_window_extent()
                if (prev_ext.x0 + prev_ext.x1) / 2 <= event.x < (ext.x0 + ext.x1) / 2 and ext.y0 < event.y < ext.y1:
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

        # RangeSlider.setObjectName("RangeSlider")
        self.range_slider.resize(1000, 100)

        self.range_slider.setMinimum(0)
        self.range_slider.setMaximum(1991 - 1958)

        self.range_slider.setRange(0, 1991 - 1958)

        self.range_slider.setMaximumSize(QtCore.QSize(16777215, 30))
        self.range_slider.sliderMoved.connect(self.update_year)

        self.range_slider.sliderReleased.connect(self.valuechange)
        self.update_year_labels()

        print(type(self.figure_p))

        # a figure instance to plot on
        # self.figure, axes = plt.subplots(1, len(self.feature_list)-1, sharey=False)

        # self.figure = plt.figure()

        # this is the Canvas Widget that
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        #
        # for key, value in self.df_dict.items():
        #     self.canvas_dict[key] = FigureCanvas(self.figure_dict[key])

        self.canvas = FigureCanvas(self.figure_p)

        # self.annot = self.figure.annotate("", xy=(0, 0), xytext=(5, 5), textcoords="offset points")
        # self.annot.set_visible(False)

        # TODO uncomment
        self.canvas.mpl_connect('motion_notify_event', self.hover)

        # self.canvas.mouseMoveEvent(self.hover)

        #self.valuechange() # TODO mayabe you need this
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

        self.combo_box = QComboBox()
        self.combo_box.addItems(list(self.df_dict.keys()))
        self.combo_box.setMaximumSize(200, 20)
        self.layout.addWidget(self.combo_box)
        self.combo_box.currentIndexChanged.connect(self.on_df_select)

        self.layout.addWidget(self.canvas)

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label.setMinimumWidth(80)

        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.label2.setMinimumWidth(80)

        vbox = QHBoxLayout()

        vbox.addWidget(self.label)
        vbox.addWidget(self.range_slider)
        vbox.addWidget(self.label2)

        # self.layout.addWidget(self.range_slider)
        self.layout.addLayout(vbox)

        # adding push button to the layout
        # layout.addWidget(self.button)

        # setting layout to the main window
        print('change layout')
        # self.setLayout(self.layout)
        #self.show()

        # self.start_plot_thread()

    def set_my_layout(self):
        self.setLayout(self.layout)

    def start_plot_thread(self):
        print("start plot thread")

        for i, ax in enumerate(self.figure_p.axes):
            ax.lines = [line.line for line in self.df_lines_dict[self.selected_dataframe_id][i] if
                        self.mini <= line.year <= self.maxi]


    def update_canvas(self):
        self.canvas.draw_idle()

class Worker(QObject):
    finished = pyqtSignal()
    # progress = pyqtSignal(ParallelCoordinatesWidget)

    def __init__(self, widget):
        super(Worker, self).__init__()
        self.widget = widget

    def run(self):
        #widget = ParallelCoordinatesWidget()
        # widget = LoggedWidget()
        # self.window.set_parallel_coordinates_widget(widget)
        # print('created widget')
        self.widget.init()
        self.finished.emit()

class Window(QMainWindow):
    # constructor
    def __init__(self, parent=None, window_title=''):
        super(Window, self).__init__(parent)
        self.setGeometry(400, 200, 1000, 600)
        self.setWindowTitle(window_title)

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        login_widget = LoadingWidget(self)
        # login_widget.button.clicked.connect(self.login)
        self.central_widget.addWidget(login_widget)

        self.parallel_coordinates_widget = ParallelCoordinatesWidget(self)
        # self.parallel_coordinates_widget.init()
        #
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self.parallel_coordinates_widget)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        self.thread.finished.connect(self.show_gui)

    # def set_parallel_coordinates_widget(self, widget):
    #     self.parallel_coordinates_widget = widget

    # def create_widget(self):
    #     self.parallel_coordinates_widget = ParallelCoordinatesWidget(self)
    #     self.parallel_coordinates_widget = ParallelCoordinatesWidget(self)
    #     self.central_widget.addWidget(self.parallel_coordinates_widget)

    def show_gui(self):
        print('show gui')
        self.parallel_coordinates_widget.set_my_layout()
        self.central_widget.addWidget(self.parallel_coordinates_widget)
        self.parallel_coordinates_widget.show_labels()
        self.central_widget.setCurrentWidget(self.parallel_coordinates_widget)



# driver code
if __name__ == '__main__':
    # creating apyqt5 application
    init_song_features()
    app = QApplication(sys.argv)

    # creating a window object
    main = Window(window_title='Interaktive Parallelkoordinaten')

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())
