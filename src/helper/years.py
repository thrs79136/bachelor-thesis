from collections import defaultdict, OrderedDict
from typing import List

import numpy as np
import pandas as pd
from scipy.stats import stats

from src.helper.absolute_surprise import get_song_surprise
from src.helper.genres import genres_genres, genres_accepted_genres
from src.helper.img.lineplot import lineplot, lineplot_multiple_lines, stacked_area_plot
from src.helper.statistics_helper import most_common_genres, get_genres_dictionary
from src.models.song import Song
from src.models.song_feature import SongFeature

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


def draw_sentiment_lineplot2(songs: List[Song]):
    # exclude songs without sentiments
    songs = [song for song in songs if song.sentiments is not None]
    years_dict = get_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))

    year_sentiment_dict = {}


    for year, song_list in od.items():
        sentiment_count = defaultdict(int)
        for song in song_list:
            sentiment = song.sentiments[0]['label']
            sentiment_count[sentiment] += 1
            x = 42

        # convert to percentages
        for sentiment_name, sentiment_val in sentiment_count.items():
            sentiment_count[sentiment_name] = sentiment_val / len(song_list)
        year_sentiment_dict[year] = sentiment_count

    possible_sentiments = ['POSITIVE', 'NEGATIVE']
    sentiment_perc_lists = []

    for i, sentiment in enumerate(possible_sentiments):
        sentiment_perc_lists.append([])
        for sentiment_percentages in year_sentiment_dict.values():
            sentiment_perc_lists[i].append(sentiment_percentages[sentiment])

        years = list(year_sentiment_dict.keys())
        percentages = sentiment_perc_lists[i]

        spearman_result = stats.spearmanr(years, percentages)
        suptitle = f'n={len(songs)}; r={"{0:.3f}".format(spearman_result.correlation)}; p={"{0:.3f}".format(spearman_result.pvalue)}'


        lineplot(years, percentages, 'Jahr', 'Sentiment', f'{sentiment}-years.png', suptitle=suptitle)


def analyze_instruments(songs: List[Song], dir=''):
    years_instrument_dict = {}
    total_songs_count = defaultdict(int)

    for song in songs:
        total_songs_count[song.chart_year] += 1

        if years_instrument_dict.get(song.chart_year, -1) == -1:
            years_instrument_dict[song.chart_year] = defaultdict(int)
        for instrument in song.get_used_instruments():
            if instrument == 'synth' or instrument == 'synthesiser':
                instrument = 'synthesizer'
            years_instrument_dict[song.chart_year][instrument] += 1

    instruments = ['guitar', 'synthesizer', 'piano', 'saxophone', 'strings', 'trumpet']
    # instruments = ['electric guitar']

    perc_dict = {}

    for year, instrument_dict in years_instrument_dict.items():
        perc_dict[year] = defaultdict(int)
        for instrument, count in instrument_dict.items():
            if instrument in instruments:
                perc_dict[year][instrument] = count / total_songs_count[year]

    od = OrderedDict(sorted(perc_dict.items()))

    years = list(od.keys())
    for instrument in instruments:
        percentages = [inst_dict[instrument] for inst_dict in od.values()]
        spearman_result = stats.spearmanr(years, percentages)
        suptitle = f'n={len(songs)}; r={"{0:.3f}".format(spearman_result.correlation)}; p={"{0:.3f}".format(spearman_result.pvalue)}'
        lineplot(years, percentages, 'Jahr', 'Anteil Lieder', f'{instrument}-percentages.png', suptitle=suptitle, title = instrument, dir=dir)


def draw_sentiment_lineplot(songs: List[Song]):
    # exclude songs without sentiments
    songs = [song for song in songs if song.emotions is not None]
    years_dict = get_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))

    year_sentiment_dict = {}


    for year, song_list in od.items():
        sentiment_count = defaultdict(int)
        for song in song_list:
            sentiment = song.emotions[0]['label']
            if sentiment == 'fear':
                x = 42
            sentiment_count[sentiment] += 1

        # convert to percentages
        for sentiment_name, sentiment_val in sentiment_count.items():
            sentiment_count[sentiment_name] = sentiment_val / len(song_list)
        year_sentiment_dict[year] = sentiment_count

    possible_sentiments = ['joy', 'love', 'anger', 'surprise', 'sadness', 'fear']
    sentiment_perc_lists = []

    for i, sentiment in enumerate(possible_sentiments):
        sentiment_perc_lists.append([])
        for sentiment_percentages in year_sentiment_dict.values():
            sentiment_perc_lists[i].append(sentiment_percentages[sentiment])

        years = list(year_sentiment_dict.keys())
        percentages = sentiment_perc_lists[i]

        spearman_result = stats.spearmanr(years, percentages)
        suptitle = f'n={len(songs)}; r={"{0:.3f}".format(spearman_result.correlation)}; p={"{0:.3f}".format(spearman_result.pvalue)}'
        if spearman_result.pvalue <= 0.05:
            x = 42


        lineplot(years, percentages, 'Jahr', 'Sentiment', f'{sentiment}-years.png', suptitle=suptitle, dir='sentiments', title=sentiment.capitalize())



    # lineplot_multiple_lines(year_sentiment_dict.keys(), sentiment_perc_lists, possible_sentiments, 'Jahr', 'Sentiments', 'testtest.png', 'Sentiments')
    x = 42


# rewrite this
# def draw_feature_line_plot_from_song_feature(songs: List[Song], songfeature: SongFeature):
#     title = songfeature.display_name
#     ylabel = title
#     feature_fn = songfeature.feature_fn
#     fn_parameters = songfeature.parameters
#     draw_feature_line_plot(songs, feature_fn, ylabel, title, fn_parameters=fn_parameters, use_variance=True)


# def draw_feature_line_plot(songs: List[Song], feature_fn, ylabel, title='', suptitle='', dir='',
#                            fn_parameters=[], artist_coordinates=None, coordinate_legend=None, use_variance=False):
#     global years_dict
#
#     init_years_dict(songs)
#
#     od = OrderedDict(sorted(years_dict.items()))
#
#     medians_or_variance = []
#
#     for value in od.values():
#         feature_values = [feature_fn(song, *fn_parameters) for song in value]
#         result = np.var(feature_values) if use_variance else np.median(feature_values)
#         medians_or_variance.append(result)
#
#     years = [int(year) for year in od.keys()]
#     if title == '':
#         title = ylabel
#
#     file_name = ylabel.lower().replace(' ', '_')
#
#     spearman_result = stats.spearmanr(years, medians_or_variance)
#     suptitle = f'n={len(songs)}; r={"{0:.3f}".format(spearman_result.correlation)}; p={"{0:.3f}".format(spearman_result.pvalue)}'
#     if use_variance and dir == '':
#         dir = 'variance'
#
#     lineplot(years, medians_or_variance, 'Jahr', ylabel, file_name, title, suptitle, dir, dot_coordinates=artist_coordinates, dot_legend=coordinate_legend)
#

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


def draw_mode_area_plot(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))
    years = [int(year) for year in od.keys()]

    y_values_maj = []

    for year_index, song_list in enumerate(od.values()):
        # count major songs for every year
        major_count = len([song for song in song_list if song.get_mode() == 'Dur'])
        major_perc = major_count / len(song_list)
        y_values_maj.append(major_perc)
        x = 42

    y_values_min = [1-y for y in y_values_maj]

    lineplot_multiple_lines(years, [y_values_min, y_values_maj], ['Moll', 'Dur'],  'Jahr', 'Anteil von Tongeschlechtern', 'mode_perc.png',
                      'Verwendung von Moll und Dur im Zeitverlauf')
    # stacked_area_plot(years, [y_values_min, y_values_maj], ['Moll', 'Dur'], 'Jahr', 'Anteil von Tongeschlechtern',
    #                   'mode_perc.png',
    #                   'Verwendung von Moll und Dur im Zeitverlauf')


# t.b.d.
def compare_genre_features_over_time(songs: List[Song]):
    pass


def draw_genres_line_plot_new(songs: List[Song]):
    years, genre_dict = get_year_genre_perc_dict(songs)

    lineplot_multiple_lines(years, genre_dict.values(), list(genre_dict.keys()), 'Jahr', 'Anteil von Genres',
                            'genre_perc_lines-.png',
                            'Anteil von Genres')

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


def get_year_genre_perc_dict(songs):
    global years_dict

    init_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))
    years = [int(year) for year in od.keys()]

    genre_dict = defaultdict(list)

    for year_index, item in enumerate(od.items()):

        print(item[0])

        song_list = item[1]
        genre_song_count = defaultdict(int)
        year_song_count = 0

        for genre in genres_genres:
            genre_dict[genre].append(0)

        try:
            for song in song_list:
                song_genres = '-'.join(sorted([genre for genre in song.genres if genre in genres_accepted_genres]))
                if song_genres in genres_genres:
                    print(song_genres)
                    genre_dict[song_genres][-1] += 1
                    genre_song_count[song_genres] += 1
                    year_song_count += 1
        except Exception:
            print(song.genres[0])

        for genre in genres_genres:
            genre_dict[genre][-1] = genre_dict[genre][-1] / year_song_count

    return years, genre_dict


def draw_genres_area_plot_new(songs: List[Song], filename='genre_perc_-.png'):
    years, genre_dict = get_year_genre_perc_dict(songs)

    stacked_area_plot(years, genre_dict.values(), list(genre_dict.keys()), 'Jahr', 'Anteil von Genres',
                      filename,
                      'Anteil von Musikrichtungen im Zeitverlauf')


# also looks like crap
def draw_genres_area_plot(songs: List[Song]):
    global years_dict

    init_years_dict(songs)
    od = OrderedDict(sorted(years_dict.items()))
    years = [int(year) for year in od.keys()]

    genre_dict = defaultdict(list)

    for year_index, song_list in enumerate(od.values()):
        genre_song_count = defaultdict(int)

        for genre in most_common_genres:
            genre_dict[genre].append(0)

        try:
            for song in song_list:
                # only use songs with one genre
                # if len(song.genres) == 1 and genre_dict.get(song.genres[0], -1) != -1:
                #     genre_dict[song.genres[0]][-1] += 1
                for genre in most_common_genres:
                    if genre in song.genres:
                        genre_dict[genre][-1] += 1
                genre_song_count[genre] += 1
        except Exception:
            print(song.genres[0])

        for genre in most_common_genres:
            genre_dict[genre][-1] = genre_dict[genre][-1] / len(song_list)

    stacked_area_plot(years, genre_dict.values(), list(genre_dict.keys()), 'Jahr', 'Anteil von Genres',
                      'genre_perc2.png',
                      'Anteil von Musikrichtungen im Zeitverlauf')

