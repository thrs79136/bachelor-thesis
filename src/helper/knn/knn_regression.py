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


# predict spotify position, chart position and year
def knn_regression():
    data = pd.read_csv(feature_file_path)
    Y = data['spotify_popularity']

    data = data[data.columns.intersection(feature_list_spotify_popularity)]

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
        error = sqrt(mean_squared_error(y_test, pred))
        test_accuracy[i] = error


    fig, ax = plt.subplots()

    # Generate plot
    plt.plot(neighbors, test_accuracy)
    # plt.plot(neighbors, train_accuracy, label='Testdaten Genauigkeit')

    plt.title('Vorhersage der Spotify Popularity mittels KNN-Regression')
    plt.xlabel('k')
    plt.ylabel('RMSE')
    plt.show()
    fig.savefig(f'../data/img/plots/k_nearest_neighbor/knn_regression_popularity_ds1.png')



