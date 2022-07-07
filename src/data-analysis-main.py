
import pickle
import shutil
import statistics
from collections import defaultdict
from typing import List

from src.helper.absolute_surprise import prog_prob, split_by_quartiles, get_quartile_surprises_mean, \
    find_linear_contributions, init, get_song_average_surprise, get_quartile_surprises, init_group_dict, \
    get_quarter_group, get_song_surprise, analyze_absolute_surprises
from src.helper.cadences import analyze_cadences
from src.helper.chord_progressions import identify_chord_progressions, find_progressions, find_song_progressions
from src.helper.file_helper import get_songs, get_songs_from_binary_file
from src.helper.img.boxplot import create_boxplot
from src.helper.img.pca import pca, pca_test2, pca_test_backup, get_genres_to_color, chart_pos_to_color
from src.helper.statistics_helper import get_median_chart_positions, create_bar_plot, get_genres_dictionary, \
    most_common_genres, create_key_table, create_mode_table, create_genre_scatter_plots, t_test, \
    create_audio_feature_scatter_plot, create_scatter_plot, \
    analyze_song_feature_correlation_all_genres, analyze_song_groups, analyze_song_feature_correlation
from src.models.mgill_chord import note_to_interval, McGillChord, MajOrMin
from src.models.scales import circle_of_fifths
from src.models.song import Song, key_dict
from src.shared import settings
import numpy as np


# TODO move to scatter plot
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


def create_absolute_surprise_box_plot(songs):

    # TODO analyze_song_groups
    res = get_quartile_surprises(songs)
    song_surprises = [res.values()]
    create_boxplot(song_surprises, ['1st quarter', '2nd quarter', '3rd quarter', '4th quarter'], 'Average surprise (chord progressions)', '', 'chord_prog_average_surprises.png')






# def create_chords_count_scatter_plot(songs: List[Song]):
#     different_chords_count = [song.get_different_chords_count() for song in songs]
#     peak_chart_positions = [song.peak_chart_position for song in songs]
#     create_scatter_plot(peak_chart_positions, different_chords_count, 'chord_count.png', '', '',
#                         'Höchste Chartposition', 'Anzahl verschiedener Akkorde')


def analyze_scales():

    # number of different scales
    def process_result2(result, dist, scale_id):
        if not isinstance(result, set):
            result = set()

        result.add(scale_id)
        return result


    parameters3 = [process_result2, lambda res, chord_count: len(res), False]

    analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_general,
                                     'Anzahl Tonarten',
                                     directory='circle_of_fifths', feature_fn_parameters=parameters3)


    def process_result(result, dist, scale_id):
        if dist > 1/6:
            result += dist
        return result

    parameters = [process_result, lambda res, chord_count: res / chord_count, False]
    parameters2 = [process_result, lambda res, chord_count: res / chord_count, True]

    analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_general,
                                     'Abweichungen im Quintenzirkel (Ignorieren benachbarter Tonarten)',
                                     directory='circle_of_fifths', feature_fn_parameters=parameters)
    analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_general,
                                     'Abweichungen im Quintenzirkel DC (Ignorieren benachbarter Tonarten)',
                                     directory='circle_of_fifths', feature_fn_parameters=parameters2)

    # analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_largest_distance,
    #                                 'Abweichungen im Quintenzirkel (Maximale Distanz)', directory='circle_of_fifths')
    # analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_different_chords, 'Abweichungen im Quintenzirkel 2 (Vorgaengerharmonie)', directory='circle_of_fifths')
    # analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys, 'Abweichungen im Quintenzirkel (Vorgaengerharmonie)', directory='circle_of_fifths')

def copynr1(songs):
    nr1_songs = [song for song in songs_with_audio_features if song.peak_chart_position == 1]
    for song in nr1_songs:
        filepath = f'../data/songs/mcgill-billboard/{song.mcgill_billboard_id.zfill(4)}/salami_chords.txt'
        dest = f'../data/chartpos_1/{song.mcgill_billboard_id.zfill(4)}_chords.txt'

        shutil.copyfile(filepath, dest)


settings.init_logger('analysis.log')

bin_file = '../data/songs.pickle'

# songs = get_songs('../data/songs-finished.csv')
# #
# #save binary
# with open(bin_file, 'wb') as file:
#     pickle.dump(songs, file)


songs: List[Song] = get_songs_from_binary_file(bin_file)

songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
#analyze_scales()



#analyze_song_feature_correlation(songs_with_audio_features, Song.get_minor_count, 'Mollakkorde %')
analyze_song_feature_correlation(songs_with_audio_features, Song.get_tonic_changes_count, 'Anzahl Tonartänderungen')


# song1 = Song.from_code(['A:min', 'C:maj', 'F:maj', 'D:min'])
# song2 = Song.from_code(['C:maj', 'Eb:maj', 'F:maj', 'Ab:maj', 'Bb:maj'])
# song3 = Song.from_code(['C:maj', 'G:maj', 'D:maj', 'A:maj', 'E:maj'])
# song4 = Song.from_code(['C:min', 'D:maj', 'E:maj', 'F:min', 'G:min', 'A:maj', 'B:maj'])
# test1 = Song.analyze_different_keys(song1)
# test2 = Song.analyze_different_keys(song2)
# test3 = Song.analyze_different_keys(song3)
# test4 = Song.analyze_different_keys(song4)

# for song in songs_with_audio_features:
#     Song.analyze_different_keys(song)

#pca_test2(songs_with_audio_features, 'Song features PCA (Chart positions)', chart_pos_to_color)
#pca_test2(songs_with_audio_features, 'Song features PCA', get_genres_to_color)


analyze_absolute_surprises(songs_with_audio_features)

#create_absolute_surprise_box_plot(songs_with_audio_features)

#
#
#
# genres_dictionary = get_genres_dictionary(songs_with_audio_features)
#
# for genre in most_common_genres:
#     songs = genres_dictionary[genre]
#     analyze_song_feature_correlation(songs, Song.analyze_different_keys,
#                                      'Abweichungen im Quintenzirkel', genre=genre)
#
# results = [song.analyze_different_keys() for song in songs_with_audio_features]


#analyze_song_groups(songs_with_audio_features, Song.get_genres, 'Genres und höchste Chartplatzierungen', 'genres.png', 9, ['disco', 'british', 'singer-songwriter', 'dance'])
#analyze_song_groups(songs, Song.get_used_instruments, 'Instrumente und höchste Chartplatzierungen', 'instruments.png', 8, ['voice', 'drums', 'strings', 'bass', 'synth', 'synthesiser'])
#analyze_song_groups(songs, Song.get_metre, 'Taktart und höchste Chartplatzierungen', 'metre_boxplot.png')
#analyze_song_groups(songs_with_audio_features, Song.get_mode, 'Tongeschlecht und höchste Chartplatzierungen', 'tongeschlecht.png')
#analyze_song_groups(songs_with_audio_features, Song.get_key, 'Tonart und höchste Chartplatzierungen', 'tonart.png', group_order=key_dict.values())




