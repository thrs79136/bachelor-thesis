import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.manifold import MDS

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

data = pd.read_csv('../../data/csv/song_features.csv')


song_features = data[
    feature_list1
].values

mds = MDS(n_components=2)
mds.fit_transform(song_features)

embedding = mds.embedding_

plt.scatter(mds.embedding_[:,0], mds.embedding_[:,1],
            c=[sns.cubehelix_palette(start=.5, rot=-.75)[x] for x in data.decade.map({1950:0, 1960:1, 1970:2, 1980:3, 1990:4})])
plt.title('MDS Plot')

plt.show()
