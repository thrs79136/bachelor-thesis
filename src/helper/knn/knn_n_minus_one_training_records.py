import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier

from src.dimension_reduction.common import spotify_genres_playlists_path, spotify_playlists_path
from src.helper.file_helper import feature_file_path
from src.helper.genres import create_genres_df, genres_genres, transform_genre_string


def knn_n_minus_one_mcgill_decade():
    df = pd.read_csv(feature_file_path)
    knn_n_minus_one_training_records(df, 'decade', 'decade_mcgill.png', 'KNN mit Klassifizierung nach Jahrzehnt (Datensatz 1)', ['decade', 'artist', 'genre'])

def knn_n_minus_one_mcgill_genre():
    df = pd.read_csv(feature_file_path)
    genres_df = create_genres_df(df)

    for i in range(genres_df.shape[0]):
        genres_df.iloc[i-1, genres_df.columns.get_loc('genre')] = transform_genre_string(genres_df.iloc[i-1, genres_df.columns.get_loc('genre')])

    knn_n_minus_one_training_records(genres_df, 'genre', 'mcgillgenres.png', 'KNN mit Klassifizierung nach Musikrichtung (Datensatz 1)', ['decade', 'artist', 'genre'])


def knn_n_minus_one_genre_spotify():
    df = pd.read_csv(spotify_genres_playlists_path)
    knn_n_minus_one_training_records(df, 'genre', 'spotify_genres.png', 'KNN mit Klassifizierung nach Musikrichtung (Datensatz 3)', ['id', 'artists', 'name', 'genre'])


def knn_n_minus_one_decade_spotify():
    df = pd.read_csv(spotify_playlists_path)
    knn_n_minus_one_training_records(df, 'decade', 'spotify_decades.png', 'KNN mit Klassifizierung nach Jahrzehnt (Datensatz 2)', ['id', 'artists', 'name', 'decade', 'time_signature'])


def knn_n_minus_one_training_records(data, classified_column, filename, title, dropped_columns=[]):

    y = data[classified_column].values

    data = data.drop(dropped_columns, axis=1)

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    training_sets_X = []
    training_sets_Y = []

    test_sets_X = []
    test_sets_Y = []

    for i in range(len(data.index)):
        training_sets_X.append(np.concatenate((X[:i], X[i+1:])))
        training_sets_Y.append(np.concatenate([y[:i], y[i+1:]]))

        test_sets_X.append([np.array(X[i])])
        test_sets_Y.append([np.array(y[i])])


    neighbors = np.arange(1, 11)
    means = []

    for i, k in enumerate(neighbors):
        print(i, k)
        train_accuracy = []
        test_accuracy = []
        for i in range(len(training_sets_X)):
            X_train = training_sets_X[i]
            y_train = training_sets_Y[i]

            X_test = test_sets_X[i]
            y_test = test_sets_Y[i]

            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X_train, y_train)

            # Compute training and test data accuracy
            train_accuracy.append(knn.score(X_train, y_train))
            test_accuracy.append(knn.score(X_test, y_test))

        mean = np.mean(test_accuracy)
        means.append(mean)

    print(means)
    fig, ax = plt.subplots()

    # Generate plot
    plt.plot(neighbors, means, label='Trainingsdaten Genauigkeit')
    # plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    # plt.legend()
    plt.ylim(0,1.05)
    plt.title(title)
    plt.xlabel('k')
    plt.ylabel('Durchschnittliche Genauigkeit')
    plt.show()
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/n_minus_one/{filename}')



