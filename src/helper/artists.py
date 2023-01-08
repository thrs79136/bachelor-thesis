import math
from collections import OrderedDict, defaultdict
from typing import List

import pandas as pd

from src.helper.file_helper import feature_file_path
from src.helper.img.barplot import create_barplot
from src.helper.img.lineplot import lineplot
from src.helper.statistics.feature_analyzer import get_genre_group_string
from src.helper.statistics.year_feature_median import get_median, draw_feature_line_plot, get_normalized_median
#from src.helper.years import draw_feature_line_plot
from src.models.song import Song
from src.models.song_feature import SongFeature
from src.shared import shared
from src.shared.shared import non_musical_features

artists_dict = None
normalized_artist_dict = None


# def analyze_genres_over_time():
#     grouped_df = shared.normalized_mcgill_df.groupby('genre_groups')
#
#     dict = {}
#     labels = []
#     deviation_values = []
#     for genre, group_df in grouped_df:
#         labels.append(genre)
#         dev_value = get_deviation_value_songs(group_df)
#         deviation_values.append(dev_value)
#         dict[genre] = dev_value
#
#     return deviation_values

#
# def get_deviation_value_songs(df):
#     deviation = 0
#     n = len(list(shared.song_features_dict.values()))
#
#     for feature in shared.song_features_dict.values():
#         if feature.feature_id not in shared.non_y_axis_features and feature.is_numerical and not feature.is_boolean and not feature.is_sentiment_feature:
#             norm_median = get_normalized_median(feature)
#             for i, song in df.iterrows():
#                 year = song['year']
#                 dev = (norm_median.loc[song['year']] - song[feature.feature_id])**2
#                 if math.isnan(dev):
#                     x = 42
#                 deviation += dev
#
#     return deviation/(n*len(df))


def analyze_feature_median_deviation():
    dev_value_all_songs = get_deviation_value_all_songs()
    analyze_artists_over_time(dev_value_all_songs)
    analyze_genre_deviations_from_median(dev_value_all_songs)

# TODO check if all features are normalized
def analyze_artists_over_time(dev_value_all_songs):
    global artists_dict
    global normalized_artist_dict

    df = pd.read_csv(feature_file_path)
    artists_dict = defaultdict(list)
    normalized_artist_dict = defaultdict(list)

    for index, row in df.iterrows():
        artists = row['artist'].split(";")
        for artist in artists:
            artists_dict[artist].append(row)
            normalized_artist_dict[artist].append(shared.normalized_mcgill_df.iloc[index])

    sorted_dict = {k: v for k, v in sorted(artists_dict.items(), key=lambda song_list: len(song_list[1]), reverse=True)}

    upper_line = ''
    lower_line = ''
    most_common_artists = []
    most_common_artists_str = ''
    for i in range(9):
        upper_line += f'{list(sorted_dict.keys())[i]} & '
        lower_line += f'n={len(list(sorted_dict.values())[i])} & '
        artist = list(sorted_dict.keys())[i]
        most_common_artists.append(artist)
        most_common_artists_str += f'{artist} (n={len(list(sorted_dict.values())[i])}), '

    print(most_common_artists_str)

    for artist in most_common_artists:
        print(f'{artist} & {get_deviation_value(artist):.3f} \\\\ \n \\hline')

    print('deviation of all songs')
    dev_value_all_songs = get_deviation_value_all_songs()
    print(dev_value_all_songs)
    create_barplot([get_deviation_value(artist) for artist in most_common_artists], most_common_artists, '$a_K$', 'a_k.jpg', '$a_K$ nach Künstler', ylim=1.4, horizontal_line=dev_value_all_songs, figsize=(4.48, 4.5))

    # for feature in list(shared.song_features_dict.values()):
    #     if feature.feature_id not in non_y_axis_features:
    #         draw_feature_line_plot_with_artist_coordinates(most_common_artists, feature)


def analyze_genre_deviations_from_median(dev_value_all_songs):
    df = shared.normalized_mcgill_df
    df = df[~df['genre_groups'].isnull()]

    df_groups = df.groupby('genre_groups')

    deviation_values = []
    genre_keys = []
    for key, df in df_groups:
        genre_keys.append(key)
        genre_songs = [song for _, song in df.iterrows()]
        deviation_values.append(get_deviation_value_songs(genre_songs))

    labels = [get_genre_group_string(g) for g in genre_keys]
    create_barplot(deviation_values, labels, '$a_k$', 'a_k_genres.jpg', '$a_k$ nach Musikrichtung', ylim=1.8, horizontal_line=dev_value_all_songs, figsize=(3.5, 3.9))


# def draw_artist_line_plots(artists):
#     for feature in shared.song_features_dict.values():
#         draw_feature_line_plot_with_artist_coordinates(artists, feature)


def get_deviation_value_all_songs():
    deviation = 0
    n = len(list(shared.song_features_dict.values()))

    for feature in shared.song_features_dict.values():
        if feature.feature_id not in shared.non_musical_features and feature.is_numerical and not feature.is_boolean and not feature.is_sentiment_feature:
            norm_median = get_normalized_median(feature)
            for i, song in shared.normalized_mcgill_df.iterrows():
                year = song['year']
                value = norm_median.loc[year]
                dev = (norm_median.loc[song['year']] - song[feature.feature_id])**2
                if math.isnan(dev):
                    x = 42
                deviation += dev

    return deviation/(n*len(shared.normalized_mcgill_df))

def get_deviation_value(artist):
    global normalized_artist_dict
    songs = normalized_artist_dict[artist]
    return get_deviation_value_songs(songs)


def get_deviation_value_songs(songs):
    deviation = 0
    n = len(list(shared.song_features_dict.values()))

    for feature in shared.song_features_dict.values():
        if feature.feature_id not in shared.non_musical_features and feature.is_numerical and not feature.is_sentiment_feature:
            norm_median = get_normalized_median(feature)
            for song in songs:
                year = song['year']
                value = norm_median.loc[year]
                feature_val = song[feature.feature_id]
                dev = (norm_median.loc[song['year']] - song[feature.feature_id])**2
                if math.isnan(dev):
                    x = 42
                deviation += dev
                if math.isnan(deviation):
                    x = 42

    return deviation/(n*len(songs))



def draw_feature_line_plot_with_artist_coordinates(artists, feature: SongFeature):
    global artists_dict

    median = get_median(feature)

    test = median.loc[1958]
    # years = median.keys().tolist()
    # feature_values = median.values
    coordinates = [[] for _ in range(len(artists))]

    for i, artist in enumerate(artists):
        songs = artists_dict[artist]
        for song in songs:
            coordinates[i].append((song['year'], song[feature.feature_id]))
    draw_feature_line_plot(feature, coordinates, artists, artist[0:3].lower())
    x = 42



def init_artists_dict(songs: List[Song]):
    global artists_dict

    if artists_dict == None:
        artists_dict = group_by_artist(songs)

    return artists_dict


def group_by_artist(songs: List[Song]):
    dict = defaultdict(list)
    for song in songs:
        artists = song.artist.split(", ")
        for artist in artists:
            dict[artist].append(song)

    sorted_dict = {k: v for k, v in sorted(dict.items(), key=lambda song_list: len(song_list[1]), reverse=True)}
    return sorted_dict


def get_artist_feature_coordinates(artist, feature_fn, feature_fn_parameters=None):
    global artists_dict

    artist_songs = artists_dict[artist]

    coordinates = []
    for song in artist_songs:
        parameters = [song]
        if feature_fn_parameters is not None:
            parameters += feature_fn_parameters
        feature_expression = feature_fn(*parameters)

        coordinates.append((int(song.chart_year), feature_expression))

    return coordinates


# def draw_feature_line_plot_with_artist_coordinates_old(artist, songs: List[Song], feature_fn, ylabel, title='', fn_parameters=[]):
#     artist_feature_coordinates = get_artist_feature_coordinates(artist, feature_fn, fn_parameters)
#     filename = f"{ylabel.lower().replace(' ', '_')}_{artist.lower().replace(' ', '_')}.png"
#
#     # draw_feature_line_plot(songs, feature_fn, ylabel,
#     #                        filename, f'{ylabel} im Verlauf der Zeit', dir='artists',
#     #                        artist_coordinates=artist_feature_coordinates, coordinate_legend=f'Lieder von {artist}', fn_parameters=fn_parameters)
#
