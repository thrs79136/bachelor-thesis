import csv
import inspect
from typing import List

from src.models.song import Song


# TODO make this a class

def write_header(path: str):
    file = open(path, "w")
    file.write('mcgill_billboard_id, artist, song_name, genres, spotify_song_data\n')


# def save_songs(path: str, songs: List[Song]):
#     with open(path, 'a', newline='') as csvfile:
#         csvwriter = csv.writer(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
#
#         for song in songs:
#             csvwriter.writerow(song.get_csv_row())


def save_song(path: str, song: Song):
    with open(path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        csvwriter.writerow(song.get_csv_row())


def get_songs(file_path: str) -> List[Song]:
    songs = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            songs.append(Song.from_csv_row(row));
            artist = row['artist']
            # song = Song.csv(row)

    return songs