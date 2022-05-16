
import pickle
from collections import defaultdict
from typing import List

from src.helper.cadences import analyze_cadences
from src.helper.chord_progressions import identify_chord_progressions, find_progressions
from src.helper.file_helper import get_songs, get_songs_from_binary_file
from src.helper.statistics_helper import get_median_chart_positions, create_bar_plot, get_genres_dictionary, \
    most_common_genres, create_key_table, create_mode_table
from src.models.mgill_chord import note_to_interval
from src.models.song import Song
from src.shared import settings

import matplotlib.pyplot as plt



settings.init_logger('analysis.log')

# songs = get_songs('../data/songs-finished.csv')
#
# # save binary
# with open(f'test.pickle', 'wb') as file:
#     pickle.dump(songs, file)
#
bin_file = '../data/songs.pickle'
songs = get_songs_from_binary_file(bin_file)
create_key_table(songs, 'key_all.png')
create_mode_table(songs, 'mode-all.png')

genres_dict = get_genres_dictionary(songs)

for genre in most_common_genres:
    create_key_table(genres_dict[genre], f'key_{genre}.png', genre)
    create_mode_table(genres_dict[genre], f'mode_{genre}.png', genre)


# get_median_chart_positions(songs, 'key')
# identify_chord_progressions(songs)
find_progressions(songs)

analyze_cadences(songs)






