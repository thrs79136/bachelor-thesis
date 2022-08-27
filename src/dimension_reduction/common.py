import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import seaborn as sns

from src.helper.img.pca import eigsorted
from src.helper.statistics_helper import most_common_genres

spotify_playlists_path = '../data/csv/years/spotify.csv'

global decade_color_map
decade_color_map = {1950: 0, 1960: 1, 1970: 2, 1980: 3, 1990: 4, 2000: 5, 2010: 6}

global genre_color_map
genre_color_map = {'pop': 0, 'rock': 1, 'soul': 2, 'country': 3, 'blues': 4}

global feature_list
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

feature_list_spotify = [
    'duration',
    'acousticness',
    # 'spotify_popularity',
    # 'chord_distances2',
    # 'chorus_repetitions',
    'energy',
    'danceability',
    # 'major_percentage',
    # 'absolute_surprise',
    # 'chord_surprise',
    # 'neither_chords',
    # 'different_sections_count',
    # 'non_triad_chords_percentage',
    # 'get_added_seventh_use',
    # 'circle_of_fifths_dist',
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
feature_list_years = ['duration', 'acousticness', 'chord_distances2', 'chorus_repetitions', 'energy', 'danceability', 'major_percentage', 'neither_chords', 'different_sections_count', 'non_triad_chords_percentage', 'get_added_seventh_use', 'chord_distances', 'circle_of_fifths_dist', 'different_chords', 'different_progressions', 'tonic_percentage', 'v_to_i', 'i_to_v', 'minor_percentage', 'loudness', 'circle_of_fifths_dist_largest_dist', 'different_notes', 'supertonic_percentage', 'power_chords']
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


feature_list = audio_feature_keys

global color_palette
color_palette = sns.color_palette('magma', n_colors=7)
color_palette_cont = sns.color_palette('magma', as_cmap=True)


use_genres = False

def create_scatterplot_with_ellipses(data_frame, x_pos, y_pos, dir, title, xlabel=None, ylabel=None):
    global use_genres


    if use_genres:
        create_scatterplot_with_ellipses_genres(data_frame, x_pos, y_pos, dir, title, xlabel, ylabel)
        return

    fig, ax = plt.subplots()

    plt.title(title)

    # color_list = ['red' if spotify_popularity > 50 else 'blue' for spotify_popularity in data_frame.spotify_popularity]
    # color_indices = [int(pop/100 * 256 - 1) for pop in data_frame.chart_pos]
    # color_indices2 = [int(pop/100 * 256 - 1) for pop in data_frame.chart_pos]
    #
    #
    # colours = []
    # for i in color_indices:
    #     colours.append(color_palette_cont.colors[i])
    d = data_frame.decade
    c = [color_palette[x] for x in data_frame.decade.map(decade_color_map)]

    plt.scatter(
        x_pos,
        y_pos,
        s=30,
        marker='o',
        c=[color_palette[x] for x in data_frame.decade.map(decade_color_map)],
        #c=colours,

        # c=[x for x in data.artist.map(map_artist)],
        edgecolors='white',
    )

    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    color_list = data_frame['decade'].map(decade_color_map)

    for k, decade_color in decade_color_map.items():
        x_values = []
        y_values = []
        for index, color in enumerate(color_list):
            if color == decade_color:
                x_values.append(x_pos[index])
                y_values.append(y_pos[index])

        ellipse = get_ellipse(x_values, y_values, color_palette[decade_color])
        ax.add_artist(ellipse)

    # Lables
    lp = lambda genre, color: plt.plot([], color=color_palette[color], ms=7, mec="none",
                                       label=str(genre), ls="", marker="o")[0]

    handles = [lp(k, v) for k, v in decade_color_map.items()]
    plt.legend(handles=handles)

    plt.savefig(dir + '/scatter_plot_spotify_years.png')

    plt.show()


def create_scatterplot_with_ellipses_genres(data_frame, x_pos, y_pos, dir, title, xlabel=None, ylabel=None):
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

    plt.savefig(dir + '/scatter_plot_genre.png')

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
