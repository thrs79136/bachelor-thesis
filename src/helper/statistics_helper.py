from collections import defaultdict
from scipy import stats
from typing import List

from src.helper.img.scatterplot import create_scatter_plot
from src.models.correlation_test_result import CorrelationTestResult
from src.models.song import Song

figure_number = 0


def analyze_feature_correlation(x_values, y_values, x_label, y_label, title, filename, directory=None, use_pearson=True, draw_plot=True):

    test_result = analyze_feature_correlation(x_values, y_values, use_pearson)

    if use_pearson:
        suptitle = f'n={len(x_values)} r={test_result[0]}, p={test_result[1]}'
    else:
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


# spearman is for ranked data
def analyze_feature_correlation(x_values, y_values, use_pearson, feature):
    if use_pearson:
        test_result = stats.pearsonr(x_values, y_values)
        test_result_cls = CorrelationTestResult(feature, test_result[0], test_result[1])
    else:
        test_result = stats.spearmanr(x_values, y_values)
        test_result_cls = CorrelationTestResult(feature, test_result.correlation, test_result.pvalue)

    return test_result_cls


def analyze_song_feature_correlation(songs: List[Song], get_feature_fn, feature_name, genre='all', directory='',
                                     feature_fn_parameters=None, use_spotify_popularity=True):

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

    spearman_result = stats.spearmanr(x_feature_values, feature_expressions)

    filename = f"{feature_name.lower().replace(' ', '_')}_{genre}{'_s' if use_spotify_popularity else ''}.png"
    title = feature_name
    if genre != 'all':
        title += f' (Musikrichtung: {genre.capitalize()})'
    else:
        title += ' (Alle Musikrichtungen)'


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


# BAR PLOTS
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


def group_by_year(songs: List[Song]):
    years_dict = defaultdict(list)
    for song in songs:
        years_dict[song.chart_year].append(song)

    return years_dict
