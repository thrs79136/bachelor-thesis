from collections import OrderedDict, defaultdict
from typing import List

from src.helper.years import draw_feature_line_plot
from src.models.song import Song

artists_dict = None

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


def draw_feature_line_plot_with_artist_coordinates(artist, songs: List[Song], feature_fn, ylabel, title='', fn_parameters=[]):
    artist_feature_coordinates = get_artist_feature_coordinates(artist, feature_fn, fn_parameters)
    filename = f"{ylabel.lower().replace(' ', '_')}_{artist.lower().replace(' ', '_')}.png"

    draw_feature_line_plot(songs, feature_fn, ylabel,
                           filename, f'{ylabel} im Verlauf der Zeit', dir='artists',
                           artist_coordinates=artist_feature_coordinates, coordinate_legend=f'Lieder von {artist}', fn_parameters=fn_parameters )

