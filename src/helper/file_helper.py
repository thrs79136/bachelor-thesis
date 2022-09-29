import csv
import os
import pickle
from typing import List

import numpy as np

from src.helper.cadences import identify_cadences
from src.helper.statistics_helper import group_by_year
from src.models.mcgill_songdata import Bar
from src.models.mgill_chord import McGillChord
from src.models.song import Song
from src.shared import song_features

global feature_file_path
feature_file_path = '../data/csv/song_features.csv'

global year_feature_file_path
year_feature_file_path = '../data/csv/year_features.csv'

global spotify_playlist_path
spotify_playlist_path = '../data/csv/years'

song_csv_header = ['mcgill_billboard_id', 'artist', 'song_name', 'chart_year', 'peak_chart_position', 'genres',
                   'spotify_song_data',
                   'spotify_id']

def write_text_file(path: str, content: str):
    try:
        file = open(path, "w", encoding = 'utf-8')
        file.write(content)
    except Exception:
        x = 42


def write_header(path: str):
    file = open(path, "w")
    file.write('mcgill_billboard_id,artist,song_name,chart_year,peak_chart_position,genres,spotify_song_data,'
               'spotify_id\n')


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

def print_sections(song: Song):
    for section in song.mcgill_billboard_song_data.sections:
        print(section.name)

        bars_roman_num = []

        for bar in section.content:
            if isinstance(bar, Bar):
                for chord in bar.content:
                    if isinstance(chord, McGillChord):
                        roman_num = repr(chord.roman_numeral_notation)
                        try:
                            if len(bars_roman_num) != 0:
                                if bars_roman_num[-1] != roman_num:
                                    bars_roman_num.append(roman_num)
                            else:
                                bars_roman_num.append(roman_num)
                        except:
                            pass


        print(' '.join(bars_roman_num))

def get_songs(file_path: str) -> List[Song]:
    songs = []
    with open(file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            song = Song.from_csv_row(row)
            # print_sections(song)
            # identify_cadences(song)
            # print(repr(song))
            songs.append(song)

    return songs


def get_songs_from_binary_file(file_path: str) -> List[Song]:
    with open(file_path, 'rb') as file2:
        return pickle.load(file2)


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


def save_dataframe(df, filename):
    df.to_csv(f'{spotify_playlist_path}/{filename}')


def save_feature_csv(songs: List[Song], feature_names, file=feature_file_path):
    with open(file, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        csvwriter.writerow(feature_names)

        features = [song_features.song_features_dict[feature_name] for feature_name in feature_names]
        for song in songs:
            csv_row = []

            for feature in features:
                if song.artist == 'Jackson Browne' and feature.feature_id == 'circle_of_fifths_dist':
                    x = 42
                parameters = [song] + feature.parameters
                csv_row.append(feature.feature_fn(*parameters))

            csvwriter.writerow(csv_row)


def save_median_feature_csv(songs: List[Song], feature_names):

    with open(year_feature_file_path, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)

        features = [song_features.song_features_dict[feature_name] for feature_name in feature_names if song_features.song_features_dict[feature_name].is_numerical]
        feature_names = [feature.feature_id for feature in features]

        csvwriter.writerow(feature_names)

        grouped_songs = group_by_year(songs)

        for year, year_songs in grouped_songs.items():
            year_medians = []
            for feature in features:
                if not feature.is_numerical:
                    continue

                feature_expr = []
                for song in year_songs:
                    parameters = [song] + feature.parameters
                    feature_expr.append(feature.feature_fn(*parameters))
                median = np.median(feature_expr)
                year_medians.append(median)

            csvwriter.writerow(year_medians)


def get_songs_from_feature_csv():
    songs = []
    with open(feature_file_path, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', escapechar='\\', quoting=csv.QUOTE_NONE)
        for row in csvreader:
            song = Song.from_feature_csv_row(row)
            songs.append(song)

    return songs
