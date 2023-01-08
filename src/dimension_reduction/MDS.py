import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.manifold import MDS

from src.dimension_reduction.common import feature_list, create_scatterplot_with_ellipses, spotify_playlists_path, \
    feature_lists
from src.shared import shared
from src.shared.shared import non_musical_features


def create_mds_plots():
    create_mds_plot('year')
    create_mds_plot('genre_groups')


def create_mds_plot(colored_feature):

    df = shared.mcgill_df
    if colored_feature == 'genre_groups':
        df = shared.sentiment_df

    df_filtered = df[~df[colored_feature].isnull()]
    df = df_filtered[feature_lists[colored_feature]].values

    scaled_df = preprocessing.scale(df)

    mds = MDS(random_state=42, normalized_stress='auto')
    mds_df = mds.fit_transform(scaled_df)

    directory = f'../data/img/plots/scatter_plots/dimension_reduction/mds'
    create_scatterplot_with_ellipses(df_filtered, mds_df[:,0], mds_df[:,1], colored_feature, directory, 'MDS', 'X', 'Y')
