import pickle
import shutil


from src.helper.artists import analyze_feature_median_deviation
from src.helper.file_helper import get_dataset_1, save_all_features_to_csv, get_songs, get_songs_from_binary_file, \
    save_median_feature_csv
from src.helper.statistics.feature_analyzer import analyze_all_features, compare_features_among_genres, \
    create_correlation_matrix

from src.models.mcgill_songdata.pause import Pause
from src.shared import shared
from src.shared.shared import init_song_features

bin_file = '../data/songs.pickle'


def init(songs):
    init_progressions_dict(songs)
    init_song_features()

# TODO uncomment
def save_feature_csv(songs):
    # sentiment_analysis_init()
    # for song in songs:
    #     print(song.mcgill_billboard_id)
    #     sentiment_analysis_emotions(song)
    #     sentiment_analysis_neg_pos(song)

    # with open(bin_file, 'wb') as file:
    #     pickle.dump(songs, file)

    save_all_features_to_csv(songs)


def get_usb_stick_files():
    all_ids = [feature.latex_id for feature in shared.song_features_dict.values() if feature.latex_id != '']
    all_features = [feature for feature in shared.song_features_dict.values() if feature.latex_id != '']

    genres = '1/box_plots/2/box_plots,3/box_plots/4/box_plots,7/box_plots/12/box_plots},{13/box_plots/15/box_plots/21/box_plots,25/box_plots/30/box_plots/40/box_plots'
    correlation_path = '../data/img/plots/box_plots/correlation/genre'
    correlation_path_nominal = '../data/img/plots/bar_plots/nominal_correlation'

    genres_ids = genres.replace('box_plots', '').replace('/', ',').replace('}', '').replace('{', '').replace(',,', ',')
    ids = [int(id) for id in genres_ids.split(',') if id != '']

    features_to_copy = [feature for feature in all_features if feature.latex_id not in ids]

    dest_path = 'C:/Users/thrss/Documents/1Stick'

    feature_name = 'genre'

    for feature in features_to_copy:

        filename = f'{feature_name}_{feature.latex_id}.jpg'
        if feature_name == 'genre' and feature.is_nominal:
            filename = f'{feature.latex_id}.jpg'

        filepath = correlation_path if not feature.is_nominal else correlation_path_nominal
        src = f'{filepath}/{filename}'
        shutil.copy(src, dest_path)

    x = 42


# get_usb_stick_files()
# exit()

#songs = get_songs('../data/songs-finished.csv')
#songs = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]

# songs_with_duplicates = get_songs('../data/songs.csv')

#songs = get_songs_from_binary_file(bin_file)


# songs = get_dataset_1()
#init(songs)
# save_feature_csv(songs)
#save_median_feature_csv(songs, shared.song_features_dict.keys())


result_dict = analyze_all_features(redraw_plots=True)

# for key, value in result_dict.items():
#     print(key)
#     # print(', '.join(f"'{feature.feature.feature_id}'" for feature in value))
#     #print(', '.join(feature.feature.feature_id.replace('_', '\_') for feature in value))
#     features = [test_result.feature for test_result in value]
#
#     result_str = '{'
#     for i, feature in enumerate(features):
#
#         if key != 'genre':
#             directory = 'box_plots' if feature.is_nominal else 'scatter_plots'
#         else:
#             directory = 'bar_plots' if feature.is_nominal else 'box_plots'
#
#         result_str += f'{feature.latex_id}/{directory}'
#
#         if i == len(features) - 1:
#             result_str += '}'
#             break
#
#         if i % 2 == 1:
#             if (i + 1) % 6 == 0:
#                 result_str += '},{'
#             else:
#                 result_str += ','
#         else:
#             result_str += '/'
#
#     print(result_str)
#
#     x = 42

# print([feature.feature.feature_id for feature in result_dict['genre']])
# genres_stacked_area_plot()

# draw_feature_line_plots()
# get_most_common_genres()
analyze_feature_median_deviation()


# create_pca_plots()
# create_mds_plots()
# ordered_feature_ids = ['acousticness', 'v_to_i', 'root_distances', 'bass_distances', 'major_chords', 'tonic_chords',
#                        'seventh_chords', 'circle_of_fifths', 'circle_of_fifths_max', 'different_notes',
#                        'different_chords', 'different_progressions', 'minor_chords', 'duration_ms',
#                        'different_sections', 'chorus_repetitions', 'danceability', 'energy', 'neither_chords',
#                        'non_triad_chords']
#
# features = [shared.song_features_dict[f] for f in ordered_feature_ids]

# create_correlation_matrix()
# create_parallel_coordinates()

# create_correlation_matrix_plt()
# multiple_regression_all()
# classification
# knn_classification_all()

# # regression
# knn_regression_all()

# svm_all()
exit()
