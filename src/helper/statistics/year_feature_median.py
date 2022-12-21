from typing import Union, Any

from pandas import DataFrame
from pandas.io.parsers import TextFileReader

from src.helper.img.lineplot import lineplot
from src.models.song_feature import SongFeature
from src.shared import shared


def get_median(feature: SongFeature):
    df: Union[Union[TextFileReader, DataFrame], Any] = shared.mcgill_df
    median = df.groupby('year')[feature.feature_id].median()
    return median
    #return median.keys().tolist(), median.values


def get_mean(feature: SongFeature):
    return shared.mcgill_df.groupby('year')[feature.feature_id].mean()


def get_normalized_median(feature: SongFeature):
    if feature.feature_id == 'duration_ms':
        pass
    df: Union[Union[TextFileReader, DataFrame], Any] = shared.normalized_mcgill_df
    try:
        median = df.groupby('year')[feature.feature_id].median()
        return median
    except Exception:
        x = 42


def draw_feature_line_plots():
    draw_instrument_line_plots()
    for feature in shared.song_features_dict.values():
        if feature.feature_id not in shared.non_y_axis_features and not feature.is_nominal:
            draw_feature_line_plot(feature)


def draw_feature_line_plot(feature: SongFeature, artist_coordinates=None, dot_legend='', filename_prefix=''):
    median = get_median(feature)
    years, feature_values = median.keys().tolist(), median.values

    subdirectory = 'median_years' if artist_coordinates is None else 'artists'

    lineplot(years, feature_values, 'Jahr', feature.display_name, f'{filename_prefix}{feature.latex_id}.jpg', f'${feature.latex_name}$ {feature.display_name} (Median) im Verlauf der Zeit', '', f'line_plots/{subdirectory}/', dot_coordinates=artist_coordinates, dot_legend=dot_legend)
    x = 42


def draw_instrument_line_plots():
    for feature in shared.song_features_dict.values():
        if not feature.is_boolean:
            continue
        mean = get_mean(feature)
        years, feature_values = mean.keys().tolist(), mean.values
        lineplot(years, feature_values, 'Jahr', feature.display_name, f'{feature.latex_id}.jpg',
                 f'${feature.latex_name}$ {feature.display_name} im Verlauf der Zeit', '',
                 f'line_plots/instrument_years/', dot_legend='')


