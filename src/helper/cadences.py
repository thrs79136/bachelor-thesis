import logging
import statistics
import traceback
from typing import List

import scs

from src.helper.statistics_helper import get_peak_chart_position_list, get_rank_correlation_coefficient_from_value_lists
from src.models.mgill_chord import RomNumNotations, RomNumNotation, MajOrMin
from src.models.song import Song

logger = logging.getLogger(__name__)

class Cadence:
    # roman numeral notation
    def __init__(self, name: str, chords: List[str]):
        self.name = name
        self.chords = []
        #self.chords = chords
        for chord_notation in chords:
            self.chords.append(RomNumNotation.from_number_and_type(chord_notation[0], chord_notation[1]))


# in this case an 'n' after the roman numeral means the chord type will not be taken into account
cadences = [

    Cadence('authentic cadence', [('V', MajOrMin.Major), ('I', MajOrMin.Neither)]),
    Cadence('plagal cadence', [('IV', MajOrMin.Neither), ('I', MajOrMin.Neither)]),
    Cadence('half cadence', [('V', MajOrMin.Neither)]),
    Cadence('deceptive cadence', [('V', MajOrMin.Major), ('VI', MajOrMin.Neither)])
]

def get_cadence_count_dict( song: Song):

    count_dict = {}

    # init dictionary
    for cadence in cadences:
        count_dict[cadence.name] = 0

    # get counts for every section
    for section in song.mcgill_billboard_song_data.sections:
        if len(section.chord_progression) < 3:
            continue

        prog = section.chord_progression

        for cadence in cadences:
            is_cadence = True
            for i, cadence_chord in enumerate(cadence.chords):
                prog_index = -len(cadence.chords) + i
                if not cmp_chord(cadence_chord, prog[prog_index]):
                    is_cadence = False
                    break

            if is_cadence:
                count_dict[cadence.name] += 1

    return count_dict


def create_cadence_count_dict_all_songs(songs: List[Song]):
    count_dict = {}
    count_dict_without_type = {}

    for song in songs:
        sections = song.mcgill_billboard_song_data.sections
        for section in sections:
            if len(section.chord_progression) < 2:
                continue

            chord1 = repr(section.chord_progression[-2])
            chord2 = repr(section.chord_progression[-1])

            chord1_without_type = section.chord_progression[-2].rom_num_notation.name
            chord2_without_type = section.chord_progression[-1].rom_num_notation.name

            cadence_str = f'{chord1},{chord2}'
            cadence_str_without_type = f'{chord1_without_type},{chord2_without_type}'

            res = count_dict.get(cadence_str, -1)
            if res == -1:
                count_dict[cadence_str] = {'sections_count': 0, 'songs_count': 0, 'songs': []}
            if res == -1 or count_dict[cadence_str]['songs'][-1] != song.mcgill_billboard_id:
                count_dict[cadence_str]['songs'].append(song.mcgill_billboard_id)
                count_dict[cadence_str]['songs_count'] += 1
            count_dict[cadence_str]['sections_count'] += 1


            res = count_dict_without_type.get(cadence_str_without_type, -1)
            if res == -1:
                count_dict_without_type[cadence_str_without_type] = {'sections_count': 0, 'songs_count': 0, 'songs': []}
            if res == -1 or count_dict_without_type[cadence_str_without_type]['songs'][-1] != song.mcgill_billboard_id:
                count_dict_without_type[cadence_str_without_type]['songs'].append(song.mcgill_billboard_id)
                count_dict_without_type[cadence_str_without_type]['songs_count'] += 1
            count_dict_without_type[cadence_str_without_type]['sections_count'] += 1


    sorted_items = {k: v for k, v in sorted(count_dict.items(), key=lambda item: item[1]['songs_count'], reverse=True)}
    sorted_items2 = {k: v for k, v in sorted(count_dict_without_type.items(), key=lambda item: item[1]['songs_count'], reverse=True)}


# # V-I or V-i
    # self.authentic_cadences = 0
    # # IV-I (major or minor)
    # self.plagal_cadences = 0
    # # phrase ends on V
    # self.half_cadences = 0
    # # TODO check minor and major
    # # V-iv
    # self.deceptive_cadences = 0


def cmp_chord(cadence_chord: RomNumNotation, song_chord: RomNumNotation):
    if not isinstance(song_chord, RomNumNotation):
        print('is not instance')
    if cadence_chord.maj_or_min == MajOrMin.Neither:
        # only compare number
        return cadence_chord.roman_number == song_chord.roman_number
    else:
        # compare number and chord type
        return cadence_chord == song_chord


def cmp_chord_old(cadence_chord: RomNumNotation, song_chord: RomNumNotation):
    if cadence_chord.rom_num_notation.value >= RomNumNotations.In.value:
        # only compare number
        return cadence_chord.roman_number == song_chord.roman_number
    else:
        # compare number and chord type
        return cadence_chord == song_chord



def cmp_rom_num(notation: RomNumNotation, rom_num: str, chord_type: MajOrMin = None):
    roman_numbers_match = notation.roman_number == RomNumNotations[rom_num]
    if chord_type is None:
        return roman_numbers_match
    return roman_numbers_match and notation.maj_or_min == chord_type


def identify_cadences(song: Song):
    cadences = get_cadence_count_dict(song)
    percentage_dict = {}
    for key, value in cadences.items():
        sections_count = len(song.mcgill_billboard_song_data.sections)
        percentage_dict[key] = value/sections_count

    song.cadences = percentage_dict


def analyze_cadences(songs: List[Song]):
    # find most popular cadences (only last 2 chords) and find out if more popular cadences correlate
    create_cadence_count_dict_all_songs(songs)

    for song in songs:
        identify_cadences(song)

    peak_chart_pos_list = get_peak_chart_position_list(songs)

    for cadence in cadences:

        cadence_percentages = [song.cadences[cadence.name] for song in songs]
        # negative value -> increased popularity
        rho = get_rank_correlation_coefficient_from_value_lists(peak_chart_pos_list, cadence_percentages)

        chart_pos_list_cadence_used = []
        chart_pos_list_cadence_not_used = []
        for song in songs:
            if song.cadences[cadence.name] > 0:
                chart_pos_list_cadence_used.append(song.peak_chart_position)
            else:
                chart_pos_list_cadence_not_used.append(song.peak_chart_position)

        median1 = statistics.median(chart_pos_list_cadence_not_used)
        median2 = statistics.median(chart_pos_list_cadence_used)

        print('Median chart position of songs that do not use this progression')
        print(median1)
        print('Median chart position of songs that do use this progression')
        print(median2)






