import math
import numpy as np
from typing import List

from src.helper.chord_progressions import find_song_progressions, find_progressions
from src.helper.statistics_helper import analyze_song_groups, analyze_song_feature_correlation
from src.models.song import Song

prog_count_dict = {}
total_progressions: int
prog_count_dict_by_song = {}
total_progressions_by_song = {}

song_to_group = {}


# splitting

index_to_group_name = {
    0: '1st quarter',
    1: '2nd quarter',
    2: '3rd quarter',
    3: '4th quarter'
}


def analyze_absolute_surprises(songs: List[Song]):
    init(songs)
    analyze_song_groups(songs, get_quarter_group, 'Absolute surprise of chord progressions',
                       'absolute_surprise.png', group_order=[index_to_group_name.values()], box_plot_values_fn=get_song_surprise)

    # analyze_song_groups(songs, Song.get_genres, 'Absolute surprise of chord progressions',
    #                     'absolute_surprise_genres.png', groups_count=5,
    #                     box_plot_values_fn=get_song_surprise)

    analyze_song_feature_correlation(songs, get_song_surprise, 'Average song surprise', directory='surprise')


def init_group_dict(songs: List[Song]):
    global song_to_group

    split_songs = split_by_quartiles(songs)
    for i, v in enumerate(split_songs):
        for song in v:
            song_to_group[song.mcgill_billboard_id] = i


def get_quarter_group(song: Song):
    return index_to_group_name[song_to_group[song.mcgill_billboard_id]]



def split_by_quartiles(songs: List[Song]):
    sorted_songs = sorted(songs)
    return np.array_split(sorted_songs, 4)


def prog_prob(prog):
    global prog_count_dict
    global total_progressions

    return prog_count_dict[prog] / total_progressions


def get_song_prog_prob(song_id, prog):
    global prog_count_dict_by_song
    global total_progressions_by_song

    prog_count_in_song = prog_count_dict_by_song[song_id].get(prog, -1)
    return prog_count_in_song / total_progressions_by_song[song_id]


def surprise_of_finding(prog):
    return -math.log2(prog_prob(prog))


def get_song_surprise(song: Song):
    return get_song_average_surprise(song.mcgill_billboard_id)

def get_song_average_surprise(song_id):
    global prog_count_dict_by_song
    global total_progressions_by_song


    surprise_sum = 0
    song_dict = prog_count_dict_by_song[song_id]
    for prog, count in song_dict.items():
        surprise = surprise_of_finding(prog)
        prog_song_prob = get_song_prog_prob(song_id, prog)
        surprise_sum += prog_song_prob * surprise

    return surprise_sum


def quartile_get_surprise_values(quartile_songs: List[Song]) -> list:
    return [get_song_average_surprise(song.mcgill_billboard_id) for song in quartile_songs]


def quartile_get_surprise_mean(quartile_songs: List[Song]):
    surprises_sum = 0
    for song in quartile_songs:
        surprises_sum += get_song_average_surprise(song.mcgill_billboard_id)
    return surprises_sum / len(quartile_songs)


def init(songs: List[Song]):
    global prog_count_dict
    global total_progressions
    global prog_count_dict_by_song
    global total_progressions_by_song

    init_group_dict(songs)

    find_progressions(songs, prog_count_dict, prog_count_dict_by_song)
    common = {k: v for k, v in sorted(prog_count_dict.items(), key=lambda item: item[1], reverse=True)}

    # count progressions
    total_progressions = sum(prog_count_dict.values())
    for song_id, prog_dict in prog_count_dict_by_song.items():
        total_count = sum(prog_dict.values())
        total_progressions_by_song[song_id] = total_count


# TODO use this
def get_quartile_surprises(songs: List[Song]):
    init(songs)

    split_songs = split_by_quartiles(songs)

    surprise_dict = {}
    for index, songs in enumerate(split_songs):
        surprise_dict[index] = quartile_get_surprise_values(songs)

    return surprise_dict


def get_quartile_surprises_mean(songs: List[Song]):
    global prog_count_dict
    global total_progressions
    global prog_count_dict_by_song
    global total_progressions_by_song

    init(songs)

    split_songs = split_by_quartiles(songs)

    surprise_dict = {}
    for index, songs in enumerate(split_songs):
        surprise_dict[index] = quartile_get_surprise_mean(songs)

    return surprise_dict


def find_linear_contributions(songs: List[Song]):
    global prog_count_dict
    global prog_count_dict_by_song

    init(songs)

    linear_contribution_dict = {}
    split_songs = split_by_quartiles(songs)
    for prog, count in prog_count_dict.items():
        linear_contribution_dict[prog] = get_linear_contribution_of_prog(split_songs[0], split_songs[3], prog)

    return linear_contribution_dict


def get_linear_contribution_of_prog(quartile1: List[Song], quartile4: List[Song], prog_str):
    sum1 = 0
    sum4 = 0
    for song in quartile1:
        sum1 += get_song_prog_prob(song.mcgill_billboard_id, prog_str)
    for song in quartile4:
        sum4 += get_song_prog_prob(song.mcgill_billboard_id, prog_str)

    return surprise_of_finding(prog_str) * (sum1 / len(quartile1) - sum4 / len(quartile4))
