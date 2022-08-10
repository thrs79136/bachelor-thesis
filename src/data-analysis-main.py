import pickle
import shutil
from collections import defaultdict
from typing import List

import numpy as np

from src.helper.absolute_surprise import init_progressions_dict, get_quartile_surprises, get_song_surprise, \
    analyze_absolute_surprises, get_different_progressions_feature, uses_doo_wop_progression
from src.helper.absolute_surprise_chords import analyze_absolute_surprises_chords, init_chords_dict
from src.helper.file_helper import get_songs_from_binary_file, get_songs, save_feature_csv, get_songs_from_feature_csv, \
    save_median_feature_csv
from src.helper.img.boxplot import create_boxplot
from src.helper.img.lineplot import lineplot_multiple_lines, stacked_area_plot, lineplot
from src.helper.img.parallel_coordinates import create_parallel_coordinates_plot, create_parallel_coordinates_plot_new, \
    create_parallel_coordinates_plot_newest
from src.helper.img.pca import pca_test2, get_genres_to_color, chart_pos_to_color, popularity_to_color, decade_to_color
from src.helper.artists import group_by_artist, init_artists_dict, get_artist_feature_coordinates, \
    draw_feature_line_plot_with_artist_coordinates
from src.helper.spotify_api import get_popularity, init_spotify
from src.helper.statistics_helper import get_genres_dictionary, \
    most_common_genres, create_key_table, create_genre_scatter_plots, t_test, \
    analyze_song_feature_correlation, analyze_song_groups, group_by_year
from src.helper.years import draw_feature_line_plot, draw_genres_line_plot, \
    draw_genres_area_plot, draw_genres_perc_line_plots, draw_genre_feature_line_plots, init_years_dict, \
    draw_progressions_line_plot, draw_feature_line_plot_with_pos1_coordinates
from src.models.mgill_chord import RomNumNotations
from src.models.pca_config import PCAConfig
from src.models.song import Song, key_dict
from src.shared import settings, dictionaries

# TODO move to scatter plot
from src.shared.dictionaries import init_song_features


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
                                     directory='circle_of_fifths', feature_fn_parameters=parameters3, use_spotify_popularity=True)


    def process_result(result, dist, scale_id):
        if dist > 1/6:
            result += dist
        return result

    parameters = [process_result, lambda res, chord_count: res / chord_count, False]
    parameters2 = [process_result, lambda res, chord_count: res / chord_count, True]

    analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_general,
                                     'Abweichungen im Quintenzirkel (Ignorieren benachbarter Tonarten)', use_spotify_popularity=True,
                                     directory='circle_of_fifths', feature_fn_parameters=parameters)
    analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_general,
                                     'Abweichungen im Quintenzirkel DC (Ignorieren benachbarter Tonarten)',
                                     directory='circle_of_fifths', feature_fn_parameters=parameters2, use_spotify_popularity=True)

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


def create_artists_lineplot(songs: List[Song]):
    init_artists_dict(songs)
    res = group_by_artist(songs_with_audio_features)


    for i, dict_item in enumerate(res.items()):
        if i >= 5:
            break
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.get_minor_count,
                                                       'Anteil von Mollakkorden')
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.get_spotify_feature,
                                                       'Danceability', fn_parameters=['danceability'])
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, get_song_surprise,
                                                       'Überraschende Akkordfolgen')
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.get_spotify_feature,
                                                       'Danceability', fn_parameters=['duration_ms'])
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.get_spotify_feature,
                                                       'Tempo', fn_parameters=['tempo'])
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.get_foreign_scale_chords_count,
                                                       'Tonartfremde Akkkorde')
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.analyze_different_keys2,
                                                       'Abstände im Quintenzirkel')
        draw_feature_line_plot_with_artist_coordinates(dict_item[0], songs, Song.get_section_repetitions_count,
                                                       'Wiederholung von Sektionen')


def start_correlation_analysis(songs: List[Song]):
    analyze_song_feature_correlation(songs, Song.get_similar_chords, 'Verwendung ähnlicher Folgen', use_spotify_popularity=True, directory='spotify_popularity')
    analyze_song_feature_correlation(songs, Song.get_similar_chords, 'Verwendung ähnlicher Folgen test', use_spotify_popularity=False, directory='spotify_popularity')
    # analyze_song_feature_correlation(songs, Song.get_chord_distances, 'Akkordabstände', use_spotify_popularity=True, directory='spotify_popularity')
    # analyze_song_feature_correlation(songs, Song.get_chord_distances, 'Akkordabstände test', use_spotify_popularity=False, directory='spotify_popularity')


    #analyze_song_feature_correlation(songs, Song.get_added_seventh_use, 'test', use_spotify_popularity=False, directory='spotify_popularity')
    # todo give added seventh proper name
    #analyze_song_feature_correlation(songs, Song.get_added_seventh_use, 'Verwendung von 7-Akkorden', use_spotify_popularity=True, directory='spotify_popularity')

    # analyze_song_feature_correlation(songs_with_audio_features, Song.get_different_chords_count, 'Anzahl verschiedener Akkorde', use_spotify_popularity=True, directory='spotify_popularity')
    return


feature_list = [
    # 'danceability',
    # 'energy',
    'major_percentage',
    'absolute_surprise',
    #'non_triad_chords_percentage',
    'different_sections_count',
    'section_repetitions',
    'get_added_seventh_use',
    # 'get_added_sixth_use',
    # 'power_chords',
    # 'neither_chords',
    # 'circle_of_fifths_dist',
    'circle_of_fifths_dist_largest_dist',
    'tonic_percentage',
    # 'supertonic_percentage',
    'dominant_percentage',
    'i_to_v',
    'v_to_i'
]

feature_list1  = [
    # 'decade',
    # 'year',
    'minor_percentage',
    # 'major_percentage',
    # 'absolute_surprise',
    'circle_of_fifths_dist',
    # 'circle_of_fifths_dist_largest_dist',
    # 'danceability',
    # 'energy',
    'tonic_percentage',
    # 'supertonic_percentage',
    'dominant_percentage',
    #'non_triad_chords_percentage',
    # 'different_sections_count',
    'get_added_seventh_use',
    # 'get_added_sixth_use',
    # 'power_chords',
    # 'neither_chords',
    # 'section_repetitions',
    # 'i_to_v',
    # 'v_to_i',
    # 'chart_pos',
    # 'spotify_popularity',
    # 'genre',
    # 'mode',
    'tempo',
    # 'valence',
    'duration',
    'chord_distances',
    'different_chords',
    'different_progressions',
    # 'chord_surprise'
]



def start_parallel_coordinate_creation():
    features = [
    # 'danceability',
    # 'energy',
    'major_percentage',
    'absolute_surprise',
    #'non_triad_chords_percentage',
    'different_sections_count',
    'section_repetitions',
    'get_added_seventh_use',
    # 'get_added_sixth_use',
    # 'power_chords',
    # 'neither_chords',
    'circle_of_fifths_dist',
    # 'circle_of_fifths_dist_largest_dist',
    'tonic_percentage',
    # 'supertonic_percentage',
    'dominant_percentage',
    # 'i_to_v',
    # 'v_to_i'
    ]

    features_arr = [
    'major_percentage',
    'circle_of_fifths_dist',
    'get_added_seventh_use',
    'tonic_percentage',
    'dominant_percentage',
    'section_repetitions',
    'different_sections_count',
    'absolute_surprise',
    ]
    create_parallel_coordinates_plot_newest(features_arr)



def start_pca(songs: List[Song]):
    decade_dict = {
        1950: 'yellow',
        1960: 'orange',
        1970: 'red',
        1980: 'blue',
        1990: 'green'
    }

    color_fn = lambda song: decade_dict[song.get_decade()]
    inv_dict = {v: f'{str(k)}s' for k, v in decade_dict.items()}

    labels_dict = {f'{str(k)}s': v for k, v in decade_dict.items()}

    decade_config = PCAConfig(feature_list1, color_fn, labels_dict)

    pca_test2(songs, 'Song features PCA 2022-08-09 (decade)', decade_config)


def draw_feature_line_plots(songs: List[Song]):
    draw_feature_line_plot(songs, Song.get_similar_chords, 'Verwendung ähnlicher Noten')
    return
    draw_feature_line_plot(songs, Song.get_chord_distances, 'Akkordabstände')
    draw_feature_line_plot(songs, Song.get_tension_use, 'Verwendung von Tensions')
    draw_feature_line_plot(songs, Song.get_added_seventh_use, 'Septakkorde')
    draw_feature_line_plot(songs_with_audio_features, Song.get_different_sections_count, 'Different Sections')
    draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Tempo', fn_parameters=['tempo'])
    draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Valence', fn_parameters=['valence'])
    draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Danceability', fn_parameters=['danceability'])
    draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Lieddauer', fn_parameters=['duration_ms'])
    draw_feature_line_plot(songs_with_audio_features, Song.get_section_repetitions_count, 'Wiederholung von Sektionen')
    draw_feature_line_plot(songs_with_audio_features, get_song_surprise, 'Überraschende Akkordfolgen')
    draw_feature_line_plot(songs_with_audio_features, Song.analyze_different_keys2, 'Verwendung tonartsfremder Akkorde')
    draw_feature_line_plot(songs_with_audio_features, Song.get_tension_use, 'Verwendung von Tensions')
    draw_feature_line_plot(songs_with_audio_features, Song.get_different_chords_count, 'Verschiedene Akkorde')
    draw_feature_line_plot(songs_with_audio_features, Song.get_peak_chart_position, 'Höchste Chartposition')
    draw_feature_line_plot(songs_with_audio_features, Song.get_minor_count, 'Anteil von Mollakkorden')


settings.init_logger('analysis.log')
init_song_features()
init_spotify()

bin_file = '../data/songs.pickle'

# songs = get_songs('../data/songs-finished.csv')
# #
# #save binary
# with open(bin_file, 'wb') as file:
#     pickle.dump(songs, file)
# exit()

songs: List[Song] = get_songs_from_binary_file(bin_file)
songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]

genres_dict = defaultdict(int)

for song in songs_with_audio_features:
    genre_id = song.get_genres_id()
    genres_dict[genre_id] += 1

common = {k: v for k, v in sorted(genres_dict.items(), key=lambda item: item[1], reverse=True)}

init_artists_dict(songs)
res = group_by_artist(songs_with_audio_features)

exit()
init_progressions_dict(songs_with_audio_features)
init_chords_dict(songs_with_audio_features)

save_feature_csv(songs_with_audio_features, list(dictionaries.song_features_dict.keys()))
exit()

draw_feature_line_plot_with_pos1_coordinates(songs_with_audio_features, Song.analyze_different_keys2, 'Anteil von Mollakkorden')
exit()

draw_feature_line_plots(songs_with_audio_features)

exit()

start_correlation_analysis(songs_with_audio_features)
exit()





start_pca(songs_with_audio_features)
exit()

# res = get_different_progressions_feature(songs_with_audio_features[0])
# exit()

# TODO number of different chords





analyze_absolute_surprises_chords(songs_with_audio_features)
exit()
init_progressions_dict(songs_with_audio_features)
# save_median_feature_csv(songs_with_audio_features, list(dictionaries.song_features_dict.keys()))
# save_feature_csv(songs_with_audio_features, list(dictionaries.song_features_dict.keys()))
# #songs = get_songs_from_feature_csv()
# exit()

start_parallel_coordinate_creation()
exit()








sorted_songs = sorted(songs_with_audio_features, key=lambda song: song.get_spotify_feature('danceability'), reverse=True)

# analyze_song_groups(songs_with_audio_features, Song.get_genres, 'Genres und höchste Chartplatzierungen', 'genres.png', 9, ['disco', 'british', 'singer-songwriter', 'dance'])
# analyze_song_groups(songs_with_audio_features, Song.get_used_instruments, 'Instrumente und höchste Chartplatzierungen', 'instruments.png', 8, ['voice', 'drums', 'strings', 'bass', 'synth', 'synthesiser'])
# analyze_song_groups(songs_with_audio_features, Song.get_metre, 'Taktart und höchste Chartplatzierungen', 'metre_boxplot.png')
# analyze_song_groups(songs_with_audio_features, Song.get_mode, 'Tongeschlecht und höchste Chartplatzierungen', 'tongeschlecht.png')
analyze_song_groups(songs_with_audio_features, Song.get_key, 'Tonart und höchste Chartplatzierungen', 'tonart.png', group_order=key_dict.values())



for rom_num1 in RomNumNotations:
    for rom_num2 in RomNumNotations:
        if rom_num1.name != rom_num2.name:
            transition = (rom_num1.name, rom_num2.name)
            analyze_song_feature_correlation(songs_with_audio_features, Song.chord_transition_test,
                                             f'{rom_num1.name} zu {rom_num2.name} Relative Haeufigkeit', directory='transition_spotify',
                                             feature_fn_parameters=[transition], use_spotify_popularity=True)

exit()



#analyze_scales()
# analyze_song_feature_correlation(songs_with_audio_features, Song.get_metre_changes_count, 'Taktartänderungen', use_spotify_popularity=True, directory='spotify_popularity')
# analyze_song_feature_correlation(songs_with_audio_features, Song.get_tension_use, 'Verwendung von Tensions', use_spotify_popularity=True, directory='spotify_popularity')
#analyze_song_feature_correlation(songs_with_audio_features, Song.get_section_repetitions_count, 'Wiederholungen von Sektionen', use_spotify_popularity=True, directory='spotify_popularity')
#analyze_song_feature_correlation(songs_with_audio_features, Song.get_tonic_changes_count, 'Tonartänderungen', use_spotify_popularity=True, directory='spotify_popularity')
#analyze_song_feature_correlation(songs_with_audio_features, Song.get_spotify_feature, 'Dauer', use_spotify_popularity=True, directory='spotify_popularity', feature_fn_parameters=['duration_ms'])
#analyze_song_feature_correlation(songs_with_audio_features, get_song_surprise, 'Ueberraschende Akkordfolgen', use_spotify_popularity=True, directory='spotify_popularity')




sorted_songs[0].analyze_different_keys_largest_distance()

analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys2, 'Anteil Tonartfremder Akkorde', use_spotify_popularity=True)
#analyze_song_feature_correlation(songs_with_audio_features, Song.analyze_different_keys_largest_distance, 'Anteil Tonartfremder Akkorde LD', use_spotify_popularity=True)


# for rom_num in RomNumNotations:
    # analyze_song_feature_correlation(songs_with_audio_features, Song.chord_frequency,
    #                                  f'{rom_num.name} Relative Haeufigkeit', directory='chord_frequency_spotify',
    #                                  feature_fn_parameters=[f'{rom_num.name}'], use_spotify_popularity=True)
#
#     analyze_song_feature_correlation(songs_with_audio_features, Song.chord_frequency2,
#                                      f'{rom_num.name} Relative Haeufigkeit', directory='chord_frequency_spotify2',
#                                      feature_fn_parameters=[f'{rom_num.name}'], use_spotify_popularity=True)
#     analyze_song_feature_correlation(songs_with_audio_features, Song.chord_frequency2,
#                                      f'{rom_num.name}m Relative Haeufigkeit', directory='chord_frequency_spotify2',
#                                      feature_fn_parameters=[f'{rom_num.name}m'], use_spotify_popularity=True)
exit()

analyze_song_feature_correlation(songs_with_audio_features, Song.get_minor_count, 'Anteil von Mollakkorden', use_spotify_popularity=True)


draw_feature_line_plot(songs_with_audio_features, Song.get_section_repetitions_count, 'Wiederholung von Sektionen', 'section_repetition.png', 'Wiederholung von Sektionen')

create_artists_lineplot(songs_with_audio_features)


draw_genre_feature_line_plots(songs_with_audio_features)


draw_genres_perc_line_plots(songs_with_audio_features)
# draw_genres_line_plot(songs_with_audio_features)


#pca_test2(songs_with_audio_features, 'Song features PCA 2022-07-13', get_genres_to_color)

# create_parallel_coordinates_plot_years(songs_with_audio_features)

#draw_genre_feature_line_plots(songs_with_audio_features)


analyze_song_feature_correlation(songs_with_audio_features, Song.get_non_triad_rate, 'Akkorde ohne Dreiklang (%)')
exit()

draw_feature_line_plot(songs_with_audio_features, Song.get_different_sections_count, 'Different Sections', 'different_sections.png')

draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Tempo', 'tempo.png', fn_parameters=['tempo'])
draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Valence', 'valence.png', fn_parameters=['valence'])
draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Danceability', 'danceability.png', fn_parameters=['danceability'])
draw_feature_line_plot(songs_with_audio_features, Song.get_spotify_feature, 'Lieddauer', 'duration.png', fn_parameters=['duration_ms'])
draw_feature_line_plot(songs_with_audio_features, Song.get_section_repetitions_count, 'Wiederholung von Sektionen', 'section_repetition.png', 'Wiederholung von Sektionen')
draw_feature_line_plot(songs_with_audio_features, get_song_surprise, 'Überraschende Akkordfolgen', 'absolute_surprise.png', '"Überraschende" Akkordfolgen')
draw_feature_line_plot(songs_with_audio_features, Song.analyze_different_keys2, 'Verwendung tonartsfremder Akkorde', 'different_keys.png', 'Verwendung tonartsfremder Akkorde')
draw_feature_line_plot(songs_with_audio_features, Song.get_tension_use, 'Verwendung von Tensions', 'tensions_use.png', 'Verwendung von Tensions')
draw_feature_line_plot(songs_with_audio_features, Song.get_different_chords_count, 'Verschiedene Akkorde', 'different_chords.png', 'Verschiedene Akkorde')
draw_feature_line_plot(songs_with_audio_features, Song.get_peak_chart_position, 'Höchste Chartposition', 'peak_chart_pos.png', 'Höchste Chartposiiton im Zeitverlauf')
draw_feature_line_plot(songs_with_audio_features, Song.get_minor_count, 'Anteil von Mollakkorden', 'minor_chords.png', 'Anteil von Mollakkorden im Zeitverlauf')



for rom_num1 in RomNumNotations:
    for rom_num2 in RomNumNotations:
        if rom_num1.name != rom_num2.name:
            transition = (rom_num1.name, rom_num2.name)
            analyze_song_feature_correlation(songs_with_audio_features, Song.chord_transition_test,
                                             f'{rom_num1.name} zu {rom_num2.name} Relative Haeufigkeit', directory='transitions',
                                             feature_fn_parameters=[transition])




for rom_num in RomNumNotations:
    # maj
    analyze_song_feature_correlation(songs_with_audio_features, Song.chords_test,
                                    f'{rom_num.name} Relative Haeufigkeit', directory='chord_frequency2', feature_fn_parameters=[rom_num.name])
    # # min
    analyze_song_feature_correlation(songs_with_audio_features, Song.chords_test,
                                     f'{rom_num.name}n Relative Haeufigkeit', directory='chord_frequency2',
                                     feature_fn_parameters=[f'{rom_num.name}m'])



analyze_absolute_surprises(songs_with_audio_features)

pca_test2(songs_with_audio_features, 'Song features PCA (Chart positions) new', get_genres_to_color)
x = 42


#analyze_scales()
#analyze_song_feature_correlation(songs_with_audio_features, Song.get_non_triad_rate, 'Akkorde ohne Dreiklang (%)')
#analyze_song_feature_correlation(songs_with_audio_features, Song.get_minor_count, 'Mollakkorde %')
#analyze_song_feature_correlation(songs_with_audio_features, Song.get_tonic_changes_count, 'Anzahl Tonartänderungen')


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
#analyze_song_groups(songs_with_audio_features, Song.get_mode, 'Tongeschlecht und höchste Chartplatzierungen', 'tongeschlecht.png')





