import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import svm, datasets
from sklearn import preprocessing

from src.dimension_reduction.common import spotify_playlists_path, mcgill_features_path, spotify_genres_playlists_path, \
    feature_lists
from src.helper.genres import transform_genre_string, create_genres_df
from src.helper.img.barplot import create_barplot
from src.shared import shared
from src.shared.shared import non_musical_features


def svm_all():
    svm_genre_mcgill()
    svm_decade_mcgill()


def svm_decade_mcgill():
    feature_list = [feature.feature_id for feature in shared.song_features_dict.values() if not feature.is_nominal and feature.feature_id not in non_musical_features and not feature.is_sentiment_feature]
    my_svm(mcgill_features_path, 'decade', feature_lists['year'], 'Klassifizierung nach Jahrzehnt (Datensatz 1)', 'decades.jpg')


def svm_genre_mcgill():
    df = shared.sentiment_df
    genres_df = df[~df['genre_groups'].isnull()]

    svm_dataframe(genres_df, 'genre_groups', feature_lists['genre'], 'Klassifizierung nach Musikrichtung (Datensatz 1)', 'genre.jpg')


# def svm_genre_spotify():
#     my_svm(spotify_genres_playlists_path, 'genre', ['id', 'artists', 'name', 'genre'], 'Klassifizierung nach Musikrichtung (Datensatz 2)', 'genres_dataset2.png')


def svm_decade_spotify():
    my_svm(spotify_playlists_path, 'decade', ['id', 'artists', 'name', 'decade', 'time_signature'], 'Klassifizierung nach Jahrzehnt (Datensatz 2)', 'decades_dataset3.png')


def my_svm(dataframe_path, classifier_column, feature_list, title, filename):
    data = pd.read_csv(dataframe_path)
    svm_dataframe(data, classifier_column, feature_list, title, filename)


def svm_dataframe(dataframe, classifier_column, feature_list, title, filename):
    y = dataframe[classifier_column]

    feature_list = shared.song_features_dict.values()
    feature_list = [f.feature_id for f in feature_list if f.feature_id not in non_musical_features and not f.is_nominal and not f.is_sentiment_feature]

    data = dataframe[feature_list]

    X = data.to_numpy()
    scaler = preprocessing.StandardScaler().fit(X)
    X = scaler.transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)

    # linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(X_train, y_train)
    # rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo').fit(X_train, y_train)
    # poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo').fit(X_train, y_train)
    # sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo').fit(X_train, y_train)
    #
    # accuracy_lin = linear.score(X_test, y_test)
    # accuracy_poly = poly.score(X_test, y_test)
    # accuracy_rbf = rbf.score(X_test, y_test)
    # accuracy_sig = sig.score(X_test, y_test)

    linear = svm.SVC(kernel='linear', C=1, decision_function_shape='ovo')
    rbf = svm.SVC(kernel='rbf', gamma=1, C=1, decision_function_shape='ovo')
    poly = svm.SVC(kernel='poly', degree=3, C=1, decision_function_shape='ovo')
    sig = svm.SVC(kernel='sigmoid', C=1, decision_function_shape='ovo')

    accuracy_lin = cross_val_score(linear, X, y, cv=10).mean()
    accuracy_poly = cross_val_score(rbf, X, y, cv=10).mean()
    accuracy_rbf = cross_val_score(poly, X, y, cv=10).mean()
    accuracy_sig = cross_val_score(sig, X, y, cv=10).mean()



    accuracies = [accuracy_lin, accuracy_poly, accuracy_rbf, accuracy_sig]

    create_barplot(accuracies, ['Linearer\nKernel', 'Polynomieller\nKernel', 'Radialer-Basis-\nKernel', 'Sigmoid-\nKernel'], 'Genauigkeit',
                   filename, '', directory='svm', ylim=1, figsize=(4.8, 3.599))


