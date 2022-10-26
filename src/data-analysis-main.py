import pickle

from src.helper.absolute_surprise import init_progressions_dict
from src.helper.file_helper import get_dataset_1, save_all_features_to_csv
from src.helper.statistics.sentiment_analysis import sentiment_analysis_init, \
    sentiment_analysis_emotions, sentiment_analysis_neg_pos
from src.shared.song_features import init_song_features

bin_file = '../data/songs.pickle'


def init(songs):
    init_progressions_dict(songs)
    init_song_features()


def save_feature_csv(songs):
    sentiment_analysis_init()
    for song in songs:
        sentiment_analysis_emotions(song)
        sentiment_analysis_neg_pos(song)

    save_all_features_to_csv(songs)


songs = get_dataset_1()

init(songs)
# save_feature_csv(songs)




# TODO
#  * create pickle in dataset-creation.py
#  * create feature csv
#  * analyze feature correlation

# sentiment_analysis_init()
# for song in songs:
#     sentiment_analysis_emotions(song)
