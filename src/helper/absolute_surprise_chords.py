import math
from collections import defaultdict
from typing import List

from src.helper.statistics_helper import analyze_song_feature_correlation
from src.helper.years import draw_feature_line_plot
from src.models.song import Song

chord_count_dict = defaultdict(int)
total_chords: int
chord_count_dict_by_song = {}
total_chords_by_song = {}

inited_dict = False

def analyze_absolute_surprises_chords(songs: List[Song]):
    init_chords_dict(songs)

    analyze_song_feature_correlation(songs, get_song_chord_surprise, 'Average song chord surprise', directory='surprise')
    draw_feature_line_plot(songs, Song.get_added_seventh_use, 'Überraschungswert für Akkorde')


def init_chords_dict(songs: List[Song]):
    global chord_count_dict
    global total_chords
    global chord_count_dict_by_song
    global total_chords_by_song
    global inited_dict

    if inited_dict:
        return

    inited_dict = True
    find_chords(songs)

    # count progressions
    total_chords = sum(chord_count_dict.values())
    for song_id, chord_dict in chord_count_dict_by_song.items():
        total_count = sum(chord_dict.values())
        total_chords_by_song[song_id] = total_count


def find_chords(songs: List[Song]):
    global chord_count_dict
    global chord_count_dict_by_song

    for song in songs:
        chord_count_dict_by_song[song.mcgill_billboard_id] = {}
        section_ids = set()

        chord_count_dict_by_song[song.mcgill_billboard_id] = {}
        for section in song.mcgill_billboard_song_data.sections:
            if section.id in section_ids:
                continue
            section_ids.add(section.id)
            for chord in section.chord_progression:
                chord_dict_name = f'{chord.roman_number}:{chord.chord_name}'
                chord_count_dict[chord_dict_name] += 1
                song_dict = chord_count_dict_by_song[song.mcgill_billboard_id]
                if song_dict.get(chord_dict_name, -1) == -1:
                    song_dict[chord_dict_name] = 1
                else:
                    song_dict[chord_dict_name] += 1


def get_song_chord_surprise(song: Song):
    surprise = get_song_average_chord_surprise(song.mcgill_billboard_id)
    #return surprise
    return min(200, surprise)




def get_song_average_chord_surprise(song_id):
    global chord_count_dict
    global chord_count_dict_by_song

    surprise_sum = 0
    song_dict = chord_count_dict_by_song[song_id]
    for chord, count in song_dict.items():
        surprise = surprise_of_finding_chord(chord)
        chord_song_prob = get_song_chord_prob(song_id, chord)
        surprise_sum += chord_song_prob * surprise * count

    return surprise_sum


def get_song_chord_prob(song_id, chord):
    global chord_count_dict_by_song
    global total_chords_by_song

    prog_count_in_song = chord_count_dict_by_song[song_id].get(chord, -1)
    return prog_count_in_song / total_chords_by_song[song_id]


def surprise_of_finding_chord(chord):
    return -math.log2(chord_prob(chord))


def chord_prob(chord):
    global chord_count_dict
    global total_chords

    return chord_count_dict[chord] / total_chords
