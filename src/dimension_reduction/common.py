import os
from copy import copy
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import seaborn as sns

from src.helper.statistics.feature_analyzer import get_genre_group_string
from src.helper.statistics_helper import most_common_genres

mcgill_features_path = '../data/csv/song_features.csv'
spotify_playlists_path = '../data/csv/years/spotify.csv'
spotify_genres_playlists_path = '../data/csv/spotify_genres.csv'

global color_palette

class DimensionReductionConfig:
    def __init__(self, csv_file, feature_list, color_palette, color_map):
        self.csv_file = csv_file
        self.feature_list = feature_list
        self.color_palette = color_palette
        self.color_map = color_map


audio_feature_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
color_palette = sns.color_palette('magma', n_colors=7)


# spotify_genres_config = DimensionReductionConfig(spotify_playlists_path, audio_feature_keys, color_palette, decade_color_map)



# current_config = spotify_genres_config




global genre_color_map
genre_color_map = {'pop': 0, 'rock': 1, 'soul': 2, 'country': 3, 'blues': 4}

global parallel_coordinates_feature_list
parallel_coordinates_feature_list = [
    'circle_of_fifths_dist',  # 1
    'get_added_seventh_use',  # 2
    'different_progressions',  # 3
    'tonic_percentage',  # 4
    'chord_distances',  # 5
    'minor_or_major',  # 8
    'dominant_percentage',  # 9
    'different_chords',  # 7
    'average_chord_count_per_bar',  # 11
    'different_sections_count',  # 6
    'duration',  # 10
    'minor_percentage',  # 12
    'chorus_repetitions',  # 13
    'acousticness',
    'energy',
    'danceability',
]


global feature_list_all
# parallel coordinates
# feature_list = [
#     'circle_of_fifths_dist',  # 1
#     'get_added_seventh_use',  # 2
#     'different_progressions',  # 3
#     'tonic_percentage',  # 4
#     'chord_distances',  # 5
#     'minor_or_major',  # 8
#     'dominant_percentage',  # 9
#     'different_chords',  # 7
#     'average_chord_count_per_bar',  # 11
#     'different_sections_count',  # 6
#     'duration',#10
#     'minor_percentage',  # 12
#     'chorus_repetitions'#13
# ]

feature_list_all = [
    'duration',
    'acousticness',
    # 'spotify_popularity',
    'chord_distances2',
    'chorus_repetitions',
    'energy',
    'danceability',
    'major_percentage',
    # 'absolute_surprise',
    # 'chord_surprise',
    # 'neither_chords',
    'different_sections_count',
    'non_triad_chords_percentage',
    'get_added_seventh_use',
    'circle_of_fifths_dist',
    #'chord_distances',
    # 'different_progressions',
    # 'different_chords',
    # 'v_to_i',
    # 'tonic_percentage',
    # 'i_to_v',
    # 'minor_percentage',
    # 'loudness',
    # 'circle_of_fifths_dist_largest_dist',
    # 'different_notes',
    # 'supertonic_percentage',
    # 'power_chords',
    # 'mode',
    # 'average_chord_count_per_bar'
]

# features for song_features.csv with strong correlation
#feature_list_years = ['duration', 'acousticness', 'synthesizer', 'chord_distances2', 'neither_chords', 'major_percentage', 'energy', 'danceability', 'chorus_repetitions', 'different_sections_count', 'non_triad_chords_percentage', 'get_added_seventh_use', 'power_chords', 'different_chords', 'chord_distances', 'tonic_percentage', 'minor_percentage', 'different_progressions', 'v_to_i', 'circle_of_fifths_dist', 'tonic_percentage', 'average_chord_count_per_bar', 'i_to_v', 'loudness', 'circle_of_fifths_dist_largest_dist', 'different_notes']
feature_list_years = ['acousticness', 'danceability', 'duration_ms', 'energy', 'major_chords', 'neither_chords', 'non_triad_chords', 'bass_distances', 'different_sections', 'chorus_repetitions']
#feature_list_chart_pos = ['i_to_v', 'v_to_i', 'chorus_repetitions', 'tonic_percentage', 'danceability', 'loudness', 'minor_percentage', 'circle_of_fifths_dist_largest_dist', 'dominant_percentage']
feature_list_chart_pos = ['danceability', 'loudness', 'minor_chords', 'major_chords', 'tonic_chords', 'circle_of_fifths_max', 'section_repetitions', 'chorus_repetitions']
# feature_list_spotify_popularity = ['acousticness', 'duration', 'chorus_repetitions', 'circle_of_fifths_dist_largest_dist', 'major_percentage', 'neither_chords', 'different_progressions', 'energy', 'circle_of_fifths_dist', 'non_triad_chords_percentage', 'get_added_seventh_use', 'different_notes', 'v_to_i', 'danceability', 'minor_percentage', 'loudness', 'i_to_v', 'chord_distances2', 'power_chords', 'tonic_percentage', 'chord_distances', 'tonic_percentage', 'section_repetitions']
feature_list_spotify_popularity = ['acousticness', 'danceability', 'duration_ms', 'energy', 'loudness', 'major_chords', 'neither_chords', 'seventh_chords', 'v_to_i', 'circle_of_fifths', 'circle_of_fifths_max', 'different_progressions', 'different_notes', 'chorus_repetitions']


feature_list_sentiments = ['love', 'anger', 'joy', 'sadness']
feature_list_without_mcgill = [
    'duration',
    'acousticness',
    'energy',
    'danceability',
    'positive',
    'negative'
]
feature_list_without_mcgill2 = [
    'duration',
    'acousticness',
    'energy',
    'danceability',
    'love', 'anger', 'joy', 'sadness'
]

audio_feature_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']


# feature_list_year = ['acousticness', 'danceability', 'duration_ms', 'energy', 'major_percentage', 'neither_chords', 'non_triad_chords_percentage', 'chord_distances2', 'different_sections_count', 'chorus_repetitions']

# feature_list_year = ['acousticness', 'danceability', 'duration_ms', 'energy', 'major_chords', 'neither_chords', 'non_triad_chords', 'bass_distances', 'different_sections', 'chorus_repetitions']
feature_list_year = ['acousticness', 'danceability', 'duration_ms', 'energy', 'major_chords', 'neither_chords', 'non_triad_chords', 'bass_distances', 'different_sections', 'chorus_repetitions']
# feature_list_chart_pos = ['danceability', 'loudness', 'minor_percentage', 'major_percentage', 'tonic_percentage', 'circle_of_fifths_dist_largest_dist', 'section_repetitions', 'chorus_repetitions']
feature_list_chart_pos = ['danceability', 'loudness', 'minor_chords', 'major_chords', 'tonic_chords', 'circle_of_fifths_max', 'section_repetitions', 'chorus_repetitions']
# feature_list_spotify_popularity = ['acousticness', 'danceability', 'duration_ms', 'energy', 'loudness', 'major_percentage', 'neither_chords', 'get_added_seventh_use', 'v_to_i', 'circle_of_fifths_dist', 'circle_of_fifths_dist_largest_dist', 'different_progressions', 'different_notes', 'chorus_repetitions']
feature_list_spotify_popularity = ['acousticness', 'danceability', 'duration_ms', 'energy', 'loudness', 'major_chords', 'neither_chords', 'seventh_chords', 'v_to_i', 'circle_of_fifths', 'circle_of_fifths_max', 'different_progressions', 'different_notes', 'chorus_repetitions']
feature_list_genre = ['acousticness', 'danceability', 'duration_ms', 'energy', 'loudness',
'minor_chords', 'major_chords', 'seventh_chords', 'standard_triads','v_to_i', 'bass_distances', 'different_sections', 'anger']


feature_list_genre_less = ['acousticness', 'danceability', 'duration_ms', 'energy', 'loudness', 'minor_percentage', 'major_percentage']


feature_lists = {
    'year': feature_list_year,
    'chart_pos': feature_list_chart_pos,
    'spotify_popularity': feature_list_spotify_popularity,
    'genre': feature_list_genre,
    'genre_groups': feature_list_genre
 }

decade_color_map = {
    1950: 0,
    1960: 1,
    1970: 2,
    1980: 3,
    1990: 4,
}

genres_color_map = {
    'rock': 0,
    'pop-rock': 1,
    'pop': 2,
    'soul': 3,
    'country': 4,
    'funk-soul': 5
}

# decade_color_map2 = {
#     1950: 0,
#     1960: 1,
#     1970: 2,
#     1980: 3,
#     1990: 4,
#     2000: 5,
#     2010: 6
# }

color_maps = {
    'year': decade_color_map,
    'genre_groups': genres_color_map
}

color_palette_year = sns.color_palette('magma', n_colors=12)

color_palette = sns.color_palette('magma', n_colors=12)
color_palette_cont = sns.color_palette('magma', as_cmap=True)

color_palettes = {
    'year': sns.color_palette('CMRmap', n_colors=12)[1::2],
    #'genre_groups': [(0.8853517877739331, 0.3190311418685121, 0.29042675893886966), (0.9873125720876587, 0.6473663975394078, 0.3642445213379469), (0.9943179751791559, 0.8313849891525765, 0.36129296971368624), (0.9288735101883892, 0.9715494040753557, 0.6380622837370243), (0.6334486735870821, 0.8521337946943485, 0.6436755094194541), (0.2800461361014994, 0.6269896193771626, 0.7024221453287197)]
    # 'genre_groups': [
    #     '#ba2727', # rock red
    #     '#ec9d22', # poprock orange
    #     '#c8d42c', #pop light orange TODO
    #     '#41bc31', #soul light green TODO
    #     '#2c6bad', # country darker green
    #     '#000000'] # funk sould looks good
    'genre_groups': sns.color_palette('nipy_spectral', n_colors=12)[1::2]
    # 'genre_groups': sns.hls_palette(n_colors=12, s=1)[1::2]    'genre_groups': sns.hls_palette(n_colors=12, s=1)[1::2]
    #'genre_groups':  sns.color_palette('Spectral', n_colors=12)[1::2]

}

feature_list = feature_list_all

use_genres = False

#
# def get_data():
#
#     data = pd.read_csv(current_config.csv_file)
#
#     print(data.head())
#     print(data.shape)
#
#     data_dropped = data[
#         current_config.feature_list
#     ].values
#     return data_dropped

def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]

def create_scatterplot_with_ellipses(data_frame, x_pos, y_pos, colored_feature, directory, title, xlabel=None, ylabel=None):
    # global use_genres

    # if use_genres:
    #     create_scatterplot_with_ellipses_genres(data_frame, x_pos, y_pos, directory, title, xlabel, ylabel)
    #     return

    fig, ax = plt.subplots()

    # plt.title(title)

    # color_list = ['red' if spotify_popularity > 50 else 'blue' for spotify_popularity in data_frame.spotify_popularity]
    # color_indices = [int(pop/100 * 256 - 1) for pop in data_frame.chart_pos]
    # color_indices2 = [int(pop/100 * 256 - 1) for pop in data_frame.chart_pos]
    #
    #
    # colours = []
    # for i in color_indices:
    #     colours.append(color_palette_cont.colors[i])
    group_by_feature = colored_feature if colored_feature != 'year' else 'decade'
    d = data_frame.decade

    color_map = color_maps[colored_feature]
    # c = [color_palette[x] for x in data_frame.decade.map(color_map)]
    color_palette = color_palettes[colored_feature]
    color_list = data_frame[group_by_feature].map(color_map)


    plt.scatter(
        x_pos,
        y_pos,
        s=30,
        marker='o',
        c=[color_palette[x] for x in data_frame[group_by_feature].map(color_map)],
        #c=colours,

        # c=[x for x in data.artist.map(map_artist)],
        edgecolors='white',
    )

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    # if colored_feature == 'year' or colored_feature == 'year_spotify':
    #     color_list = data_frame['decade'].map(color_map)

    for k, decade_color in color_map.items():
        x_values = []
        y_values = []
        for index, color in enumerate(color_list):
            if color == decade_color:
                x_values.append(x_pos[index])
                y_values.append(y_pos[index])


        ellipse = get_ellipse(x_values, y_values, color_palette[decade_color])

        if colored_feature == 'genre_groups':
            center = ellipse.get_center()
            ellipse_shadow = copy(ellipse)
            ellipse_shadow.set_center((center[0]+0.025, center[1]-0.025))
            ellipse_shadow.set_color('black')
            ellipse_shadow.set_alpha(0.7)
            ellipse_shadow.set_facecolor('none')
            ax.add_artist(ellipse_shadow)

        ax.add_artist(ellipse)

    label_string = lambda label: f'{label}er' if colored_feature == 'year' or colored_feature == 'year' else get_genre_group_string(label)

    # Lables
    lp = lambda category, color: plt.plot([], color=color_palette[color], ms=7, mec="none",
                                       label=label_string(str(category)), ls="", marker="o")[0]

    handles = [lp(k, v) for k, v in color_map.items()]
    plt.legend(handles=handles)

    Path(directory).mkdir(parents=True, exist_ok=True)
    plt.savefig(directory + f'/scatter_plot_{colored_feature}.jpg')

    plt.show()


def create_scatterplot_with_ellipses_genres(data_frame, x_pos, y_pos, directory, title, xlabel=None, ylabel=None):
    fig, ax = plt.subplots()

    plt.title(title)

    plt.scatter(
        x_pos,
        y_pos,
        s=30,
        marker='o',
        # c=[color_palette[x] for x in data_frame.decade.map(decade_color_map)],
        # c=[x for x in data.artist.map(map_artist)],
        edgecolors='white',
    )

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    # BEGIN Ellipses
    genres_list = [genre.split('.') for genre in data_frame['genre']]

    # foreach ellipse
    for genre in most_common_genres:
        x_values = []
        y_values = []
        for index, genres in enumerate(genres_list):
            if genre in genres:
                x_values.append(x_pos[index])
                y_values.append(y_pos[index])

        ellipse = get_ellipse(x_values, y_values, color_palette[genre_color_map[genre]])
        ax.add_artist(ellipse)
    # END Ellipses

    # Lables
    lp = lambda genre, color: plt.plot([], color=color_palette[color], ms=7, mec="none",
                                       label=str(genre), ls="", marker="o")[0]

    handles = [lp(k, v) for k, v in genre_color_map.items()]
    plt.legend(handles=handles)

    Path(directory).mkdir(parents=True, exist_ok=True)
    plt.savefig(directory + '/scatter_plot_genre.png')

    plt.show()


def add_labels_and_ellipses_for_genres(plt, ax, data_frame, x_pos, y_pos):
    # BEGIN Ellipses
    genres_list = [genre.split('.') for genre in data_frame['genre']]

    # foreach ellipse
    for genre in most_common_genres:
        x_values = []
        y_values = []
        for index, genres in enumerate(genres_list):
            if genre in genres:
                x_values.append(x_pos[index])
                y_values.append(y_pos[index])

        ellipse = get_ellipse(x_values, y_values, color_palette[genre_color_map[genre]])
        ax.add_artist(ellipse)
    # END Ellipses


def get_ellipse(x, y, color):
    nstd = 1
    cov = np.cov(x, y)
    vals, vecs = eigsorted(cov)
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    w, h = 2 * nstd * np.sqrt(vals)
    ellipse = Ellipse(xy=(np.mean(x), np.mean(y)),
                  width=w, height=h,
                  angle=theta, color=color,
                   linewidth=1)
    ellipse.set_facecolor('none')
    ellipse.set
    return ellipse
