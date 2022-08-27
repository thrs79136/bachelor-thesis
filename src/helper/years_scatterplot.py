import pandas as pd

from src.helper.statistics_helper import analyze_feature_correlation
from src.models.song_feature import SongFeature
from src.shared import song_features
from src.shared.song_features import init_song_features

class TestResult:
    def __init__(self, feature_id, test_result):
        self.feature_id = feature_id
        self.test_result = test_result

def draw_year_scatter_plots():

    test_results = []
    init_song_features()
    dictionaries.song_features_dict

    df = pd.read_csv('./../data/csv/song_features.csv')

    years = df['year'].tolist()

    for column_name in df:
        feature: SongFeature = dictionaries.song_features_dict[column_name]
        if not feature.is_numerical or column_name == 'year' or column_name == 'decade':
            continue

        column_values = df[column_name].tolist()

        result = analyze_feature_correlation(years, column_values, 'Jahr', feature.feature_display_name, feature.feature_display_name, f'{feature.feature_id}.jpg', directory='years', draw_plot=False)
        test_result = TestResult(column_name, result)
        test_results.append(test_result)

    results_low_pvalue = [res for res in test_results if res.test_result[1] <= 0.01]
    sorted_results = sorted(results_low_pvalue, key=lambda res: abs(res.test_result[0]), reverse=True)
    feature_names = [res.feature_id for res in sorted_results]
    x =42


# TODO remove from here
def test_chart_pos():
    test_results = []
    init_song_features()
    dictionaries.song_features_dict

    df = pd.read_csv('./../data/csv/song_features.csv')

    chart_positions = df['spotify_popularity'].tolist()


    for column_name in df:
        feature: SongFeature = dictionaries.song_features_dict[column_name]
        if not feature.is_numerical or column_name == 'year' or column_name == 'decade':
            continue

        column_values = df[column_name].tolist()

        result = analyze_feature_correlation(chart_positions, column_values, 'Jahr', feature.feature_display_name, feature.feature_display_name, f'{feature.feature_id}.jpg', directory='years', use_pearson=False)
        test_result = TestResult(column_name, result)
        test_results.append(test_result)

    results_low_pvalue = [res for res in test_results if res.test_result[1] <= 0.05]
    sorted_results = sorted(results_low_pvalue, key=lambda res: abs(res.test_result[0]), reverse=True)
    feature_names = [res.feature_id for res in sorted_results]

    x = 42