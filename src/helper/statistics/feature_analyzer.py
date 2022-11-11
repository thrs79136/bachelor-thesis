from typing import List

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

from src.helper.file_helper import feature_file_path
from src.helper.img.barplot import create_stacked_barplot
from src.helper.img.boxplot import create_boxplot
from src.helper.img.scatterplot import create_scatter_plot
from src.helper.statistics_helper import analyze_feature_correlation
from src.models.song import Song, most_common_genres
from src.models.song_feature import SongFeature
from src.shared import shared
import pandas as pd
from scipy import stats
import seaborn as sns

# TODO do these separately
non_y_axis_features = ['decade', 'year', 'artist', 'chart_pos', 'genre', 'spotify_popularity']

# TODO only use this function in main
def analyze_all_features(redraw_plots=True):
    dataframe = pd.read_csv(feature_file_path)
    # compare_features_among_genres(dataframe)
    result_dict = {}
    result_dict['year'] = analyze_features(dataframe, 'year', True, 0.2, 0.05, redraw_plots)
    result_dict['chart_pos'] = analyze_features(dataframe, 'chart_pos', False, 0.08, 0.1, redraw_plots)
    result_dict['spotify_popularity'] = analyze_features(dataframe, 'spotify_popularity', False, 0.1, 0.05, redraw_plots)
    return result_dict


def analyze_features(dataframe, feature_to_analyze_id, use_pearson, minimum_correlation, maximum_p_value, redraw_plots):
    non_instrumenal_songs_df = dataframe[dataframe['sadness'].notnull()]

    feature_to_analyze = shared.song_features_dict[feature_to_analyze_id]
    features: List[SongFeature] = shared.song_features_dict.values()
    ordinal_features, nominal_features = [], []
    for feature in features:
        (ordinal_features, nominal_features)[feature.is_nominal].append(feature)

    # draw all scatterplots for ordinal data
    feature_to_analyze_values = dataframe[feature_to_analyze.feature_id].values
    feature_name1 = feature_to_analyze.display_name

    # draw barplots for nominal data
    for feature in nominal_features:
        if feature.feature_id != 'decade' and feature.feature_id != 'genre':
            grouped_features = dataframe.groupby(feature.feature_id)
            labels = grouped_features.groups.keys()
            if feature.nominal_labels is not None:
                labels = [feature.nominal_labels[i] for i in labels]

            groups = dataframe.groupby(feature.feature_id)[feature_to_analyze_id].apply(list)

            title = f'{feature_name1} nach ${feature.latex_name}$ {feature.display_name}'

            stat, pvalue, med, tbl = stats.median_test(*groups)
            median_test_result_str = f'Mood\'s median test; χ2={stat:.3f}; p={pvalue:.3f}'

            if redraw_plots:
                create_boxplot(groups, labels, title, median_test_result_str, f'{feature_to_analyze_id}_{feature.latex_id}.jpg', f'correlation/{feature_to_analyze_id}', ylabel=feature_name1)

    test_results = []

    for feature in ordinal_features:
        if feature.feature_id not in non_y_axis_features and \
                feature.is_numerical is True and \
                feature.is_boolean is False:
            # section_repetitions
            if feature.is_sentiment_feature is False:
                x_values = feature_to_analyze_values
                y_values = dataframe[feature.feature_id].values
            else:
                x_values = non_instrumenal_songs_df[feature_to_analyze.feature_id].values
                y_values = non_instrumenal_songs_df[feature.feature_id].values
            feature_name2 = feature.display_name
            test_result = analyze_feature_correlation(x_values, y_values, use_pearson, feature)
            test_results.append(test_result)
            if redraw_plots:
                draw_feature_scatterplot(x_values, y_values, feature_name1, f'${feature.latex_name}$',
                                         f'{feature_name1} vs. ${feature.latex_name}$ {feature_name2}', f'{feature_to_analyze_id}_{feature.latex_id}.jpg', test_result,
                                         f'correlation/{feature_to_analyze_id}', use_pearson)

    filtered_test_results =  [test_result for test_result in test_results if abs(test_result.correlation) >= minimum_correlation and test_result.pvalue <= maximum_p_value]
    latex_names = '; '.join([f'${result.feature.latex_name}$' for result in filtered_test_results])
    print(feature_to_analyze_id)
    print(latex_names)
    return filtered_test_results


def create_correlation_matrix(features):
    # matrix = [[] for _ in range(len(features))]
    matrix = np.zeros((len(features), len(features)))
    for i, feature in enumerate(features):
        for j, feature2 in enumerate(features):
            x_values = shared.mcgill_df[feature.feature_id].values
            y_values = shared.mcgill_df[feature2.feature_id].values
            test_result = analyze_feature_correlation(x_values, y_values, True, feature)
            matrix[i][j] = test_result.correlation


    ordered_features = [features[0]]
    current_feature_idx = 0
    while len(ordered_features) != len(features):
        max_corr = -1
        best_feature = None
        best_feature_idx = -1
        if features[current_feature_idx].feature_id == 'major_percentage':
            x = 42
        for j, f2 in enumerate(features):
            if current_feature_idx == j:
                continue
            if matrix[current_feature_idx, j] > max_corr and f2 not in ordered_features:
                max_corr = matrix[current_feature_idx,j]
                best_feature = f2
                best_feature_idx = j
        if best_feature is None:
            x = 42
        current_feature_idx = best_feature_idx
        ordered_features.append(best_feature)

    print([feature.feature_id for feature in ordered_features])
    x = 42


# creates box plots
def compare_features_among_genres(df):
    genres = []

    for value in df['genre']:
        added_genre = None
        for i, genre in enumerate(most_common_genres):
            if genre in value:
                added_genre = i
                break
        genres.append(added_genre)

    df['single_genre'] = genres
    single_genre_df = df[df['single_genre'].notnull()]

    non_instrumenal_songs_df = df[df['sadness'].notnull()]

    genre_dict = {}
    genre_dict_sentiments = {}

    for genre in most_common_genres:
        genre_songs = df[df['genre'].str.contains(genre)]
        genre_songs_non_instrumental = non_instrumenal_songs_df[non_instrumenal_songs_df['genre'].str.contains(genre)]
        genre_dict[genre] = genre_songs
        genre_dict_sentiments[genre] = genre_songs_non_instrumental

    feature_to_analyze = shared.song_features_dict['genre']
    features: List[SongFeature] = shared.song_features_dict.values()
    ordinal_features, nominal_features = [], []
    for feature in features:
        (ordinal_features, nominal_features)[feature.is_nominal].append(feature)

    for feature in nominal_features:
        if feature.feature_id not in non_y_axis_features:
            # bar_values = []

            group_keys = list(genre_dict.values())[0].groupby(feature.feature_id).groups.keys()
            bar_values = [[] for _ in range(len(group_keys))]

            x = len(genre_dict.items())
            y = len(group_keys)

            for i, (key, dataframe) in enumerate(genre_dict.items()):
                # labels.append(key)
                grouped_features = dataframe.groupby(feature.feature_id)
                # labels = grouped_features.groups.keys()

                perc_values = []
                for j, group_key in enumerate(group_keys):
                    n = len(dataframe)
                    group = len(grouped_features.get_group(group_key))
                    perc_value = group/n
                    bar_values[j].append(perc_value)
                    x = 42
#                   perc_values.append(group/n)
                x = 42



            # execute test
            genre_ids = single_genre_df['single_genre'].values
            feature_values = single_genre_df[feature.feature_id].values

            contigency = pd.crosstab(genre_ids, feature_values)

            stat, p, dof, expected = chi2_contingency(contigency)
            x = 42

            # bar_values.append
            labels = [label.capitalize() for label in list(genre_dict.keys())]
            legend = [feature.nominal_labels[i] for i in group_keys] if feature.nominal_labels is not None else group_keys

            # suptitle = f'$\chi^2$-Test, $\chi^2$({dof}, n={len(feature_values)})={stat:.3f}, p={p:.3f}'
            suptitle = ''

            create_stacked_barplot(bar_values, labels, legend, f'${feature.latex_name}$ {feature.display_name} nach Musikrichtung', suptitle)
            # if len(legend) == 2:
            #     return


    # TODO remove
    return

    for feature in ordinal_features:
        if feature.feature_id not in non_y_axis_features:
            box_plot_values = []

            dict = genre_dict_sentiments if feature.is_sentiment_feature else genre_dict

            for key, value in dict.items():
                res = value[feature.feature_id].values
                box_plot_values.append(res)
            try:
                stat, pvalue, med, tbl = stats.median_test(*box_plot_values)
                median_test_result_str = f'Mood\'s median test; χ2={stat:.3f}; p={pvalue:.3f}'
                #
                create_boxplot(box_plot_values, [g.capitalize() for g in most_common_genres], f'${feature.latex_name}$ {feature.display_name} nach Genre', median_test_result_str, f'genre_{feature.latex_id}.jpg',
                               f'correlation/genre', ylabel=feature.display_name)
            except Exception:
                print('except')
                x = 42




    # genres_dict = get_common_genres_dictionary(songs)
    # box_plot_values = []
    #
    # feature_fn = feature.feature_fn
    # parameters = feature.parameters
    #
    # for song_list in genres_dict.values():
    #     feature_expr = []
    #     for song in song_list:
    #         parameter_list = [song] + parameters
    #         feature_expr.append(feature_fn(*parameter_list))
    #
    #     box_plot_values.append(feature_expr)
    #
    # title = feature.display_name
    # filename = f'{feature.feature_id}.jpg'
    #
    # oneway_result = stats.f_oneway(*box_plot_values)
    # test_result_str = f'One-Way ANOVA test; F={oneway_result.statistic:.3f}; p={oneway_result.pvalue:.3f}'
    #
    # stat, pvalue, med, tbl = stats.median_test(*box_plot_values)
    # median_test_result_str = f'Mood\'s median test; χ2={stat:.3f}; p={pvalue:.3f}'
    #
    # test_result_str += f'\n{median_test_result_str}'
    #
    # labels = [key.capitalize() for key in genres_dict.keys()]
    #
    # pairwise_result = {}
    # if oneway_result.pvalue < 0.05:
    #     for i, genre in enumerate(most_common_genres):
    #         for j in range(i + 1, len(most_common_genres)):
    #             other_genre = most_common_genres[j]
    #             scores1 = box_plot_values[i]
    #             scores2 = box_plot_values[i + 1]
    #             stat, pvalue = stats.mood(scores1, scores2)
    #             pairwise_result[f'{genre}-{other_genre}'] = pvalue
    #
    # create_boxplot(box_plot_values, labels, title, test_result_str, filename, 'genres')



def draw_feature_scatterplot(x_values, y_values, x_label, y_label, title, filename, test_result, directory=None, use_pearson=True):

    suptitle = f'n={len(x_values)} r={"{0:.3f}".format(test_result.correlation)}, p={"{0:.3f}".format(test_result.pvalue)}'

    create_scatter_plot(x_values,
                        y_values,
                        filename,
                        title,
                        suptitle,
                        x_label,
                        y_label,
                        directory)
