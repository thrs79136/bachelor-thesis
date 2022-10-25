from typing import List

from src.helper.file_helper import get_songs_from_binary_file, get_dataset_1, save_feature_csv
from src.helper.statistics.sentiment_analysis import startsentiment_analysis, sentiment_analysis_init, \
    sentiment_analysis_emotions
from src.models.song import Song
from src.shared import song_features

bin_file = '../data/songs.pickle'

songs = get_dataset_1()
save_feature_csv(songs, list(song_features.song_features_dict.keys()))


# TODO
#  * create pickle in dataset-creation.py
#  * create feature csv
#  * analyze feature correlation

save_feature_csv(songs, list(song_features.song_features_dict.keys()))

sentiment_analysis_init()
for song in songs:
    sentiment_analysis_emotions(song)
