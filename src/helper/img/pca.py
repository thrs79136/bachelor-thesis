import os
from collections import defaultdict
from typing import List

import pandas as pd
import numpy as np
import random as rd

from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn import preprocessing
import plotly.express as px
from sklearn import datasets

import matplotlib.pyplot as plt
from sklearn.preprocessing import scale  # Data scaling
from sklearn import decomposition  # PCA
import pandas as pd  # pandas
from sklearn.datasets import load_digits

from src.helper.absolute_surprise import get_song_surprise
from src.helper.file_helper import write_text_file
from src.models.song import Song
from src.models.spotify_song_data import audio_feature_keys

genres_to_color = {
    'rock': 'red',
    'pop': 'yellow',
    'blues': 'blue',
    'soul': 'black',
    'country': 'green',
    ('blues', 'rock', 'soul'): 'indigo',
    ('pop', 'rock'): 'orange',
    ('pop', 'soul'): 'darkkhaki',
    ('blues', 'rock'): 'blueviolet',
    ('country', 'pop'): 'yellowgreen',
    ('blues', 'pop', 'rock'): 'sienna',
    ('rock', 'soul'): 'darkred',
    ('pop', 'rock', 'soul'): 'darkgoldenrod',
    ('blues', 'soul'): 'darkblue',
    ('country', 'pop', 'rock'): 'darkkhaki',
    ('country', 'rock'): 'saddlebrown',
}

def get_cov_ellipse(cov, centre, nstd, **kwargs):
    """
    Return a matplotlib Ellipse patch representing the covariance matrix
    cov centred at centre and scaled by the factor nstd.

    """

    # Find and sort eigenvalues and eigenvectors into descending order
    eigvals, eigvecs = np.linalg.eigh(cov)
    order = eigvals.argsort()[::-1]
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]

    # The anti-clockwise angle to rotate our ellipse by
    vx, vy = eigvecs[:,0][0], eigvecs[:,0][1]
    theta = np.arctan2(vy, vx)

    # Width and height of ellipse to draw
    width, height = 2 * nstd * np.sqrt(eigvals)
    return Ellipse(xy=centre, width=width, height=height,
                   angle=np.degrees(theta), **kwargs)


def eigsorted(cov):
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    return vals[order], vecs[:,order]


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


def get_common_genres(song: Song):
    genres = song.genres
    genres_for_color = []

    for genre in genres:
        if genres_to_color.get(genre, -1) != -1:
            genres_for_color.append(genre)

    if len(genres_for_color) == 0:
        color = 'Other'
    elif len(genres_for_color) == 1:
        return str(genres_for_color[0])
    else:
        required_comb = []
        for genre in genres_for_color:
            if genres_to_color.get(genre, -1) != -1:
                required_comb.append(genre)
        sor = tuple(sorted(required_comb))
        return str(sor)

    return color


def get_genres_to_color(song: Song):
    genres = song.genres
    genres_for_color = []

    for genre in genres:
        if genres_to_color.get(genre, -1) != -1:
            genres_for_color.append(genre)

    if len(genres_for_color) == 0:
        color = 'grey'
    elif len(genres_for_color) == 1:
        color = genres_to_color.get(genres[0], -1)
        if color == -1:
            return 'grey'
    else:
        required_comb = []
        for genre in genres_for_color:
            if genres_to_color.get(genre, -1) != -1:
                required_comb.append(genre)
        sor = tuple(sorted(required_comb))
        color = genres_to_color.get(sor, -1)

    return color

def chart_pos_to_color(song):
    pos = song.peak_chart_position
    if pos < 4:
        return 'green'
    if pos < 13:
        return 'blue'
    if pos < 34:
        return 'purple'
    return 'red'


def get_circle_of_fiths_dist(song: Song):
    def process_result(result, dist, scale_id):
        result += dist
        return result


    return song.analyze_different_keys_general(process_result, lambda res, chord_count: res/chord_count, False)


def pca(songs: List[Song]):
    # features = audio_feature_keys

    features = ['duration_ms', 'energy', 'loudness', 'speechiness',
                          'acousticness',
                          'instrumentalness', 'tempo']

    # feature_names = features_dict.keys()


    song_ids = [song.mcgill_billboard_id for song in songs]
    # audio_feature_keys


    songs_df = pd.DataFrame(columns=song_ids, index=audio_feature_keys)

    # for i in range(len(songs)):
    #     for audio_feature in audio_feature_keys:
    #         audio_feature_value = songs[i].spotify_song_data.audio_features_dictionary[audio_feature]
    #         songs_df.loc[audio_feature, songs[i].mcgill_billboard_id] = audio_feature_value


    first_id = songs[0].mcgill_billboard_id
    last_id = songs[-1].mcgill_billboard_id
    # 2nd try
    for key in audio_feature_keys:
        feature_value_list = [song.spotify_song_data.audio_features_dictionary[key] for song in songs]
        songs_df.loc[key, first_id:last_id] = feature_value_list



    # data = pd.DataFrame(columns=[*wt, *ko], index=genes)
    #
    # for i, gene in enumerate(data.index):
    #     data.loc[gene, 'wt1':'wt5'] = [97, 91, 99, 98, 91]
    #     data.loc[gene, 'ko1':'ko5'] = [9, 4, 8, 3, 8]


    print(songs_df.head())
    print(songs_df.shape)

    scaled_data = preprocessing.scale(songs_df.T)

    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)

    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]

    plt.bar(x=range(1, len(per_var) + 1), height=per_var, tick_label=labels)
    plt.ylabel('Percentage of Explained Variance')
    plt.xlabel('Principal component')
    plt.title('Scree Plot')
    plt.show()

    pca_df = pd.DataFrame(pca_data, index=song_ids, columns=audio_feature_keys)

    #test = pca_df.index.map(color_map)
    # c=pca_df.index.map(color_map)

    plt.scatter(pca_df.PC1.values, pca_df.PC2.values)
    plt.title('My PCA Graph')
    plt.xlabel('PC1 - {0}%'.format(per_var[0]))
    plt.ylabel('PC2 - {0}%'.format(per_var[1]))

    # for sample in pca_df.index:
    # plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

    plt.show()

    for i in range(2):
        loading_scores = pd.Series(pca.components_[i], index=genes)
        sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

        top_10_genes = sorted_loading_scores[0:10].index.values

        print(loading_scores[top_10_genes])


def pca_test():
    population = np.random.rand(100)
    Area = np.random.randint(100, 600, 100)
    continent = ['North America', 'Europe', 'Asia', 'Australia'] * 25

    df = pd.DataFrame(dict(population=population, Area=Area, continent=continent))

    fig, ax = plt.subplots()

    colors = {'North America': 'red', 'Europe': 'green', 'Asia': 'blue', 'Australia': 'yellow'}

    ax.scatter(df['population'], df['Area'], c=df['continent'].map(colors))

    plt.show()


def pca_test2(songs: List[Song], title, color_fn):
    dir = '../data/pca/' + title.lower().replace(' ', '_')
    if not os.path.exists(dir):
        os.mkdir(dir)


    # feature_names = features_dict.keys()

    # genes = ['danceability', 'duration_ms', 'energy', 'loudness', 'speechiness', 'acousticness',
    #     'instrumentalness', 'liveness', 'valence', 'tempo']
    # genes = ['duration_ms', 'loudness', 'acousticness',
    #                       'instrumentalness', 'tempo']
    genes = []
    additional_features = ['minor_perc',
                           'absolute_surprise',
                           'circle_of_fiths_dist',
                           'different_chords_count',
                           'non_triad_rate',
                           'different_sections_count',
                           'peak_chart_pos',
                           'section_repetitions_count',
                           'pentatonic_notes',
                           'metre_changes_count',
                           'tonic_changes_count',
                           'tension_use',
                           'foreign_scale_notes',
                           'different_keys']
    feature_fn = [Song.get_minor_count,
                  get_song_surprise,
                  get_circle_of_fiths_dist,
                  Song.get_different_chords_count,
                  Song.get_non_triad_rate,
                  Song.get_different_sections_count,
                  Song.get_peak_chart_position,
                  Song.get_section_repetitions_count,
                  Song.pentatonic_notes,
                  Song.get_metre_changes_count,
                  Song.get_tonic_changes_count,
                  Song.get_tension_use,
                  Song.get_foreign_scale_notes,
                  Song.analyze_different_keys2,
                  ]



    wt = ['song' + str(song.mcgill_billboard_id) for song in songs]
    firstkey = wt[0]
    lastkey = wt[-1]

    data = pd.DataFrame(columns=[*wt], index=genes)


    # for i, audio_feature in enumerate(data.index):
    #     data.loc[audio_feature, firstkey:lastkey] = \
    #         [song.spotify_song_data.audio_features_dictionary[audio_feature] for song in songs]
    for i, key in enumerate(additional_features):
        feature_value_list = [feature_fn[i](song) for song in songs]
        data.loc[key, firstkey:lastkey] = feature_value_list
        genes.append(key)


    print(data.head())
    print(data.shape)

    scaled_data = preprocessing.scale(data.T)

    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)

    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]

    plt.bar(x=range(1, len(per_var) + 1), height=per_var, tick_label=labels)
    plt.ylabel('Percentage of Explained Variance')
    plt.xlabel('Principal component')
    plt.title('Scree Plot')
    plt.savefig(dir + '/scree_plot.png')
    plt.show()

    pca_df = pd.DataFrame(pca_data, index=[*wt], columns=labels)

    # c=pca_df.index.map(color_map)

    colors = []
    color_list_indices = defaultdict(list)
    for index, song in enumerate(songs):
        # create color list
        color = color_fn(song)
        colors.append(color_fn(song))
        color_list_indices[color].append(index)

    # colors = [color_fn(song) for song in songs]
    # colors = [chart_pos_to_color(song) for song in songs]

    fig, ax = plt.subplots()
    plt.scatter(pca_df.PC1.values, pca_df.PC2.values, c=colors, s=7)

    for genre in ['rock', 'pop', 'blues', 'soul', 'country']:
    #for genre_color in ['green', 'blue', 'red', 'purple']:
        pca1_values = []
        pca2_values = []

        genre_color = genres_to_color[genre]
        for index, color in enumerate(colors):
            if color == genre_color:
                pca1_values.append(pca_df.PC1.values[index])
                pca2_values.append(pca_df.PC2.values[index])

        ellipse = get_ellipse(pca1_values, pca2_values, genre_color)
        ax.add_artist(ellipse)

    # e = Ellipse(xy=(0,0), width=5, height=2,
    #                angle=np.degrees(-2.7))

    size = len(songs)
    lp = lambda genre, color: plt.plot([], color=color, ms=7, mec="none",
                            label=genre.capitalize(), ls="", marker="o")[0]

    genre_items = [i for i in genres_to_color.items() if isinstance(i[0], str)]
    # handles = [lp(k, v) for k, v in genre_items] + [lp('None', 'grey')]
    handles = [lp(k, v) for k, v in [('1st quarter', 'green'), ('2nd quarter', 'blue'), ('3rd quarter', 'purple'), ('4th quarter', 'red')]]
    plt.legend(handles=handles)

    plt.title(title)
    plt.xlabel('PC1 - {0}%'.format(per_var[0]))
    plt.ylabel('PC2 - {0}%'.format(per_var[1]))

    plt.savefig(dir + '/scatter_plot.png')

    plt.show()



    # for sample in pca_df.index:
    # plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))



    file_content = ''
    for i in range(2):
        loading_scores = pd.Series(pca.components_[i], index=genes)
        sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

        top_10_genes = sorted_loading_scores[0:10].index.values


        file_content += f'PCA{str(i+1)}\n{str(loading_scores[top_10_genes])}\n\n'
        write_text_file(dir + '/loading_scores.txt', file_content)


def pca_test_backup(songs: List[Song]):
    # feature_names = features_dict.keys()

    color_map = {
        'ko1': 'red', 'ko2': 'red', 'ko3': 'red', 'ko4': 'red', 'ko5': 'red',
        'wt1': 'blue', 'wt2': 'blue', 'wt3': 'blue', 'wt4': 'blue', 'wt5': 'blue'

    }

    genes = ['gene' + str(i) for i in range(1, 101)]

    wt = ['wt' + str(i) for i in range(1, 6)]
    ko = ['ko' + str(i) for i in range(1, 6)]

    data = pd.DataFrame(columns=[*wt, *ko], index=genes)

    for i, gene in enumerate(data.index):
        data.loc[gene, 'wt1':'wt5'] = rd.choices(range(0, 10), k=5)
        data.loc[gene, 'ko1':'ko5'] = rd.choices(range(0, 30), k=5)

    print(data.head())
    print(data.shape)

    scaled_data = preprocessing.scale(data.T)

    pca = PCA()
    pca.fit(scaled_data)
    pca_data = pca.transform(scaled_data)

    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = ['PC' + str(x) for x in range(1, len(per_var) + 1)]

    plt.bar(x=range(1, len(per_var) + 1), height=per_var, tick_label=labels)
    plt.ylabel('Percentage of Explained Variance')
    plt.xlabel('Principal component')
    plt.title('Scree Plot')
    plt.show()

    pca_df = pd.DataFrame(pca_data, index=[*wt, *ko], columns=labels)

    test = pca_df.index.map(color_map)
    c=pca_df.index.map(color_map)

    plt.scatter(pca_df.PC1.values, pca_df.PC2.values, c=['blue']*5 + ['red']*5)
    plt.title('My PCA Graph')
    plt.xlabel('PC1 - {0}%'.format(per_var[0]))
    plt.ylabel('PC2 - {0}%'.format(per_var[1]))

    # for sample in pca_df.index:
    # plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))

    plt.show()

    for i in range(2):
        loading_scores = pd.Series(pca.components_[i], index=genes)
        sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

        top_10_genes = sorted_loading_scores[0:10].index.values

        print(loading_scores[top_10_genes])

