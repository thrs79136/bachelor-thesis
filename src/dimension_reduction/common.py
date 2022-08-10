import numpy as np
from matplotlib.patches import Ellipse
import seaborn as sns

from src.helper.img.pca import eigsorted
from src.helper.statistics_helper import most_common_genres

global decade_color_map
decade_color_map = {1950: 0, 1960: 1, 1970: 2, 1980: 3, 1990: 4}

global genre_color_map
genre_color_map = {'pop': 0, 'rock': 1, 'soul': 2, 'country': 3, 'blues': 4}

global feature_list
feature_list = [
    # 'decade',
    # 'year',
    'minor_percentage',
    #'major_percentage',
    # 'absolute_surprise',
    'circle_of_fifths_dist',
    # 'circle_of_fifths_dist_largest_dist',
    'danceability',
    'energy',
    'tonic_percentage',
    # 'supertonic_percentage',
    'dominant_percentage',
    # 'non_triad_chords_percentage',
    'different_sections_count',
    'get_added_seventh_use',
    'get_added_sixth_use',
    'power_chords',
    #'neither_chords',
    'section_repetitions',
    # 'i_to_v',
    # 'v_to_i',
    # 'chart_pos',
    # 'spotify_popularity',
    # 'genre',
    'mode',
    # 'tempo',
    'valence',
    #'duration',
    'chord_distances',
    'different_chords',
    'different_progressions',
    # 'chord_surprise'
]
# feature_list = [
#     # 'decade',
#     # 'year',
#     'minor_percentage',
#     #'major_percentage',
#     #'absolute_surprise',
#     'circle_of_fifths_dist',
#     #'circle_of_fifths_dist_largest_dist',
#     'danceability',
#     'energy',
#     'tonic_percentage',
#     #'supertonic_percentage',
#     'dominant_percentage',
#     #'non_triad_chords_percentage',
#     'different_sections_count',
#     'get_added_seventh_use',
#     #'get_added_sixth_use',
#     #'power_chords',
#     #'neither_chords',
#     'section_repetitions',
#     #'i_to_v',
#     #'v_to_i',
#     #'chart_pos',
#     #'spotify_popularity',
#     #'genre',
#     #'mode',
#     'tempo',
#     #'valence',
#     #'duration',
#     'chord_distances',
#     'different_chords',
#     'different_progressions',
#     #'chord_surprise'
# ]

global color_palette
color_palette = sns.color_palette('magma')



def add_labels_and_ellipses(ax, data_frame, x_pos, y_pos):
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


def add_labels_and_ellipses_for_genres(ax, data_frame, x_pos, y_pos):
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
