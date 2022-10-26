import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.manifold import MDS

from src.dimension_reduction.common import feature_list, create_scatterplot_with_ellipses, spotify_playlists_path, \
    get_data

data = pd.read_csv('../../data/csv/song_features.csv')
#data = pd.read_csv(spotify_playlists_path)
dir = '../../data/img_old/plots/scatter_plots/dimension_reduction/MDS'


song_features = get_data()

mds = MDS(n_components=2)
mds.fit_transform(song_features)

embedding = mds.embedding_

create_scatterplot_with_ellipses(data, mds.embedding_[:,0], mds.embedding_[:,1], dir, 'MDS', 'X', 'Y')
#
# plt.scatter(mds.embedding_[:,0], mds.embedding_[:,1],
#             c=[sns.cubehelix_palette(start=.5, rot=-.75)[x] for x in data.decade.map({1950:0, 1960:1, 1970:2, 1980:3, 1990:4})])
# plt.title('MDS Plot')
#
# plt.show()
