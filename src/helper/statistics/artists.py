from collections import OrderedDict, defaultdict
from typing import List

from src.models.song import Song


def group_by_artist(songs: List[Song]):
    dict = defaultdict(list)
    for song in songs:
        artists = song.artist.split(", ")
        for artist in artists:
            dict[artist].append(song)

    sorted_dict = {k: v for k, v in sorted(dict.items(), key=lambda song_list: len(song_list[1]), reverse=True)}
    return sorted_dict


