import csv
import inspect
from typing import List

from src.models.song import Song


# TODO make this a class

def write_header(path: str):
    file = open(path, "w")
    file.write('mcgill_billboard_id,artist,song_name,chart_year,peak_chart_position,genres,spotify_song_data\n')


def save_songs(path: str, songs: List[Song]):
    write_header(path)
    with open(path, "a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)

        for song in songs:
            csvwriter.writerow(song.get_csv_row())


def save_song(path: str, song: Song):
    with open(path, "a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        csvwriter.writerow(song.get_csv_row())


def get_songs(file_path: str) -> List[Song]:
    songs = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            songs.append(Song.from_csv_row(row))

    return songs


def get_csv_reader(filepath: str) -> csv.DictReader:
    with open(filepath, newline='') as csvfile:
        return csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)


def get_next_song_from_mcgill_index(csvreader: csv.DictReader) -> [Song]:
    row = next(csvreader)
    return Song.from_mcgill_csv_row(row)


def row_count(filename):
    with open(filename) as in_file:
        return sum(1 for _ in in_file)


def modify_billboard_index(oldpath: str, newpath: str):
    reading_file = open(oldpath, "r")

    new_file_content = ""
    is_string = False
    for line in reading_file:
        stripped_line = line.strip()
        new_line = ''

        for index in range(0, len(stripped_line)):
            character = stripped_line[index]
            if character == '"':
                is_string = not is_string
            elif character == ';' and is_string:
                new_line += ','
            else:
                new_line += character
        new_file_content += new_line + '\n'

    reading_file.close()
    writing_file = open(newpath, "w")
    writing_file.write(new_file_content)
    writing_file.close()
