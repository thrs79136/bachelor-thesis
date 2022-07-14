from collections import defaultdict
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

from src.helper.absolute_surprise import get_song_surprise
from src.helper.img.pca import get_circle_of_fiths_dist, get_genres_to_color, get_common_genres
from src.helper.years import get_years_dict
from src.models.song import Song



def create_parallel_coordinates_plot(songs: List[Song]):
    features = ['decade',
                           #'different_chords_count',
                           'section_repetitions_count',
                           'minor_perc',
                           'absolute_surprise',
                           'different_keys']
    feature_fn = [
                Song.get_decade,
                #Song.get_different_chords_count,
                Song.get_section_repetitions_count,
                Song.get_minor_count,
                get_song_surprise,
                Song.analyze_different_keys2,
                ]

    df_data = {}
    for index, value in enumerate(features):
        df_data[value] = [feature_fn[index](song) for song in songs]


    data = pd.DataFrame(df_data)
    parallel_coordinates(data, 'decade', color=['blue', 'orange', 'purple', 'yellow', 'red'], sort_labels=True)

    plt.savefig('../data/img/plots/line_plots/test.png')

    plt.show()



def create_parallel_coordinates_plot_years(songs: List[Song]):
    features = [
        #'decade',
       #'different_chords_count',
       'section_repetitions_count',
       'minor_perc',
       'absolute_surprise',
       'different_keys']
    feature_fn = [
                #Song.get_decade,
                #Song.get_different_chords_count,
                Song.get_section_repetitions_count,
                Song.get_minor_count,
                get_song_surprise,
                Song.analyze_different_keys2,
                ]

    df_data = defaultdict(list)


    years_dict = get_years_dict(songs)
    for year, songs in years_dict.items():
        decade = int(year) - (int(year) % 10)
        df_data['decade'].append(decade)
        for index, value in enumerate(features):
            median = np.median([feature_fn[index](song) for song in songs])
            df_data[value].append(median)


    # for index, value in enumerate(features):
    #     df_data[value] = [feature_fn[index](song) for song in songs]


    data = pd.DataFrame(df_data)
    parallel_coordinates(data, 'decade', color=['blue', 'orange', 'purple', 'yellow', 'red'], sort_labels=True)

    plt.savefig('../data/img/plots/parallel_coordinates/years_median.png')

    plt.show()



