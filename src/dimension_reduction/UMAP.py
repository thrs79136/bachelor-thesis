import os

import pandas as pd
import umap.umap_ as umap
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
import seaborn as sns

from src.dimension_reduction.common import decade_color_map, feature_list, get_ellipse, color_palette, genre_color_map
from src.helper.statistics_helper import most_common_genres


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





reducer = umap.UMAP()


wd = os.getcwd()
data = pd.read_csv('./../data/csv/song_features.csv')

song_features = data[
    feature_list
].values

scaled_song_data = StandardScaler().fit_transform(song_features)
embedding = reducer.fit_transform(scaled_song_data)

fig, ax = plt.subplots()
plt.scatter(
    embedding[:, 0],
    embedding[:, 1],
    s=50,
    marker='o',
    #c=[decade_to_color(x) for x in data.decade]
    #c=[color_palette[x] for x in data.decade.map(decade_color_map)],
    edgecolors='white',
)

add_labels_and_ellipses_for_genres(ax, data, embedding[:, 0], embedding[:, 1])


# plt.gca().set_aspect('equal', 'datalim')
plt.title('UMAP', fontsize=15)

plt.show()