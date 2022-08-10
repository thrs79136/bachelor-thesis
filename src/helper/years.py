from collections import defaultdict, OrderedDict
from typing import List

import numpy as np
from scipy.stats import stats

from src.helper.absolute_surprise import get_song_surprise
from src.helper.img.lineplot import lineplot, lineplot_multiple_lines, stacked_area_plot
from src.helper.statistics_helper import most_common_genres, get_genres_dictionary
from src.models.song import Song

years_dict = None


def init_years_dict(songs: List[Song]):
    global years_dict

    years_dict = defaultdict(list)
    # init dictionary
    for song in songs:
        years_dict[song.chart_year].append(song)


def get_years_dict(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    return years_dict


def draw_feature_line_plot(songs: List[Song], feature_fn, ylabel, title='', suptitle='', dir='',
                           fn_parameters=[], artist_coordinates=None, coordinate_legend=None):
    global years_dict

    init_years_dict(songs)

    od = OrderedDict(sorted(years_dict.items()))

    medians = []

    for value in od.values():
        feature_values = [feature_fn(song, *fn_parameters) for song in value]
        medians.append(np.median(feature_values))

    years = [int(year) for year in od.keys()]
    if title == '':
        title = ylabel

    file_name = ylabel.lower().replace(' ', '_')

    spearman_result = stats.spearmanr(years, medians)
    suptitle = f'n={len(songs)}; r={"{0:.3f}".format(spearman_result.correlation)}; p={"{0:.3f}".format(spearman_result.pvalue)}'

    lineplot(years, medians, 'Jahr', ylabel, file_name, title, suptitle, dir, dot_coordinates=artist_coordinates, dot_legend=coordinate_legend)


def draw_feature_line_plot_with_pos1_coordinates(songs: List[Song], feature_fn, ylabel, title='', fn_parameters=[]):
    filename = f"{ylabel.lower().replace(' ', '_')}.png"
    scatter_coordinates = []
    for song in songs:
        if song.peak_chart_position == 1:
            scatter_coordinates.append((song.chart_year, feature_fn(song)))

    draw_feature_line_plot(songs, feature_fn, ylabel,
                           filename, f'{ylabel} im Verlauf der Zeit', dir='chartpos1',
                           artist_coordinates=scatter_coordinates, fn_parameters=fn_parameters )




def draw_progressions_line_plot(songs: List[Song], uses_prog_fn, ylabel, title='', suptitle='', dir=''):
    years_dict = get_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))

    years = [int(year) for year in od.keys()]
    y_values = []

    for song_list in od.values():
        songs_with_prog = [song for song in song_list if uses_prog_fn(song)]
        y_values.append(len(songs_with_prog)/len(song_list))

    lineplot(years, y_values, 'Jahr', ylabel, 'prog', title, suptitle, dir)


def draw_genres_perc_line_plots(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))
    years = [int(year) for year in od.keys()]

    genre_dict = defaultdict(list)

    for year_index, song_list in enumerate(od.values()):
        # genre_song_count = defaultdict(int)

        for genre in most_common_genres:
            genre_dict[genre].append(0)

        for song in song_list:

            for genre in most_common_genres:
                if genre in song.genres:
                    genre_dict[genre][-1] += 1
                    # genre_song_count[genre] += 1

        for genre in most_common_genres:
            genre_dict[genre][-1] = genre_dict[genre][-1] / len(song_list)

    for genre, y_values in genre_dict.items():
        percentages = [y * 100 for y in y_values]
        lineplot(years, percentages, 'Jahr', f'Anteil',
                 f'{genre}_perc.png',
                 f'Anteil von {genre.capitalize()} im Verlauf der Zeit', dir='years_genres')


def draw_genre_feature_line_plots(songs: List[Song]):
    genre_dict = get_genres_dictionary(songs)
    for genre in most_common_genres:
        draw_feature_line_plot(genre_dict[genre], Song.get_spotify_feature, f'Tempo', f'tempo_{genre}.png',
                               fn_parameters=['tempo'], dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_spotify_feature, 'Valence', f'valence_{genre}.png',
                               fn_parameters=['valence'], dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_spotify_feature, 'Danceability', f'danceability_{genre}.png',
                               fn_parameters=['danceability'], dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_spotify_feature, 'Lieddauer', f'duration_{genre}.png',
                               fn_parameters=['duration_ms'], dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_section_repetitions_count,
                               'Wiederholung von Sektionen', f'section_repetition_{genre}.png',
                               'Wiederholung von Sektionen', dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], get_song_surprise, '"Überraschende" Akkordfolgen',
                               f'absolute_surprise_{genre}.png', '"Überraschende" Akkordfolgen',
                               dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.analyze_different_keys2,
                               'Verwendung tonartsfremder Akkorde', f'different_keys_{genre}.png',
                               'Verwendung tonartsfremder Akkorde', dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_tension_use, 'Verwendung von Tensions',
                               f'tensions_use_{genre}.png', 'Verwendung von Tensions', dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_different_chords_count, 'Verschiedene Akkorde',
                               f'different_chords_{genre}.png', 'Verschiedene Akkorde', dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_peak_chart_position, 'Höchste Chartposition',
                               f'peak_chart_pos_{genre}.png', 'Höchste Chartposiiton im Zeitverlauf',
                               dir='genres_development')
        draw_feature_line_plot(genre_dict[genre], Song.get_minor_count, 'Anteil von Mollakkorden',
                               f'minor_chords_{genre}.png', 'Anteil von Mollakkorden im Zeitverlauf',
                               dir='genres_development')


# looks like crap
def draw_genres_line_plot(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))
    years = [int(year) for year in od.keys()]

    genre_dict = defaultdict(list)

    for year_index, song_list in enumerate(od.values()):
        # genre_song_count = defaultdict(int)

        for genre in most_common_genres:
            genre_dict[genre].append(0)

        for song in song_list:

            for genre in most_common_genres:
                if genre in song.genres:
                    genre_dict[genre][-1] += 1
                    # genre_song_count[genre] += 1

        for genre in most_common_genres:
            genre_dict[genre][-1] = genre_dict[genre][-1] / len(song_list)

    lineplot_multiple_lines(years, genre_dict.values(), list(genre_dict.keys()), 'Jahr', 'Anteil von Genres',
                            'genre_perc.png',
                            'Anteil von Genres')


# also looks like crap
def draw_genres_area_plot(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))
    years = [int(year) for year in od.keys()]

    genre_dict = defaultdict(list)

    for year_index, song_list in enumerate(od.values()):
        # genre_song_count = defaultdict(int)

        for genre in most_common_genres:
            genre_dict[genre].append(0)

        try:
            for song in song_list:
                # only use songs with one genre
                if len(song.genres) == 1 and genre_dict.get(song.genres[0], -1) != -1:
                    genre_dict[song.genres[0]][-1] += 1
                # for genre in most_common_genres:
                #     if genre in song.genres:
                #         genre_dict[genre][-1] += 1
                # genre_song_count[genre] += 1
        except Exception:
            print(song.genres[0])

        for genre in most_common_genres:
            genre_dict[genre][-1] = genre_dict[genre][-1] / len(song_list)

    stacked_area_plot(years, genre_dict.values(), list(genre_dict.keys()), 'Jahr', 'Anteil von Genres',
                      'genre_perc.png',
                      'Anteil von Musikrichtungen im Zeitverlauf')
