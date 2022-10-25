import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

from src.dimension_reduction.common import spotify_playlists_path, spotify_genres_playlists_path, feature_list_years
from src.helper.file_helper import feature_file_path
from src.helper.genres import create_genres_df, genres_genres, transform_genre_string

import itertools

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

