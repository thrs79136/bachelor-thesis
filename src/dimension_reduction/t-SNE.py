import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
from sklearn.manifold import TSNE
from sklearn import preprocessing


from src.dimension_reduction.common import create_scatterplot_with_ellipses, color_palette, decade_color_map, \
    feature_list, \
    add_labels_and_ellipses_for_genres, spotify_playlists_path

dir = '../../data/img/plots/scatter_plots/dimension_reduction/t-SNE'

data = pd.read_csv('../../data/csv/song_features.csv')
# data = pd.read_csv(spotify_playlists_path)

dropped_columns  = [
    'decade',
    'year',
    'artist',
    # 'minor_percentage',
    'major_percentage',
    'absolute_surprise',
    # 'circle_of_fifths_dist',
    'circle_of_fifths_dist_largest_dist',
    'danceability',
    'energy',
    # 'tonic_percentage',
    'supertonic_percentage',
    # 'dominant_percentage',
    'non_triad_chords_percentage',
    'different_sections_count',
    # 'get_added_seventh_use',
    'get_added_sixth_use',
    'power_chords',
    'neither_chords',
    'section_repetitions',
    'i_to_v',
    'v_to_i',
    'chart_pos',
    'spotify_popularity',
    'genre',
    'mode',
    # 'tempo',
    'valence',
    # 'duration',
    # 'chord_distances',
    # 'different_chords',
    # 'different_progressions',
    'chord_surprise'
]

# decade
#data_dropped = data.drop(dropped_columns, axis=1)

# data = data.drop(data[(data.artist != 'Elvis Presley') & (data.artist != 'The Rolling Stones') & (data.artist != 'The Beatles') & (data.artist != 'Brenda Lee') & (data.artist != 'James Brown')].index)

data_dropped = data[
    feature_list
].values


# 10 - 1000
m = TSNE(learning_rate=100)

scaled_data = preprocessing.scale(data_dropped)


tsne_features = m.fit_transform(scaled_data)

data['x'] = tsne_features[:,0]
data['y'] = tsne_features[:,1]




def map_artist(input):
    artist_to_color_dict = {
        'Elvis Presley': 'red',
        'The Rolling Stones': 'blue',
        'The Beatles': 'green',
        'Brenda Lee': 'purple',
        'James Brown': 'black'

    }

    color = artist_to_color_dict.get(input, -1)
    if color == -1:
        return 'grey'
    return color


    x = 42

# fig, ax = plt.subplots()
# plt.scatter(
#     tsne_features[:,0],
#     tsne_features[:,1],
#     s=50,
#     marker='o',
#     c=[color_palette[x] for x in data.decade.map(decade_color_map)],
#     #c=[x for x in data.artist.map(map_artist)],
#     edgecolors='white',
# )

#sns.scatterplot(x='x', y='y', hue='decade', data=data)

create_scatterplot_with_ellipses(data, tsne_features[:, 0], tsne_features[:, 1], dir, 't-SNE')

