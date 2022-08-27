import os

import pandas as pd
import umap.umap_ as umap
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns

from src.dimension_reduction.common import decade_color_map, feature_list, get_ellipse, color_palette, genre_color_map, \
    create_scatterplot_with_ellipses, spotify_playlists_path
from src.helper.statistics_helper import most_common_genres


dir = '../../data/img/plots/scatter_plots/dimension_reduction/UMAP'
reducer = umap.UMAP()


wd = os.getcwd()
#data = pd.read_csv('../../data/csv/song_features.csv')
data = pd.read_csv(spotify_playlists_path)


song_features = data[
    feature_list
].values

scaled_song_data = StandardScaler().fit_transform(song_features)
embedding = reducer.fit_transform(scaled_song_data)

# fig, ax = plt.subplots()
# plt.scatter(
#     embedding[:, 0],
#     embedding[:, 1],
#     s=50,
#     marker='o',
#     #c=[decade_to_color(x) for x in data.decade]
#     c=[color_palette[x] for x in data.decade.map(decade_color_map)],
#     edgecolors='white',
# )

create_scatterplot_with_ellipses(data, embedding[:, 0], embedding[:, 1], dir, 'UMAP')


# plt.gca().set_aspect('equal', 'datalim')
# plt.title('UMAP', fontsize=15)
# plt.savefig(dir + '/scatter_plot.png')
#
#
# plt.show()