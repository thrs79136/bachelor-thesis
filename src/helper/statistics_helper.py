import statistics
from collections import defaultdict
from math import sqrt

import scipy
import scs as scs
import scipy.stats as scs
from typing import List
from matplotlib import pyplot as plt
from src.models.song import Song
from src.models.spotify_song_data import SpotifySongData

figure_number = 0
most_common_genres = ['rock', 'pop', 'soul', 'country', 'blues']


def get_peak_chart_position_list(songs: List[Song]) -> List[int]:
    return [song.peak_chart_position for song in songs]


def create_scatter_plot(x: List, y: List, filename: str, title: str = '', suptitle: str = '', xlabel: str = '', ylabel: str = ''):
    global figure_number

    plt.figure(figure_number)
    figure_number += 1
    plt.style.use('seaborn-whitegrid')
    plt.plot(x, y, 'x', color='black')
    plt.suptitle(title, fontsize=13, y=0.97)
    plt.title(suptitle, fontsize=10)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    #plt.savefig('../data/plots/scatter_plots/' + filename)
    plt.close()


def get_audio_feature_ranks(songs: List[Song], audio_feature: str):
    audio_feature_values = [song.spotify_song_data.audio_features_dictionary[audio_feature] for song in
                            songs]
    audio_feature_ranks = scs.rankdata(audio_feature_values)
    return audio_feature_ranks


def create_audio_feature_scatter_plot(songs: List[Song], audio_feature_name: str, filename: str, genre: str = 'All genres'):

    peak_chart_positions = []
    audio_feature_values = []
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
    for song in songs:
        if song.spotify_song_data.audio_features_dictionary is None:
            continue

        peak_chart_positions.append(song.peak_chart_position)
        audio_feature_values.append(song.spotify_song_data.audio_features_dictionary[audio_feature_name])

    audio_feature_ranks = get_audio_feature_ranks(songs_with_audio_features, audio_feature_name)
    chart_ranks = scs.rankdata(peak_chart_positions)


    corr_coeff = get_rank_correlation_coefficient(audio_feature_ranks, chart_ranks)

    create_scatter_plot(peak_chart_positions, audio_feature_values, filename, f'{genre.capitalize()}', f'n={len(songs_with_audio_features)} ρ={corr_coeff}', 'Peak chart position', audio_feature_name.capitalize())
    return corr_coeff


# spearman
def get_rank_correlation_coefficient(rank_x: List[int], rank_y: List[int]) -> float:
    rg_line_x = (len(rank_x) + 1)/2
    rg_line_y = (len(rank_y) + 1)/2
    dividend = 0
    for i in range(len(rank_x)):
        dividend += (rank_x[i] - rg_line_x)*(rank_y[i]-rg_line_y)

    divisor_sum_x = 0
    divisor_sum_y = 0
    for i in range(len(rank_x)):
        divisor_sum_x += (rank_x[i] - rg_line_x)**2
        divisor_sum_y += (rank_y[i] - rg_line_y)**2
    divisor = sqrt(divisor_sum_x)*sqrt(divisor_sum_y)

    return dividend/divisor


# returns true if correlation is statistically significant
def t_test(rho, n):
    t_value = rho * sqrt((n - 2) / (1 - rho * rho))
    p_value = scipy.stats.t.sf(abs(t_value), n-2)
    print(p_value)
    return p_value < 0.05


def get_rank_correlation_coefficient_from_value_lists(value_x: List[int], value_y: List[int]) -> float:
    rank_x = scs.rankdata(value_x)
    rank_y = scs.rankdata(value_y)

    return get_rank_correlation_coefficient(rank_x, rank_y)


def create_genre_scatter_plots(songs: List[Song]):

    t_test_parameters = {}
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]

    for audio_feature in SpotifySongData.audio_feature_keys:
        if audio_feature != 'mode' and audio_feature != 'key':
            rho = create_audio_feature_scatter_plot(songs_with_audio_features, audio_feature, f'all_{audio_feature}.png')
            t_test_parameters[f'all_{audio_feature}'] = {'r': rho, 'n': len(songs_with_audio_features)}

    genres_dictionary = get_genres_dictionary(songs_with_audio_features)

    for genre in most_common_genres:

        genre_songs = genres_dictionary[genre]

        for audio_feature in SpotifySongData.audio_feature_keys:
            if audio_feature != 'mode' and audio_feature != 'key':
                rho = create_audio_feature_scatter_plot(genre_songs, audio_feature, f'{genre}_{audio_feature}.png', genre)
                t_test_parameters[f'{genre}_{audio_feature}'] = {'r': rho, 'n': len(genre_songs)}

    return t_test_parameters


def get_median_chart_positions(songs: List[Song], audio_feature: str):
    dict = {}
    #dict = defaultdict({'median': [],  'len': -1})

    grouped_songs = defaultdict(list)
    medians = {}
    lengths = {}
    for song in songs:
        if song.spotify_song_data.audio_features_dictionary is not None:
            audio_feature_value = song.spotify_song_data.audio_features_dictionary[audio_feature]
            grouped_songs[audio_feature_value].append(song.peak_chart_position)


    for key, value in grouped_songs.items():
        median = statistics.median(value)
        medians[key] = median
        lengths[key] = len(value)
        dict[key] = {}
        dict[key]['median'] = median
        dict[key]['len'] = len(value)
    return dict


def get_genres_dictionary(songs: List[Song], exclude_songs_without_spotify_data = False):
    genres_dictionary = defaultdict(list)
    for song in songs:
        for genre in song.genres:
            genres_dictionary[genre].append(song)

    return genres_dictionary


def get_decades_dictionary(songs: List[Song]):
    decades_dict = defaultdict(list)
    for song in songs:
        decades_dict[song.chart_year // 10 % 10].append(song)

    len_dict = {}
    for k, v in decades_dict.items():
        len_dict[k] = len(v)
    return decades_dict

# BAR PLOTS
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def get_audio_feature_median(songs: List[Song], audio_feature: str):
    audio_feature_values = [song.spotify_song_data.audio_features_dictionary[audio_feature] for song in songs]
    median = statistics.median(audio_feature_values)
    return median


def create_bar_plot(values, filename: str):
    global figure_number

    fig = plt.figure(figure_number)
    figure_number += 1
    ax = fig.add_axes([0, 0, 1, 1])
    ax.bar([i for i in range(len(values))], values)
    plt.show()
    #plt.savefig('../data/plots/bar_plots/' + filename)
    #plt.close()


def create_audio_feature_bar_plot(songs: List[Song], audio_feature: str):
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
    songs_with_audio_features.sort(key=lambda song: song.peak_chart_position)
    sorted_chunks = list(split(songs_with_audio_features, 10))
    medians = [get_audio_feature_median(chunk, audio_feature) for chunk in sorted_chunks]

# TABLES

def create_key_table(songs: List[Song], filename: str, genre: str = None):
    plt.figure(figsize=(8, 3))

    result = get_median_chart_positions(songs, 'key')
    sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1]['median'])}

    keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    sorted_keys = [keys[res] for res in sorted_result.keys()]
    data = [[res['median'] for res in sorted_result.values()],
            sorted_keys,
            [res['len'] for res in sorted_result.values()]]

    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = plt.table(
        cellText=data,
        rowLabels=['Chartposition', 'Tonart', 'n'],
        cellLoc='center',
        loc='upper left')

    genre_str = '' if genre is None else f'({genre.capitalize()})'
    plt.title(f'Höchste Chartposition (Median) nach Tonart {genre_str}',
                 fontweight="bold")

    plt.savefig('../data/img/tables/' + filename, bbox_inches="tight")
    plt.show()


def create_mode_table(songs: List[Song], filename: str, genre: str = None):
    plt.figure(figsize=(6, 1))

    result = get_median_chart_positions(songs, 'mode')
    val1 = ['Moll', 'Dur']
    val3 = [[res['median'] for res in result.values()],
            [val1[res] for res in result.keys()],
            [res['len'] for res in result.values()]]

    fig, ax = plt.subplots()
    ax.set_axis_off()
    table = plt.table(
        cellText=val3,
        rowLabels=['Chartposition', 'Tongeschlecht', 'n'],
        colWidths=[0.3, 0.3, 0.3],
        cellLoc='center',
        loc='upper center')

    genre_str = '' if genre is None else f'({genre.capitalize()})'

    plt.title(f'Höchste Chartposition (Median) nach Tongeschlecht {genre_str}',
                 fontweight="bold")


    plt.axis('off')
    plt.grid('off')
    plt.savefig('../data/img/tables/' + filename, bbox_inches="tight")
    plt.show()
