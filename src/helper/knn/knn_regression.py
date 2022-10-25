import random

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

from src.dimension_reduction.common import feature_list_years, feature_list_chart_pos, feature_list_spotify_popularity
from src.helper.file_helper import feature_file_path
from sklearn.model_selection import train_test_split

from sklearn import neighbors, preprocessing
from sklearn.metrics import mean_squared_error
from math import sqrt
import matplotlib.pyplot as plt

def knn_regression_spotify_popularity_ds1():
    knn_regression('spotify_popularity', feature_list_spotify_popularity, 'Vorhersage der Spotify Popularity mittels KNN-Regression', 'knn_regression_popularity_ds1_m.png', True)


def knn_regression_chart_pos_ds1():
    knn_regression('chart_pos', feature_list_chart_pos, 'Vorhersage der höchsten Chartposition mittels KNN-Regression', 'knn_regression_chart_pos_ds1_m.png', True)


def knn_regression_year_ds1():
    knn_regression('year', feature_list_years, 'Vorhersage des Jahres mittels KNN-Regression', 'knn_regression_year_ds1_m.png', True)

def knn_regression_year_ds1_balanced():
    data = pd.read_csv(feature_file_path)
    gb = data.groupby('year')
    res_dataframes = [gb.get_group(x) for x in gb.groups]
    min_song_count = min(x.shape[0] for x in res_dataframes)

    balanced_dfs = [df.head(min_song_count) for df in res_dataframes]
    merged_df = pd.concat(balanced_dfs)

    knn_regression_dataframe(merged_df, 'year', feature_list_years, 'Vorhersage des Jahres mittels KNN-Regression', 'knn_regression_year_ds1_balanced.png')

# TODO get spotify popularity for dataset 3

# predict spotify position, chart position and year
def knn_regression(column, feature_list, title, filename, use_mean_instead_of_rmse=False):
    data = pd.read_csv(feature_file_path)
    knn_regression_dataframe(data, column, feature_list, title, filename, use_mean_instead_of_rmse)


def knn_regression_dataframe(data, column, feature_list, title, filename, use_mean_instead_of_rmse=False):
    Y = data[column]

    data = data[data.columns.intersection(feature_list)]

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)


    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42)

    neighbors = np.arange(1, 25)
    test_accuracy = np.empty(len(neighbors))

    for i, k in enumerate(neighbors):
        knn = KNeighborsRegressor(n_neighbors=k)
        knn.fit(X_train, y_train)

        # make prediction on test set
        pred = knn.predict(X_test)
        if use_mean_instead_of_rmse:
            differences = [abs(val-pred[i]) for i, val in enumerate(y_test.values.tolist())]
            error = np.mean(differences)
        else:
            error = sqrt(mean_squared_error(y_test, pred))
        test_accuracy[i] = error


    fig, ax = plt.subplots()

    # Generate plot
    plt.plot(neighbors, test_accuracy)

    if not use_mean_instead_of_rmse:
        random_assignment_rmse = knn_regression_random_values(Y)
        plt.plot(neighbors, [random_assignment_rmse] * len(neighbors))
    # plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    plt.title(title)
    plt.xlabel('k')
    if use_mean_instead_of_rmse:
        plt.ylabel('Mean error')
    else:
        plt.ylabel('RMSE')
    plt.show()
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/{filename}')

# assign random values based on distribution
def knn_regression_random_values(column):
    arr = column.values.tolist()
    random_prediction = [random.sample(arr, 1) for _ in range(len(arr))]
    return sqrt(mean_squared_error(arr, random_prediction))
