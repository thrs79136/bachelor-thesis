import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm, datasets
from sklearn import preprocessing

from src.dimension_reduction.common import spotify_playlists_path, mcgill_features_path, spotify_genres_playlists_path
from src.helper.genres import transform_genre_string, create_genres_df
from src.helper.img.barplot import create_barplot


def svm_decade_mcgill():
    my_svm(mcgill_features_path, 'decade', ['decade', 'artist', 'genre'], 'Klassifizierung nach Jahrzehnt (Datensatz 1)', 'decades_dataset1.png')


def svm_genre_mcgill():
    data = pd.read_csv(mcgill_features_path)
    genres_df = create_genres_df(data)

    for i in range(genres_df.shape[0]):
        genres_df.iloc[i-1, genres_df.columns.get_loc('genre')] = transform_genre_string(genres_df.iloc[i-1, genres_df.columns.get_loc('genre')])

    svm_dataframe(genres_df, 'genre', ['decade', 'artist', 'genre'], 'Klassifizierung nach Musikrichtung (Datensatz 1)', 'genres_dataset1.png')


def svm_genre_spotify():
    my_svm(spotify_genres_playlists_path, 'genre', ['id', 'artists', 'name', 'genre'], 'Klassifizierung nach Musikrichtung (Datensatz 2)', 'genres_dataset2.png')


def svm_decade_spotify():
    my_svm(spotify_playlists_path, 'decade', ['id', 'artists', 'name', 'decade', 'time_signature'], 'Klassifizierung nach Jahrzehnt (Datensatz 3)', 'decades_dataset3.png')


def my_svm(dataframe_path, classifier_column, dropped_columns, title, filename):
    data = pd.read_csv(dataframe_path)
    svm_dataframe(data, classifier_column, dropped_columns, title, filename)


def svm_dataframe(dataframe, classifier_column, dropped_columns, title, filename):
    y = dataframe[classifier_column]

    data = dataframe.drop(dropped_columns + [classifier_column], axis=1)

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(X_train, y_train)
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo').fit(X_train, y_train)
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo').fit(X_train, y_train)
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo').fit(X_train, y_train)

    accuracy_lin = linear.score(X_test, y_test)
    accuracy_poly = poly.score(X_test, y_test)
    accuracy_rbf = rbf.score(X_test, y_test)
    accuracy_sig = sig.score(X_test, y_test)

    accuracies = [accuracy_lin, accuracy_poly, accuracy_rbf, accuracy_sig]

    create_barplot(accuracies, ['Linear\nKernel', 'Polynomial\nKernel', 'Radial Basis\nKernel', 'Sigmoid\nKernel'],
                   filename, title)


