import pickle

from src.dimension_reduction.PCA import create_pca_plot
from src.dimension_reduction.t_SNE import create_tsne_plot
from src.helper.absolute_surprise import init_progressions_dict
from src.helper.artists import analyze_artists_over_time
from src.helper.file_helper import get_dataset_1, save_all_features_to_csv, get_songs, get_songs_from_binary_file
from src.helper.img.barplot import create_grouped_barplot, create_stacked_barplot
from src.helper.img.boxplot import create_boxplot
from src.helper.img.parallel_coordinates import create_parallel_coordinates
from src.helper.img.scatterplot import create_scatter_plot
from src.helper.statistics.feature_analyzer import analyze_all_features, compare_features_among_genres, \
    create_correlation_matrix
# from src.helper.statistics.sentiment_analysis import sentiment_analysis_init, \
#     sentiment_analysis_emotions, sentiment_analysis_neg_pos
from src.helper.statistics.genres import get_most_common_genres
from src.helper.statistics.year_feature_median import get_median, draw_feature_line_plot, draw_feature_line_plots
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
#songs = [song for song in songs_all if song.spotify_song_data.audio_features_dictionary is not None]
# songs_with_duplicates = get_songs('../data/songs.csv')

# songs = get_songs_from_binary_file(bin_file)

#songs = get_dataset_1()
#init(songs)
#save_feature_csv(songs)
result_dict = analyze_all_features(redraw_plots=False)
print([feature.feature.feature_id for feature in result_dict['year']])
# draw_feature_line_plots()
# get_most_common_genres()
# analyze_artists_over_time()

# create_correlation_matrix([result.feature for result in result_dict['year']])
#create_pca_plot()
create_tsne_plot()
#create_parallel_coordinates(result_dict)
exit()


# sentiment_analysis_init()
# for song in songs:
#     sentiment_analysis_emotions(song)
