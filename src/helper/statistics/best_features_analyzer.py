# determine best features by low pvalue and high correlation
import pandas as pd
from scipy.stats import stats

from src.helper.statistics_helper import analyze_feature_correlation
from src.helper.years_scatterplot import TestResult
from src.models.song_feature import SongFeature
from src.shared import shared
from src.shared.shared import init_song_features


def get_best_features(csv_file_path, analyzed_feature, max_pvalue=0.01, spearman=True):

    test_results = []
    init_song_features()

    df = pd.read_csv(csv_file_path)

    #df = pd.read_csv('./../data/csv/song_features.csv')

    analyzed_feature_values = df[analyzed_feature].tolist()

    for column_name in df:
        feature: SongFeature = song_features.song_features_dict.get(column_name, None)
        if feature == None:
            continue
        if not feature.is_numerical or \
                column_name == 'year' or \
                column_name == 'decade' or \
                column_name == 'mode' or \
                column_name == 'spotify_popularity' or \
                column_name == 'chart_pos':
            continue

        column_values = df[column_name].tolist()

        if not feature.is_boolean:
            test_result = analyze_feature_correlation(analyzed_feature_values, column_values, feature.feature_id, spearman)
        else:
            test_result_raw = stats.pointbiserialr(analyzed_feature_values, column_values)
            test_result = TestResult(feature.feature_id, test_result_raw.correlation, test_result_raw.pvalue)

        test_results.append(test_result)

    results_low_pvalue = [res for res in test_results if res.pvalue <= max_pvalue]
    sorted_results = sorted(results_low_pvalue, key=lambda res: abs(res.correlation), reverse=True)

    res_str = " \\\\ \n \\hline\n".join(str(res) for res in sorted_results)
    res_str += ' \\\\'

    features_names = [feature.feature_id for feature in sorted_results]

    return features_names


def get_best_features_years(csv_file_path, max_pvalue=0.01):
    return get_best_features(csv_file_path, 'year', max_pvalue, False)
