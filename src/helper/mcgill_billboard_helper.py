from typing import List
import os

from src.models.song import Song


def get_mcgill_song_ids() -> List[str]:
    directories = [dir[0] for dir in os.walk('./data/songs/mcgill-billboard')]
    return [dir.split('\\')[1] for dir in directories[1::]]


def get_song_by_mcgill_id(id: str) -> Song:
    chords_file = open(f'./data/songs/mcgill-billboard/{id}/salami_chords.txt', 'r')
    song_title = chords_file.readline()[9:-1]
    artist = chords_file.readline()[10:-1]
    return Song(id, artist, song_title)