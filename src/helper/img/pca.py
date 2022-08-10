import os
from collections import defaultdict
from typing import List
import numpy as np
import seaborn as sns
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt
import pandas as pd
from src.helper.file_helper import write_text_file
from src.models.pca_config import PCAConfig
from src.models.song import Song

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
    try:
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
    except Exception:
        x = 32
        return None


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


def popularity_to_color(song):
    popularity = song.get_spotify_popularity()
    if popularity < 38:
        return 'green'
    if popularity < 50:
        return 'blue'
    if popularity < 62:
        return 'purple'
    return 'red'


def decade_to_color(song):
    decade = song.get_decade

    return {
        1960: 'orange',
        1970: 'red',
        1980: 'blue',
        1990: 'green'
            }[decade]


def get_circle_of_fiths_dist(song: Song):
    def process_result(result, dist, scale_id):
        result += dist
        return result


    return song.analyze_different_keys_general(process_result, lambda res, chord_count: res/chord_count, False)


feature_list1  = [
    # 'decade',
    # 'year',
    'minor_percentage',
    # 'major_percentage',
    # 'absolute_surprise',
    'circle_of_fifths_dist',
    # 'circle_of_fifths_dist_largest_dist',
    # 'danceability',
    # 'energy',
    'tonic_percentage',
    # 'supertonic_percentage',
    'dominant_percentage',
    #'non_triad_chords_percentage',
    # 'different_sections_count',
    'get_added_seventh_use',
    # 'get_added_sixth_use',
    # 'power_chords',
    # 'neither_chords',
    # 'section_repetitions',
    # 'i_to_v',
    # 'v_to_i',
    # 'chart_pos',
    # 'spotify_popularity',
    # 'genre',
    # 'mode',
    'tempo',
    # 'valence',
    'duration',
    'chord_distances',
    'different_chords',
    'different_progressions',
    # 'chord_surprise'
]



def pca_test2(songs: List[Song], title, pca_config: PCAConfig):

    color_palette = sns.color_palette('magma')

    dir = '../data/pca/' + title.lower().replace(' ', '_')
    if not os.path.exists(dir):
        os.mkdir(dir)

    genes = []

    wt = ['song' + str(song.mcgill_billboard_id) for song in songs]
    firstkey = wt[0]
    lastkey = wt[-1]

    data = pd.DataFrame(columns=[*wt], index=genes)

    for feature in pca_config.features:
    #for i, key in enumerate(feature_names):
        #feature = dictionaries.song_features_dict[key]
        feature_fn = feature.feature_fn

        feature_value_list = []
        for song in songs:
            parameters = [song] + feature.parameters
            feature_value_list.append(feature_fn(*parameters))

        data.loc[feature.feature_id, firstkey:lastkey] = feature_value_list
        genes.append(feature.feature_id)


    # create dataframe

    data = pd.read_csv('./../data/csv/song_features.csv')

    print(data.head())
    print(data.shape)
    dropped_columns = [
        # 'decade',
        # 'year',
        'minor_percentage',
        # 'major_percentage',
        # 'absolute_surprise',
        'circle_of_fifths_dist',
        # 'circle_of_fifths_dist_largest_dist',
        # 'danceability',
        # 'energy',
        'tonic_percentage',
        # 'supertonic_percentage',
        'dominant_percentage',
        # 'non_triad_chords_percentage',
        # 'different_sections_count',
        'get_added_seventh_use',
        # 'get_added_sixth_use',
        # 'power_chords',
        # 'neither_chords',
        # 'section_repetitions',
        # 'i_to_v',
        # 'v_to_i',
        # 'chart_pos',
        # 'spotify_popularity',
        # 'genre',
        # 'mode',
        'tempo',
        # 'valence',
        'duration',
        'chord_distances',
        'different_chords',
        'different_progressions',
        # 'chord_surprise'
    ]

    # decade
    #data_dropped = data.drop(dropped_columns, axis=1)

    data_dropped = data[
        feature_list1
    ].values

    scaled_data = preprocessing.scale(data_dropped)

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

    decade_color_map = {1950: 0, 1960: 1, 1970: 2, 1980: 3, 1990: 4}
    color_list = data['decade'].map(decade_color_map)

    colors = []
    color_list_indices = defaultdict(list)
    for index, song in enumerate(songs):
        # create color list
        color = pca_config.color_fn(song)
        colors.append(pca_config.color_fn(song))
        color_list_indices[color].append(index)


    fig, ax = plt.subplots()
    plt.scatter(pca_df.PC1.values, pca_df.PC2.values,
                #c=colors,
                s = 20,
                marker='o',
                c=[color_palette[x] for x in
                   data.decade.map({1950: 0, 1960: 1, 1970: 2, 1980: 3, 1990: 4})],
                edgecolors='white',
                )

    # for genre in ['rock', 'pop', 'blues', 'soul', 'country']:
    # DRAW ellipses
    for k, decade_color in decade_color_map.items():
        pca1_values = []
        pca2_values = []
        for index, color in enumerate(color_list):
            if color == decade_color:
                pca1_values.append(pca_df.PC1.values[index])
                pca2_values.append(pca_df.PC2.values[index])

        ellipse = get_ellipse(pca1_values, pca2_values, color_palette[decade_color])
        ax.add_artist(ellipse)
    # DRAW ellipses end


    size = len(songs)
    lp = lambda genre, color: plt.plot([], color=color_palette[color], ms=7, mec="none",
                            label=str(genre), ls="", marker="o")[0]

    genre_items = [i for i in genres_to_color.items() if isinstance(i[0], str)]
    # handles = [lp(k, v) for k, v in genre_items] + [lp('None', 'grey')]
    handles = [lp(k, v) for k, v in decade_color_map.items()]
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




def pca_old(songs: List[Song], title, pca_config: PCAConfig):
    dir = '../data/pca/' + title.lower().replace(' ', '_')
    if not os.path.exists(dir):
        os.mkdir(dir)

    genes = []

    wt = ['song' + str(song.mcgill_billboard_id) for song in songs]
    firstkey = wt[0]
    lastkey = wt[-1]

    data = pd.DataFrame(columns=[*wt], index=genes)

    for feature in pca_config.features:
    #for i, key in enumerate(feature_names):
        #feature = dictionaries.song_features_dict[key]
        feature_fn = feature.feature_fn

        feature_value_list = []
        for song in songs:
            parameters = [song] + feature.parameters
            feature_value_list.append(feature_fn(*parameters))

        data.loc[feature.feature_id, firstkey:lastkey] = feature_value_list
        genes.append(feature.feature_id)




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
        color = pca_config.color_fn(song)
        colors.append(pca_config.color_fn(song))
        color_list_indices[color].append(index)


    fig, ax = plt.subplots()
    plt.scatter(pca_df.PC1.values, pca_df.PC2.values, c=colors, s=7)

    # for genre in ['rock', 'pop', 'blues', 'soul', 'country']:
    # DRAW ellipses
    for possible_color in pca_config.all_colors:
        pca1_values = []
        pca2_values = []

        #genre_color = genres_to_color[genre]
        for index, color in enumerate(colors):
            if color == possible_color:
                pca1_values.append(pca_df.PC1.values[index])
                pca2_values.append(pca_df.PC2.values[index])

        ellipse = get_ellipse(pca1_values, pca2_values, possible_color)
        ax.add_artist(ellipse)
    # DRAW ellipses end


    size = len(songs)
    lp = lambda genre, color: plt.plot([], color=color, ms=7, mec="none",
                            label=genre.capitalize(), ls="", marker="o")[0]

    genre_items = [i for i in genres_to_color.items() if isinstance(i[0], str)]
    # handles = [lp(k, v) for k, v in genre_items] + [lp('None', 'grey')]
    handles = [lp(k, v) for k, v in pca_config.color_labels]
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





