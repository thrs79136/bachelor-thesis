import math
import pickle
import random
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

from src.dimension_reduction.common import feature_list_years, feature_list_chart_pos, feature_list_spotify_popularity, \
    feature_lists, audio_feature_keys
from src.helper.file_helper import feature_file_path
from sklearn.model_selection import train_test_split

from sklearn import neighbors, preprocessing
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

from src.helper.img.lineplot import lineplot_multiple_lines
from src.shared import shared
from src.shared.shared import non_musical_features


def knn_regression_all():

    knn_regression_spotify_popularity_ds1()
    # knn_regression_spotify_popularity_ds2()
    knn_regression_chart_pos_ds1()
    knn_regression_year_ds1()

def knn_regression_spotify_popularity_ds1():
    knn_regression('spotify_popularity', 'Vorhersage der Spotify Popularity mittels KNN-Regression (Datensatz 1)', 'knn_regression_popularity_ds1.jpg', True)


def knn_regression_spotify_popularity_ds2():
    knn_regression_dataframe(shared.spotify_year_df, 'spotify_popularity', audio_feature_keys , 'Vorhersage der Spotify Popularity mittels KNN-Regression (Datensatz 2)', 'knn_regression_popularity_ds2.jpg', True)


def knn_regression_chart_pos_ds1():
    knn_regression('chart_pos', 'Vorhersage der höchsten Chartposition mittels KNN-Regression', 'knn_regression_chart_pos_ds1_m.jpg', True)


def knn_regression_year_ds1():
    knn_regression('year', 'Vorhersage des Jahres mittels KNN-Regression', 'knn_regression_year_ds1_m.jpg', True)

def knn_regression_year_ds1_balanced():
    data = pd.read_csv(feature_file_path)
    gb = data.groupby('year')
    res_dataframes = [gb.get_group(x) for x in gb.groups]
    min_song_count = min(x.shape[0] for x in res_dataframes)

    balanced_dfs = [df.head(min_song_count) for df in res_dataframes]
    merged_df = pd.concat(balanced_dfs)

    knn_regression_dataframe(merged_df, 'year', feature_list_years, 'Vorhersage des Jahres mittels KNN-Regression', 'knn_regression_year_ds1_balanced.jpg')


# predict spotify position, chart position and year
def knn_regression(column, title, filename, use_mean_instead_of_rmse=False):
    feature_list = feature_lists[column]
    data = shared.sentiment_df

    knn_regression_dataframe(data, column, feature_list, title, filename, use_mean_instead_of_rmse)


def knn_regression_dataframe(df, column, feature_list, title, filename, use_mean_instead_of_rmse=False):
    data = df.sample(frac=1)

    Y = data[column]

    feature_list = shared.song_features_dict.values()
    feature_list = [f.feature_id for f in feature_list if f.feature_id not in non_musical_features and not f.is_nominal and not f.is_sentiment_feature]

    data = data[feature_list]

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    max_k = len(data) - math.ceil(len(data)/10)

    X_subsets = np.array_split(X, 10)
    Y_subsets = np.array_split(Y, 10)


    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.1, random_state=42)

    neighbors = np.arange(1, max_k)
    # test_accuracy = np.empty(len(neighbors))

    rmse_values_cv = []

    for i, k in enumerate(neighbors):
        print(k)
        rmse_values = []
        for subset_index in range(len(X_subsets)):

            knn = KNeighborsRegressor(n_neighbors=k)

            X_train = [j for index, k in enumerate(X_subsets) for j in k if index != subset_index]
            y_train = [j for index, k in enumerate(Y_subsets) for j in k if index != subset_index]
            X_test = X_subsets[subset_index]
            y_test = Y_subsets[subset_index]

            knn.fit(X_train, y_train)

            # make prediction on test set
            pred = knn.predict(X_test)

            error = sqrt(mean_squared_error(y_test, pred))
            rmse_values.append(error)
        rmse_values_cv.append(np.mean(rmse_values))



    pickle_file = f'../data/{column}_reg.pickle'
    with open(pickle_file, 'wb') as file:
        pickle.dump(rmse_values_cv, file)
    # with open(pickle_file, 'rb') as file2:
    #     rmse_values_cv = pickle.load(file2)
    print(f'saved pickle for {column}')

    val, idx = min((val, idx) for (idx, val) in enumerate(rmse_values_cv))
    random_assignment_rmse = knn_regression_random_values(Y)
    # title = f'Vorhersage von {shared.song_features_dict[column].display_name} über KNN-Regression'
    lineplot_multiple_lines(neighbors, [rmse_values_cv, [random_assignment_rmse] * len(neighbors)],
                            ['Testdaten', 'RMSE bei zufälliger Zuordnung'], 'k', 'RMSE', f'{column}.jpg', '',
                            dot_coordinates=[[(neighbors[idx],val)]], dot_legend=[f'Minimaler RMSE (k={neighbors[idx]}, RMSE={val:.3f})'],
                            directory='knn/regression', figsize=(4.8, 3.599))

    return
    fig, ax = plt.subplots()

    # lineplot_multiple_lines(neighbors, [train_accuracy, ])

    # Generate plot
    plt.plot(neighbors, test_accuracy)

    if not use_mean_instead_of_rmse:
        random_assignment_rmse = knn_regression_random_values(Y)
        plt.plot(neighbors, [random_assignment_rmse] * len(neighbors))
    # plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    plt.title(title)
    plt.xlabel('k')
    if use_mean_instead_of_rmse:
        plt.ylabel('Durchschnittlicher Betrag des Fehlers')
    else:
        plt.ylabel('RMSE')
    plt.show()

    path = '../data/img/plots/line_plots/knn/regression'
    Path(path).mkdir(parents=True, exist_ok=True)
    fig.savefig(f'{path}/{filename}')


# assign random values based on distribution
def knn_regression_random_values(column):
    arr = column.values.tolist()
    random_prediction = [random.sample(arr, 1) for _ in range(len(arr))]
    return sqrt(mean_squared_error(arr, random_prediction))
