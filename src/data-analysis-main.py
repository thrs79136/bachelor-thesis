import pickle

from src.dimension_reduction.MDS import create_mds_plot, create_mds_plots
from src.dimension_reduction.PCA import create_pca_plot, create_pca_plots
from src.dimension_reduction.t_SNE import create_tsne_plot
from src.helper.absolute_surprise import init_progressions_dict
from src.helper.absolute_surprise_chords import init_chords_dict
from src.helper.artists import analyze_artists_over_time, analyze_feature_median_deviation
from src.helper.file_helper import get_dataset_1, save_all_features_to_csv, get_songs, get_songs_from_binary_file, \
    save_median_feature_csv
from src.helper.img.barplot import create_grouped_barplot, create_stacked_barplot
from src.helper.img.boxplot import create_boxplot
from src.helper.img.lineplot import stacked_area_plot
from src.helper.img.parallel_coordinates import create_parallel_coordinates
from src.helper.img.scatterplot import create_scatter_plot
from src.helper.knn.k_nearest_neighbor import k_nearest_neighbor_all_decades_all_features, knn_classification_all
from src.helper.knn.knn_regression import knn_regression_all
from src.helper.statistics.correlation_matrix import create_correlation_matrix_plt
from src.helper.statistics.feature_analyzer import analyze_all_features, compare_features_among_genres, \
    create_correlation_matrix
# from src.helper.statistics.sentiment_analysis import sentiment_analysis_init, \
#     sentiment_analysis_emotions, sentiment_analysis_neg_pos
from src.helper.statistics.genres import get_most_common_genres, genres_stacked_area_plot
from src.helper.statistics.multivariate_regression import multiple_regression, multiple_regression_all
from src.helper.statistics.year_feature_median import get_median, draw_feature_line_plot, draw_feature_line_plots
from src.helper.svm.svm import svm_all
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



# songs = get_songs('../data/songs-finished.csv')
# songs = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
# init_progressions_dict(songs)
# init_chords_dict(songs)
# save_median_feature_csv(songs, shared.song_features_dict.keys())

# songs_with_duplicates = get_songs('../data/songs.csv')

songs = get_songs_from_binary_file(bin_file)


# songs = get_dataset_1()
init(songs)
# save_feature_csv(songs)
save_median_feature_csv(songs, shared.song_features_dict.keys())


# result_dict = analyze_all_features(redraw_plots=True)
# for key, value in result_dict.items():
#     print(key)
#     print(', '.join(f"'{feature.feature.feature_id}'" for feature in value))
#     # print(', '.join(feature.feature.feature_id.replace('_', '\_') for feature in value))

# exit()
#print([feature.feature.feature_id for feature in result_dict['genre']])
# exit()
# genres_stacked_area_plot()

# draw_feature_line_plots()
# get_most_common_genres()
# analyze_feature_median_deviation()


#create_pca_plots()
#create_mds_plots()
create_parallel_coordinates()

# create_correlation_matrix_plt()
# multiple_regression_all()
# classification
# knn_classification_all()

# # regression
# knn_regression_all()

# svm_all()
exit()


# sentiment_analysis_init()
# for song in songs:
#     sentiment_analysis_emotions(song)
