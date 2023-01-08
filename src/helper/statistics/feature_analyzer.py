import sys
from collections import defaultdict
from typing import List

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency

from src.helper.file_helper import feature_file_path
from src.helper.genres import genres_genres
from src.helper.img.barplot import create_stacked_barplot
from src.helper.img.boxplot import create_boxplot
from src.helper.img.scatterplot import create_scatter_plot
from src.helper.statistics_helper import analyze_feature_correlation
from src.models.song import Song, most_common_genres
from src.models.song_feature import SongFeature
from src.models.test_result import TestResult
from src.shared import shared
import pandas as pd
from scipy import stats
import seaborn as sns

# TODO do these separately
non_musical_features = ['decade', 'year', 'artist', 'chart_pos', 'genre', 'spotify_popularity', 'spotify_id', 'genre_groups']

def analyze_all_features(redraw_plots=True):
    dataframe = shared.mcgill_df
    result_dict = {}
    result_dict['genre'] = compare_features_among_genres(dataframe, 0.001, redraw_plots)
    result_dict['year'] = analyze_features(dataframe, 'year', True, 0.2, 0.05, redraw_plots)
    result_dict['chart_pos'] = analyze_features(dataframe, 'chart_pos', False, 0.075, 0.1, redraw_plots)
    result_dict['spotify_popularity'] = analyze_features(dataframe, 'spotify_popularity', False, 0.1, 0.01, redraw_plots)
    return result_dict


def analyze_features(dataframe, feature_to_analyze_id, use_pearson, minimum_correlation, maximum_p_value, redraw_plots):
    non_instrumenal_songs_df = dataframe[dataframe['sadness'].notnull()]
    v = len(non_instrumenal_songs_df)

    feature_to_analyze = shared.song_features_dict[feature_to_analyze_id]
    features: List[SongFeature] = shared.song_features_dict.values()
    ordinal_features, nominal_features = [], []
    for feature in features:
        (ordinal_features, nominal_features)[feature.is_nominal].append(feature)

    # draw all scatterplots for ordinal data
    feature_to_analyze_values = dataframe[feature_to_analyze.feature_id].values
    feature_name1 = feature_to_analyze.display_name

    nominal_test_results = []

    # draw barplots for nominal data
    for feature in nominal_features:
        if feature.feature_id in non_musical_features:
            continue

        if feature.feature_id != 'decade' and feature.feature_id != 'genre':
            grouped_features = dataframe.groupby(feature.feature_id)
            labels = grouped_features.groups.keys()
            if feature.nominal_labels is not None:
                labels = [feature.nominal_labels[i] for i in labels]

            groups = dataframe.groupby(feature.feature_id)[feature_to_analyze_id].apply(list)

            title = f'{feature_name1} nach ${feature.latex_name}$ {feature.feature_id}'

            stat, pvalue, med, tbl = stats.median_test(*groups)
            nominal_test_results.append(TestResult(feature, pvalue))
            median_test_result_str = f'Mood\'s median test; χ2={stat:.3f}; p={pvalue:.3f}'

            if redraw_plots:
                create_boxplot(groups, labels, title, median_test_result_str, f'{feature_to_analyze_id}_{feature.latex_id}.jpg', f'correlation/{feature_to_analyze_id}', ylabel=feature_name1, figsize=(4.48, 3.36))

    test_results = []

    for feature in ordinal_features:
        if feature.feature_id not in non_musical_features and \
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
                                         f'{feature_name1} vs. ${feature.latex_name}$ {feature.feature_id}', f'{feature_to_analyze_id}_{feature.latex_id}.jpg', test_result,
                                         f'correlation/{feature_to_analyze_id}', use_pearson)

    filtered_test_results = [test_result for test_result in test_results if abs(test_result.correlation) >= minimum_correlation and test_result.pvalue <= maximum_p_value]
    filtered_nominal_test_results = [test_result for test_result in nominal_test_results if test_result.pvalue <= maximum_p_value]

    print(feature_to_analyze_id)
    latex_names = '; '.join([f'${result.feature.latex_name}$' for result in filtered_test_results])
    # print(latex_names)
    feature_ids = ','.join([f'${result.feature.feature_id}$' for result in filtered_test_results])
    print(f'[{feature_ids}]')

    return filtered_test_results + filtered_nominal_test_results


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

# TODO move to common helper class
def get_genre_group_string(group):
    return '-'.join([genre.capitalize() for genre in group.split('-')])

def compare_features_among_genres(df, maximum_p_value, redraw_plots):
    # filter data frame
    df = df[~df['genre_groups'].isnull()]
    genre_dict = defaultdict(list)

    grouped_df = df.groupby('genre_groups')
    for group, group_df in grouped_df:
        print(f'{get_genre_group_string(group)} n=({len(group_df)})')

    # for song in df['genre_groups']:
    #     genre_dict[song[]].append()
    features: List[SongFeature] = shared.song_features_dict.values()
    ordinal_features, nominal_features = [], []
    for feature in features:
        (ordinal_features, nominal_features)[feature.is_nominal].append(feature)

    ordinal_features = [feature for feature in ordinal_features if feature.feature_id not in non_musical_features and feature.is_numerical]
    nominal_features = [feature for feature in nominal_features if feature.feature_id not in non_musical_features]

    test_results = []
    # test_results += analyze_ordinal_features_for_genres(df, ordinal_features, redraw_plots)
    test_results += analyze_nominal_features_for_genres(df, nominal_features, redraw_plots)

    # filter test results
    filtered_test_results = [result for result in test_results if result.pvalue <= maximum_p_value]

    return filtered_test_results


def analyze_nominal_features_for_genres(df, nominal_features, redraw_plots):
    grouped_df = df.groupby('genre_groups')
    test_results = []

    for feature in nominal_features:
        # bar_values = []


        group_keys = genres_genres
        grouped_features = df.groupby(feature.feature_id)
        feature_group_keys = grouped_features.groups.keys()
        bar_values = [[] for _ in range(len(feature_group_keys))]
        labels = []

        for genre, genre_df in grouped_df:
            labels.append(genre.capitalize())

            for j, group_key in enumerate(feature_group_keys):
                n = len(genre_df)

                grouped_groups_df = genre_df.groupby(feature.feature_id)

                try:
                    group = len(grouped_groups_df.get_group(group_key))

                    perc_value = group / n
                    bar_values[j].append(perc_value)

                except Exception:
                    # zero group members
                    bar_values[j].append(0)

        # execute test
        genre_ids = df['genre_groups'].values
        feature_values = df[feature.feature_id].values

        contigency = pd.crosstab(genre_ids, feature_values)

        stat, p, dof, expected = chi2_contingency(contigency)
        test_results.append(TestResult(feature, p))

        if redraw_plots:

            # bar_values.append
            labels = [get_genre_group_string(genre) for genre in genres_genres]
            legend = [feature.nominal_labels[i] for i in range(len(feature_group_keys))] if feature.nominal_labels is not None else group_keys

            suptitle = f'$\chi^2$-Test, $\chi^2$({dof}, n={len(feature_values)})={stat:.3f}, p={p:.3f}'
            # suptitle = ''

            create_stacked_barplot(bar_values, labels, legend,
                                   f'${feature.latex_name}$ {feature.feature_id} nach Musikrichtung', suptitle, f'genre_{feature.latex_id}.jpg', f'correlation/genre', figsize=(4.48, 3.36))

    return test_results

def analyze_ordinal_features_for_genres(df, ordinal_features, redraw_plots):

    grouped_df_all = df.groupby('genre_groups')
    setiment_df = df[~df['joy'].isnull()]
    grouped_df_sentiments = setiment_df.groupby('genre_groups')

    test_results = []

    for feature in ordinal_features:
        box_plot_values = []
        labels = []

        grouped_df = grouped_df_sentiments if feature.is_sentiment_feature else grouped_df_all

        for genre, genre_df in grouped_df:
            labels.append(genre.capitalize())
            feature_values = genre_df[feature.feature_id].values
            box_plot_values.append(feature_values)

        # TODO check if sorted correctly (probably not)

        stat, pvalue, med, tbl = stats.median_test(*box_plot_values)
        test_result = TestResult(feature, pvalue)
        test_results.append(test_result)

        if redraw_plots:
            labels = [get_genre_group_string(g) for g in labels]
            median_test_result_str = f'Mood\'s median test; χ2={stat:.3f}; p={pvalue:.3f}'
            create_boxplot(box_plot_values, labels, f'${feature.latex_name}$ {feature.feature_id} nach Genre', median_test_result_str, f'genre_{feature.latex_id}.jpg',
                           f'correlation/genre', ylabel=f'${feature.latex_name}$', figsize=(4.48, 3.36))

    return test_results



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
