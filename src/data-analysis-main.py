
import pickle
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

import matplotlib.pyplot as plt


def test_correlation_significance(songs):
    t_test_parameters = create_genre_scatter_plots(songs)
    significance = {}
    for key, value in t_test_parameters.items():
        significance[key] = t_test(value['r'], value['n'])

    return significance


settings.init_logger('analysis.log')

bin_file = '../data/songs.pickle'

# songs = get_songs('../data/songs-finished.csv')
# # save binary
# with open(bin_file, 'wb') as file:
#     pickle.dump(songs, file)


songs: List[Song] = get_songs_from_binary_file(bin_file)

res = find_linear_contributions(songs)
x = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
v = 42
print(x)
#res = get_quartile_surprises(songs)






