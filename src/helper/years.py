from collections import defaultdict, OrderedDict
from typing import List

import numpy as np

from src.helper.img.lineplot import lineplot
from src.models.song import Song

years_dict = None

def init_years_dict(songs: List[Song]):
    global years_dict

    if years_dict == None:
        years_dict = defaultdict(list)
        # init dictionary
        for song in songs:
            years_dict[song.chart_year].append(song)

def get_years_dict(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    return years_dict



def draw_feature_line_plot(songs: List[Song], feature_fn, ylabel, file_name, title='', suptitle='', dir='', fn_parameters=[]):
    global years_dict

    init_years_dict(songs)

    od = OrderedDict(sorted(years_dict.items()))

    medians = []

    for value in od.values():
        feature_values = [feature_fn(song, *fn_parameters) for song in value]
        medians.append(np.median(feature_values))

    years = [int(year) for year in od.keys()]
    if title == '':
        title = ylabel
    lineplot(years, medians, 'Jahr', ylabel, file_name, title, suptitle, dir)


def draw_genres_line_plot(songs: List[Song]):
    init_years_dict(songs)



