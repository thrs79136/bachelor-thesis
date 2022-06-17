
import pickle
import statistics
from collections import defaultdict
from typing import List

from src.helper.absolute_surprise import prog_prob, split_by_quartiles, get_quartile_surprises, \
    find_linear_contributions
from src.helper.cadences import analyze_cadences
from src.helper.chord_progressions import identify_chord_progressions, find_progressions, find_song_progressions
from src.helper.file_helper import get_songs, get_songs_from_binary_file
from src.helper.statistics_helper import get_median_chart_positions, create_bar_plot, get_genres_dictionary, \
    most_common_genres, create_key_table, create_mode_table, create_genre_scatter_plots, t_test
from src.models.mgill_chord import note_to_interval
from src.models.song import Song
from src.shared import settings


def test_correlation_significance(songs):
    t_test_parameters = create_genre_scatter_plots(songs)

    true_str = ''
    false_str = ''

    with open('../data/notes/t_tests.txt', 'w') as f:
        for key, value in t_test_parameters.items():
            result = t_test(value['r'], value['n'])
            file_line = f"{key}: statistically significant: {str(result.significance)}, rho={value['r']}, t={str(result.t_value)}, df={value['n']-2}\n"

            if result.significance:
                true_str += file_line
            else:
                false_str += file_line

        f.write(true_str)
        f.write(false_str)


def create_key_tables(songs):
    create_key_table(songs, 'key_all.png')

    genre_dict = get_genres_dictionary(songs)
    for genre in most_common_genres:

        create_key_table(genre_dict[genre], f'key_{genre}', genre)


settings.init_logger('analysis.log')

bin_file = '../data/songs.pickle'

# songs = get_songs('../data/songs-finished.csv')
# # save binary
# with open(bin_file, 'wb') as file:
#     pickle.dump(songs, file)


songs: List[Song] = get_songs_from_binary_file(bin_file)
songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]

create_key_tables(songs_with_audio_features)

#res = get_quartile_surprises(songs)

# test_correlation_significance(songs)
# res = find_linear_contributions(songs)





