import pandas as pd
from mlxtend.regressor import LinearRegression
from sklearn import linear_model, preprocessing
from mlxtend.feature_selection import SequentialFeatureSelector as sfs

from sklearn import datasets ## imports datasets from scikit-learn

from src.dimension_reduction.common import feature_lists
from src.shared import shared
from src.shared.shared import non_y_axis_features


def multiple_regression_all():
    multiple_regression('year')
    multiple_regression('chart_pos')
    multiple_regression('spotify_popularity')


def multiple_regression(target):

    print(target)
    df = shared.mcgill_df

    final_features = []

    features = list(shared.song_features_dict.values())
    features_for_correlation_matrix = [feature.feature_id for feature in features if not feature.is_nominal and feature.feature_id not in non_y_axis_features and not feature.is_sentiment_feature]
    binary_features = [feature.feature_id for feature in features if feature.is_boolean]
    nominal_features = [feature.feature_id for feature in features if feature.is_nominal and not feature.is_boolean and feature.feature_id != 'genre']

    # use nomianl features as binary features
    for feature in nominal_features:
        groupkeys = df.groupby(feature).groups.keys()
        for key in groupkeys:
            binary_features.append(f'{feature}_{key}')
            df.loc[(df[feature] == key), f'{feature}_{key}'] = 1
            df.loc[(df[feature] != key), f'{feature}_{key}'] = 0

    features = features_for_correlation_matrix + binary_features
    X = df[features].to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    y = df[target].values

    lm = linear_model.LinearRegression()
    model = lm.fit(X, y)

    predictions = lm.predict(X)

    print(f'score = {lm.score(X,y):.3f}')
    # print(lm.coef_)
    # print(lm.intercept_)

    # year
    # score = 0.922
    # chart_pos
    # score = 0.109
    # spotify_popularity
    # score = 0.166

    # year
    # score = 0.530
    # chart_pos
    # score = 0.085
    # spotify_popularity
    # score = 0.145

    # year
    # score = 0.551
    # chart_pos
    # score = 0.093
    # spotify_popularity
    # score = 0.149
