import pickle
import statistics
from collections import defaultdict
from math import sqrt

import scipy
from scipy import stats
from typing import List
from matplotlib import pyplot as plt

from src.helper.img.boxplot import create_boxplot
from src.helper.img.scatterplot import create_scatter_plot
from src.models.song import Song
from src.models.song_feature import SongFeature
from src.models.spotify_song_data import SpotifySongData
from scipy.stats import chi2

figure_number = 0
most_common_genres = ['rock', 'pop', 'soul', 'country', 'blues']


def analyze_feature_correlation(x_values, y_values, x_label, y_label, title, filename, directory=None, use_pearson=True, draw_plot=True):

    if use_pearson:
        test_result = stats.pearsonr(x_values, y_values)
        suptitle = f'n={len(x_values)} r={test_result[0]}, p={test_result[1]}'
    else:
        test_result = stats.spearmanr(x_values, y_values)
        suptitle = f'n={len(x_values)} r={test_result.correlation}, p={test_result.pvalue}'

    if draw_plot:
        create_scatter_plot(x_values,
                            y_values,
                            filename,
                            title,
                            suptitle,
                            x_label,
                            y_label,
                            directory)

    return test_result



def analyze_song_feature_correlation_all_genres(songs: List[Song], get_feature_fn, feature_name, directory=''):
    # all songs grouped together
    analyze_song_feature_correlation(songs, get_feature_fn, feature_name, directory=directory)

    genres_dict = get_genres_dictionary(songs)

    # grouped by genre
    for genre in most_common_genres:
        analyze_song_feature_correlation(genres_dict[genre], get_feature_fn, feature_name, genre, directory)


# creates box plots
def compare_feature_among_genres(songs: List[Song], feature: SongFeature):
    genres_dict = get_common_genres_dictionary(songs)
    box_plot_values = []

    feature_fn = feature.feature_fn
    parameters = feature.parameters

    for song_list in genres_dict.values():
        feature_expr = []
        for song in song_list:
            parameter_list = [song] + parameters
            feature_expr.append(feature_fn(*parameter_list))

        box_plot_values.append(feature_expr)

    title = feature.feature_display_name
    filename = f'{feature.feature_id}.jpg'

    oneway_result = stats.f_oneway(*box_plot_values)
    test_result_str = f'One-Way ANOVA test; F={oneway_result.statistic:.3f}; p={oneway_result.pvalue:.3f}'

    stat, pvalue, med, tbl = stats.median_test(*box_plot_values)
    median_test_result_str = f'Mood\'s median test; χ2={stat:.3f}; p={pvalue:.3f}'

    test_result_str += f'\n{median_test_result_str}'

    labels = [key.capitalize() for key in genres_dict.keys()]

    pairwise_result = {}
    if oneway_result.pvalue < 0.05:
        for i, genre in enumerate(most_common_genres):
            for j in range(i + 1, len(most_common_genres)):
                other_genre = most_common_genres[j]
                scores1 = box_plot_values[i]
                scores2 = box_plot_values[i + 1]
                stat, pvalue = stats.mood(scores1, scores2)
                pairwise_result[f'{genre}-{other_genre}'] = pvalue

    create_boxplot(box_plot_values, labels, title, test_result_str, filename, 'genres')


def analyze_song_groups(songs: List[Song], get_groups_fn, title, filename, groups_count=None, excluded_groups=None,
                        group_order=None,
                        box_plot_values_fn=None, use_spotify_popularity=True):
    groups_songs_dict = defaultdict(list)

    for song in songs:
        one_or_multiple_groups = get_groups_fn(song)
        if isinstance(one_or_multiple_groups, set) or isinstance(one_or_multiple_groups, list):
            for group in one_or_multiple_groups:
                groups_songs_dict[group].append(song)
        else:
            groups_songs_dict[one_or_multiple_groups].append(song)

    groups_for_analysis = []

    if group_order is None:
        count = 0
        groups_songs_sorted = sorted(groups_songs_dict.items(), key=lambda x: len(x[1]), reverse=True)

        for group in groups_songs_sorted:
            if excluded_groups is None or group[0] not in excluded_groups:
                count += 1
                groups_for_analysis.append(group)
                if groups_count is not None and count == groups_count:
                    break
    else:
        for group_id in list(group_order):
            groups_for_analysis.append((group_id, groups_songs_dict[group_id]))

    if box_plot_values_fn is None:
        # default use chart positions
        if use_spotify_popularity:
            box_plot_values = [get_spotify_popularity_list(group[1]) for group in groups_for_analysis]
        else:
            box_plot_values = [get_peak_chart_position_list(group[1]) for group in groups_for_analysis]
    else:
        box_plot_values = []
        for group in groups_for_analysis:
            feature_list = [box_plot_values_fn(song) for song in group[1]]
            box_plot_values.append(feature_list)

    labels = [f'{group[0]}' for group in groups_for_analysis]

    if len(box_plot_values) > 2:
        kruskal_result = stats.kruskal(*box_plot_values)
        test_res_str = f'Kruskal-Wallis test; H={kruskal_result.statistic:.3f}; p={kruskal_result.pvalue:.3f}'
    else:
        test_res = stats.mannwhitneyu(*box_plot_values)
        test_res_str = f'Mann-Whitney U rank test; H={test_res.statistic:.3f}; p={test_res.pvalue:.3f}'

    create_boxplot(box_plot_values, labels, title, test_res_str, filename)


transitions = []


class Transition:
    def __init__(self, transition, corr, pvalue):
        self.transition = transition
        self.corr = corr
        self.pvalue = pvalue


def analyze_song_feature_correlation(songs: List[Song], get_feature_fn, feature_name, genre='all', directory='',
                                     feature_fn_parameters=None, use_spotify_popularity=True):
    global transitions

    if not use_spotify_popularity:
        x_feature_values = [song.peak_chart_position for song in songs]
        x_label = 'Höchste Chartplatzierung'
    else:
        x_feature_values = [song.get_spotify_popularity() for song in songs]
        x_label = 'Spotify Popularity'

    feature_expressions = []
    for song in songs:
        parameters = [song]
        if feature_fn_parameters is not None:
            parameters += feature_fn_parameters

        feature_expressions.append(get_feature_fn(*parameters))

    # feature_expressions = [get_feature_fn(song) for song in songs]

    spearman_result = stats.spearmanr(x_feature_values, feature_expressions)

    filename = f"{feature_name.lower().replace(' ', '_')}_{genre}{'_s' if use_spotify_popularity else ''}.png"
    title = feature_name
    if genre != 'all':
        title += f' (Musikrichtung: {genre.capitalize()})'
    else:
        title += ' (Alle Musikrichtungen)'

    # if spearman_result.pvalue >= 0.02:
    #     return

    create_scatter_plot(x_feature_values,
                        feature_expressions,
                        filename,
                        title,
                        f'n={len(songs)}; r={"{0:.3f}".format(spearman_result.correlation)}; p={"{0:.3f}".format(spearman_result.pvalue)}',
                        x_label,
                        feature_name,
                        directory)


def get_peak_chart_position_list(songs: List[Song]) -> List[int]:
    return [song.peak_chart_position for song in songs]


def get_spotify_popularity_list(songs: List[Song]) -> List[int]:
    return [song.get_spotify_popularity() for song in songs]


def get_audio_feature_ranks(songs: List[Song], audio_feature: str):
    audio_feature_values = [song.spotify_song_data.audio_features_dictionary[audio_feature] for song in
                            songs]
    audio_feature_ranks = stats.rankdata(audio_feature_values)
    return audio_feature_ranks


def create_audio_feature_scatter_plot(songs: List[Song], audio_feature_name: str, filename: str,
                                      genre: str = 'All genres'):
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]

    peak_chart_positions = [song.peak_chart_position for song in songs_with_audio_features]
    audio_feature_values = [song.spotify_song_data.audio_features_dictionary[audio_feature_name] for song in
                            songs_with_audio_features]
    spearman_result = stats.spearmanr(peak_chart_positions, audio_feature_values)

    if spearman_result.pvalue < 0.05:
        print(f'{filename} statistically significant')

    create_scatter_plot(peak_chart_positions, audio_feature_values, filename, f'{genre.capitalize()}',
                        f'n={len(songs_with_audio_features)} r={spearman_result.correlation}, p={spearman_result.pvalue}',
                        'Peak chart position', audio_feature_name.capitalize())


def create_chord_count_scatter_plot(songs: List[Song]):
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
    peak_chart_positions = [song.peak_chart_position for song in songs_with_audio_features]
    different_chords_count = [song.get_different_chords_count() for song in songs]


# spearman
def get_rank_correlation_coefficient(rank_x: List[int], rank_y: List[int]) -> float:
    rg_line_x = (len(rank_x) + 1) / 2
    rg_line_y = (len(rank_y) + 1) / 2
    dividend = 0
    for i in range(len(rank_x)):
        dividend += (rank_x[i] - rg_line_x) * (rank_y[i] - rg_line_y)

    divisor_sum_x = 0
    divisor_sum_y = 0
    for i in range(len(rank_x)):
        divisor_sum_x += (rank_x[i] - rg_line_x) ** 2
        divisor_sum_y += (rank_y[i] - rg_line_y) ** 2
    divisor = sqrt(divisor_sum_x) * sqrt(divisor_sum_y)

    return dividend / divisor


# non parametric alternatives

class TTestResult:
    def __init__(self, significance: bool, t_value):
        self.significance = significance
        self.t_value = t_value


# returns true if correlation is statistically significant
def t_test(rho, n):
    t_value = rho * sqrt((n - 2) / (1 - rho * rho))
    P = scipy.stats.t.sf(abs(t_value), n - 2)
    print(P)
    return TTestResult(P < 0.05, t_value)


def get_rank_correlation_coefficient_from_value_lists(value_x: List[int], value_y: List[int]) -> float:
    rank_x = stats.rankdata(value_x)
    rank_y = stats.rankdata(value_y)

    return get_rank_correlation_coefficient(rank_x, rank_y)


def create_genre_scatter_plots(songs: List[Song]):
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]

    for audio_feature in SpotifySongData.audio_feature_keys:
        if audio_feature != 'mode' and audio_feature != 'key':
            create_audio_feature_scatter_plot(songs_with_audio_features, audio_feature, f'all_{audio_feature}.png')

    genres_dictionary = get_genres_dictionary(songs_with_audio_features)

    for genre in most_common_genres:

        genre_songs = genres_dictionary[genre]

        for audio_feature in SpotifySongData.audio_feature_keys:
            if audio_feature != 'mode' and audio_feature != 'key':
                create_audio_feature_scatter_plot(genre_songs, audio_feature, f'{genre}_{audio_feature}.png', genre)


def get_median_chart_positions(songs: List[Song], audio_feature: str):
    dict = {}

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
        dict[key]['chart_pos_values'] = value
    return dict


def get_genres_dictionary(songs: List[Song]):
    genres_dictionary = defaultdict(list)
    for song in songs:
        for genre in song.genres:
            genres_dictionary[genre].append(song)

    return genres_dictionary


def get_common_genres_dictionary(songs: List[Song]):
    genres_dictionary = defaultdict(list)
    for song in songs:
        for genre in song.genres:
            if genre in most_common_genres:
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
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


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
    # plt.savefig('../data/plots/bar_plots/' + filename)
    # plt.close()


def create_audio_feature_bar_plot(songs: List[Song], audio_feature: str):
    songs_with_audio_features = [song for song in songs if song.spotify_song_data.audio_features_dictionary is not None]
    songs_with_audio_features.sort(key=lambda song: song.peak_chart_position)
    sorted_chunks = list(split(songs_with_audio_features, 10))
    medians = [get_audio_feature_median(chunk, audio_feature) for chunk in sorted_chunks]


# TABLES

def create_key_table(songs: List[Song], filename: str, genre: str = None):
    plt.figure(figsize=(8, 3))

    result = get_median_chart_positions(songs, 'key')
    # kruskal test
    values = result.values()
    grouped_values = [value['chart_pos_values'] for value in values]
    kruskal_result = stats.kruskal(*grouped_values)
    kruskal_res_str = f'Kruskal-Wallis test; H={kruskal_result.statistic:.3f}; p={kruskal_result.pvalue:.3f}'

    sorted_result = {k: v for k, v in sorted(result.items(), key=lambda item: item[1]['median'])}

    keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    sorted_keys = [keys[res] for res in sorted_result.keys()]
    data = [[res['median'] for res in sorted_result.values()],
            sorted_keys,
            [res['len'] for res in sorted_result.values()]]

    fig, ax = plt.subplots()
    ax.set_axis_off()
    plt.table(
        cellText=data,
        rowLabels=['Chartposition', 'Tonart', 'n'],
        cellLoc='center',
        loc='upper left')

    genre_str = '' if genre is None else f'({genre.capitalize()})'
    plt.title(f'Höchste Chartposition (Median) nach Tonart {genre_str}',
              fontweight="bold", y=1.05)
    plt.suptitle(kruskal_res_str, fontsize=10, y=0.91)

    plt.savefig('../data/img/tables/' + filename, bbox_inches="tight")
    plt.show()


def create_mode_table(songs: List[Song], filename: str, genre: str = None):
    plt.figure(figsize=(6, 1))

    result = get_median_chart_positions(songs, 'mode')

    test_result = stats.mannwhitneyu(['TODO'], ['TODO'], method="exact")

    val1 = ['Moll', 'Dur']
    val3 = [[res['median'] for res in result.values()],
            [val1[res] for res in result.keys()],
            [res['len'] for res in result.values()]]

    fig, ax = plt.subplots()
    ax.set_axis_off()
    plt.table(
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


def group_by_year(songs: List[Song]):
    years_dict = defaultdict(list)
    for song in songs:
        years_dict[song.chart_year].append(song)

    return years_dict
