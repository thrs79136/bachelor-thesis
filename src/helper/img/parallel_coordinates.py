from collections import defaultdict
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates
from matplotlib import ticker

from src.helper.absolute_surprise import get_song_surprise
from src.helper.img.pca import get_circle_of_fiths_dist, get_genres_to_color, get_common_genres
from src.helper.years import get_years_dict
from src.models.song import Song
from matplotlib.pyplot import figure

from src.models.song_feature import SongFeature
from src.shared import song_features

# def create_parallel_coordinates_years_plot(feature_names):
#

def create_parallel_coordinates_plot_newest(feature_names):

    df = pd.read_csv('../data/csv/year_features.csv')

    # categorize decades
    df['decade'] = pd.cut(df['decade'], [1940, 1950, 1960, 1970, 1980, 1990, 2000])


    cols = feature_names
    song_features: List[SongFeature] = [dictionaries.song_features_dict[feature] for feature in feature_names]

    feature_labels = []
    description_text = ''

    for index, feature in enumerate(song_features):
        label = f'F{index+1}'
        feature_labels.append(label)
        description_text += f'{label} - {feature.feature_display_name}\n'


    x = [i for i, _ in enumerate(feature_names)]

    colours = ['green', 'red', 'orange', 'purple', 'blue', 'yellow']
    colours = {df['decade'].cat.categories[i]: colours[i] for i, _ in enumerate(df['decade'].cat.categories)}

    fig, axes = plt.subplots(1, len(x) - 1, sharey=False, figsize=(15, 5))

    min_max_range = {}
    for col in feature_names:
        min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
        df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))

    for i, ax in enumerate(axes):
        for idx in df.index:
            mpg_category = df.loc[idx, 'decade']
            ax.plot(x, df.loc[idx, feature_names], colours[mpg_category])
        ax.set_xlim([x[i], x[i + 1]])

    def set_ticks_for_axis(dim, ax, ticks):
        min_val, max_val, val_range = min_max_range[cols[dim]]
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

    plt.subplots_adjust(wspace=0)

    test = df['decade'].cat.categories


    plt.gcf().subplots_adjust(bottom=0.6)
    fig.text(0.1, 0.02, description_text,
             horizontalalignment='left', wrap=True)

    plt.legend(
        [plt.Line2D((0, 1), (0, 0), color=colours[cat]) for cat in df['decade'].cat.categories],
        ['1950s', '1960s', '1970s', '1980s', '1990s'],
        bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=0.)

    plt.savefig('../data/img/plots/line_plots/years_median.png')

    plt.show()



def create_parallel_coordinates_plot_new(feature_names):
    df = pd.read_csv('../data/csv/song_features.csv')

    song_features: List[SongFeature] = [dictionaries.song_features_dict[feature] for feature in feature_names]

    fig_text = ''
    label_dict = {}
    feature_to_display_name = {}
    for index, feature in enumerate(song_features):
        feature_label = f'F{index+1}'
        label_dict[feature.feature_id] = feature_label
        feature_to_display_name[feature_label] = feature.feature_display_name
        fig_text += feature_label + f'- {feature.feature_display_name}\n'

    # label_dict = {feature.feature_id: feature.feature_display_name for feature in song_features}

    test = df.columns.values
    df.rename(columns=label_dict, inplace=True)

    # df['horsepower'] = pd.to_numeric(df['horsepower'].replace('?', np.nan))
    # df['mpg'] = pd.cut(df['mpg'], [8, 16, 24, 32, 50])

    plt.figure()
    fig, ax = plt.subplots()

    plt.gcf().subplots_adjust(bottom=0.4)


    # columns = [value for value in df.columns.values if value not in ['decade', 'year']]
    fig.text(0.1, 0.02, fig_text,
             horizontalalignment='left', wrap=True)

    parallel_coordinates(df, cols=list(label_dict.values()), class_column='decade')


    plt.show()


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
    plt.xticks(rotation=90)

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



