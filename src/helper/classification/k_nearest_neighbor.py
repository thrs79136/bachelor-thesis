import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

from src.dimension_reduction.common import spotify_playlists_path


def k_nearest_neighbor():
    data = pd.read_csv(spotify_playlists_path)

    # Loading data
    irisData = load_iris()

    # Create feature and target arrays
    y = data.decade

    data = data.drop(['id', 'decade', 'artists', 'name'], axis=1)

    X = data.to_numpy()


    # Split into training and test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=11)

    knn.fit(X_train, y_train)

    # Predict on dataset which model has not seen before
    # print(knn.predict(X_test))
    print(knn.score(X_test, y_test))
