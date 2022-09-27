import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

from src.dimension_reduction.common import spotify_playlists_path, spotify_genres_playlists_path, feature_list_years
from src.helper.file_helper import feature_file_path


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

def k_nearest_neighbor_genre():
    data = pd.read_csv(spotify_genres_playlists_path)

    # Create feature and target arrays
    genre_to_int = {
        'hiphop': 0,
        'pop': 1,
        'rock': 2,
        'blues': 3,
        'jazz': 4,
        'country': 5
    }

    y = [genre_to_int[genre] for genre in data.genre]
    # y = data.genre

    # for d in data.decade:
    #     if d < 1990:
    #         y.append(1)
    #     else:
    #         y.append(0)

    data = data.drop(['id', 'artists', 'name', 'genre'], axis=1)

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
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/genres.png')

def k_nearest_neighbor_decade_all_features():
    data = pd.read_csv(feature_file_path)

    # y = data.decade
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
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/decade_all_features_90s.png')

