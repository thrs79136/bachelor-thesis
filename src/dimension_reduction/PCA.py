import os
from collections import defaultdict

import numpy as np
import pandas as pd
import seaborn as sns

# create dataframe
from matplotlib import pyplot as plt
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.decomposition import PCA

from src.dimension_reduction.common import feature_list, color_palette, create_scatterplot_with_ellipses
from src.helper.file_helper import write_text_file
from src.helper.spotify_api import playlist_ids

path = os.getcwd()

dir = '../../data/img_old/plots/scatter_plots/dimension_reduction/pca'


#data = pd.read_csv(f'../../data/csv/years/spotify.csv')


data = pd.read_csv('../../data/csv/song_features.csv')

print(data.head())
print(data.shape)

data_dropped = data[
    feature_list
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

wt = range(pca_data.shape[0])
pca_df = pd.DataFrame(pca_data, index=[*wt], columns=labels)

decade_color_map = {1950: 0, 1960: 1, 1970: 2, 1980: 3, 1990: 4}
color_list = data['decade'].map(decade_color_map)

create_scatterplot_with_ellipses(data, pca_df.PC1.values, pca_df.PC2.values, dir, 'PCA', 'PC1 - {0}%'.format(per_var[0]), 'PC2 - {0}%'.format(per_var[1]))


file_content = ''
for i in range(2):
    loading_scores = pd.Series(pca.components_[i], index=feature_list)
    sorted_loading_scores = loading_scores.abs().sort_values(ascending=False)

    top_10_genes = sorted_loading_scores[0:10].index.values


    file_content += f'PCA{str(i+1)}\n{str(loading_scores[top_10_genes])}\n\n'
    write_text_file(dir + '/loading_scores.txt', file_content)