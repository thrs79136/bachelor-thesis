from cmath import sqrt
import random

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

from src.dimension_reduction.common import spotify_playlists_path, spotify_genres_playlists_path, feature_list_years, \
    feature_lists
from src.helper.file_helper import feature_file_path
from src.helper.genres import create_genres_df, genres_genres, transform_genre_string

import itertools

from src.helper.img.lineplot import lineplot_multiple_lines
from src.shared import shared


def knn_classification_all():
    knn_decade_ds1()
    knn_decade_ds2()
    knn_genre_ds1()


def knn_decade_ds1():
    knn_classification_dataframe(shared.mcgill_df, feature_lists['year'], 'decade', 'decade_ds1.jpg')


def knn_decade_ds2():
    pass
    # genre_groups
    # knn_classification_dataframe(shared.mcgill_df)
    # pass


def knn_genre_ds1():
    pass


def knn_classification_dataframe(dataframe, feature_list, classification_column, filename):

    X = dataframe[feature_list].to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    y = dataframe[classification_column]

    # Split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # TODO increase size
    neighbors = np.arange(1, 100)
    train_accuracy = np.empty(len(neighbors))
    test_accuracy = np.empty(len(neighbors))

    random_score = knn_random_value(y)


    # Loop over K values
    for i, k in enumerate(neighbors):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)

        # Compute training and test data accuracy
        train_accuracy[i] = knn.score(X_train, y_train)
        test_accuracy[i] = knn.score(X_test, y_test)


    # get best k value
    val, idx = max((val, idx) for (idx, val) in enumerate(test_accuracy))



    # TODO random assignment
    lineplot_multiple_lines(neighbors, [train_accuracy, test_accuracy],
                            ['Testdaten', 'RMSE bei zufälliger Zuordnung'], 'k', 'Genauigkeit', filename, 'hallo',
                            dot_coordinates=[[(neighbors[idx], val)]],
                            dot_legend=[f'Höchste Genauigkeit (p={val:.3f}, k={neighbors[idx]})'],
                            directory='knn/classification')


def knn_random_value(column):
    arr = column.values.tolist()
    random_prediction = [random.sample(arr, 1)[0] for _ in range(len(arr))]
    match = [i for i in range(len(arr)) if random_prediction[i] == arr[i]]
    return len(match)/len(arr)


def k_nearest_neighbor():
    data = pd.read_csv(spotify_playlists_path)

    # Create feature and target arrays
    # y = data.decade
    y = []
    for d in data.decade:
        if d < 1990:
            y.append(1)
        else:
            y.append(0)

    data = data.drop(['id', 'decade', 'artists', 'name'], axis=1)

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    # Split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    neighbors = np.arange(1, 20)
    train_accuracy = np.empty(len(neighbors))
    test_accuracy = np.empty(len(neighbors))

    # Loop over K values
    for i, k in enumerate(neighbors):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)

        # Compute training and test data accuracy
        train_accuracy[i] = knn.score(X_train, y_train)
        test_accuracy[i] = knn.score(X_test, y_test)

    fig, ax = plt.subplots()

    # Generate plot
    plt.plot(neighbors, test_accuracy, label='Trainingsdaten Genauigkeit')
    plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    plt.legend()
    plt.xlabel('n_neighbors')
    plt.ylabel('Accuracy')
    plt.show()
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/before_90s.png')


def knn_genre_mcgill():
    df = pd.read_csv(feature_file_path)
    genres_df = create_genres_df(df)

    for i in range(genres_df.shape[0]):
        #song.genre = transform_genre_string(song.genre)
        genres_df.iloc[i-1, genres_df.columns.get_loc('genre')] = transform_genre_string(genres_df.iloc[i-1, genres_df.columns.get_loc('genre')])

    k_nearest_neighbor_genre(genres_df, genres_genres, 'mcgillgenres.png', 'KNN mit Klassifizierung nach Musikrichtung (Datensatz 1)', ['decade', 'artist', 'genre'])


def knn_genre_spotify():
    df = pd.read_csv(spotify_genres_playlists_path)
    k_nearest_neighbor_genre(df, ['hiphop', 'pop', 'rock', 'blues', 'jazz', 'country'], 'spotify_genres.png', 'KNN mit Klassifizierung nach Musikrichtung (Datensatz 3)', ['id', 'artists', 'name', 'genre'])


def k_nearest_neighbor_genre(df, genres, filename, title, dropped_columns=[]):

    genre_to_int = {}
    for index, value in enumerate(genres):
        genre_to_int[value] = index

    y = [genre_to_int[genre] for genre in df.genre]

    data = df.drop(dropped_columns, axis=1)

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    # Split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    neighbors = np.arange(1, 25)
    train_accuracy = np.empty(len(neighbors))
    test_accuracy = np.empty(len(neighbors))

    # Loop over K values
    for i, k in enumerate(neighbors):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)

        # Compute training and test data accuracy
        train_accuracy[i] = knn.score(X_train, y_train)
        test_accuracy[i] = knn.score(X_test, y_test)

    fig, ax = plt.subplots()

    # Generate plot
    plt.plot(neighbors, test_accuracy, label='Trainingsdaten Genauigkeit')
    plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    plt.legend()
    plt.xlabel('k nächste Nachbarn')
    plt.ylabel('Genauigkeit')
    plt.show()
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/{filename}')


def k_nearest_neighbor_all_decades_all_features():
    k_nearest_neighbor_decade_all_features(True)


def k_nearest_neighbor_before_90s_all_features():
    k_nearest_neighbor_decade_all_features(False)

# spotify features, harmonic features, instruments, ...
def k_nearest_neighbor_decade_all_features(all_decades):
    data = pd.read_csv(feature_file_path)

    if all_decades:
        filename = 'decade_all_features_90s.png'
        y = data.decade
    else:
        filename = 'decade_all_features.png'
        y = []
        for d in data.decade:
            if d < 1990:
                y.append(1)
            else:
                y.append(0)

    data = data[data.columns.intersection(feature_list_years)]

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    # Split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    neighbors = np.arange(1, 25)
    train_accuracy = np.empty(len(neighbors))
    test_accuracy = np.empty(len(neighbors))

    # Loop over K values
    for i, k in enumerate(neighbors):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)

        # Compute training and test data accuracy
        train_accuracy[i] = knn.score(X_train, y_train)
        test_accuracy[i] = knn.score(X_test, y_test)

    fig, ax = plt.subplots()

    # Generate plot
    plt.plot(neighbors, test_accuracy, label='Trainingsdaten Genauigkeit')
    plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    plt.legend()
    plt.title('KNN mit Klassifizierung nach Zeitraum (Datensatz 1)')
    plt.xlabel('k')
    plt.ylabel('Genauigkeit')
    plt.show()
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/{filename}')

