import logging
import string
import re
from enum import Enum
from operator import mod
from typing import List

from parker.chords import Chord, SHORTHAND_TO_TRANSPOSE, SHORTHAND_TO_SCALE
from parker.scales import *

logger = logging.getLogger(__name__)


note_to_interval = {
    'B#':   0,
    'C':    0,
    'C#':   1,
    'Db':   1,
    'C##':  1,
    'D':    2,
    'D#':   3,
    'Eb':   3,
    'E':    4,
    'Fb':   4,
    'E#':   5,
    'F':    5,
    'Gbb':  5,
    'F#':   6,
    'Gb':   6,
    'F##':  7,
    'G':    7,
    'Abb':  7,
    'G#':   8,
    'Ab':   8,
    'G##':  9,
    'A':    9,
    'A#':   10,
    'Bb':   10,
    'Cbb':  10,
    'A##':  11,
    'B':    11,
    'Cb':   11,
}


# values denote the number of half steps
degree_to_interval = {
    '1': 0,
    '#1': 1,
    'b2': 1,
    '2': 2,
    'b3': 3,
    '3': 4,
    '4': 5,
    '#4': 6,
    'b5': 6,
    '5': 7,
    '#5': 8,
    'b6': 8,
    '6': 9,
    'b7': 10,
    '7': 11,
    'b9': 13,
    '9': 14,
    '#9': 15,
    '11': 17,
    '#11': 18,
    'b13': 20,
    '13': 21
}




class MajOrMin(Enum):
    Major = 0
    Minor = 1
    Neither = 2


class RomNumNotations(Enum):
    __order__ = 'I bII II bIII III IV bV V bVI VI bVII VII'
    I = 0
    bII = 1
    II = 2
    bIII = 3
    III = 4
    IV = 5
    bV = 6
    V = 7
    bVI = 8
    VI = 9
    bVII = 10
    VII = 11

    # Im = 12
    # bIIm = 13
    # IIm = 14
    # bIIIm = 15
    # IIIm = 16
    # IVm = 17
    # bVm = 18
    # Vm = 19
    # bVIm = 20
    # VIm = 21
    # bVIIm = 22
    # VIIm = 23
    #
    # In = 24
    # bIIn = 25
    # IIn = 26
    # bIIIn = 27
    # IIIn = 28
    # IVn = 29
    # bVn = 30
    # Vn = 31
    # bVIn = 32
    # VIn = 33
    # bVIIn = 34
    # VIIn = 35




class RomNumNotation:

    def __init__(self, rom_num_notation: RomNumNotations, rom_num: str, maj_or_min: MajOrMin, chord_name: str = None):
        self.rom_num_notation = rom_num_notation
        self.roman_number = rom_num
        self.maj_or_min = maj_or_min
        self.chord_name = chord_name

    @classmethod
    def from_number_and_type(cls, rom_num: str, chord_type: MajOrMin):
        # roman number without information about chordtype
        # if chord_type == MajOrMin.Minor:
        #     rom_num += 'm'
        # elif chord_type == MajOrMin.Neither:
        #     rom_num += 'n'

        rom_num_notation = RomNumNotations[rom_num]

        return cls(rom_num_notation, rom_num, chord_type)

    # @classmethod
    # def from_notation_id(cls, id: int):
    #     roman_number_notation = RomNumNotations(id)
    #     roman_number = RomNumNotations(roman_number_notation.value % 12).name
    #     type = MajOrMin(int(id / 12))
    #     return cls(roman_number_notation, roman_number, type)

    @classmethod
    def from_string(cls, notation: str):
        rom_num_notation = RomNumNotations[notation]
        roman_num = RomNumNotations(rom_num_notation.value % 12).name
        type = MajOrMin(int(rom_num_notation.value / 12))
        return cls(rom_num_notation, roman_num, type)

    def __eq__(self, other):
        if isinstance(other, RomNumNotations):
            return self.rom_num_notation.value == other.value
        elif isinstance(other, RomNumNotation):
            return self.roman_number == other.roman_number and self.maj_or_min == other.maj_or_min
        else:
            return False

    def __repr__(self):
        try:
            chord_type = ''
            if self.maj_or_min == MajOrMin.Minor:
                chord_type += 'm'
            elif self.maj_or_min == MajOrMin.Neither:
                chord_type += 'n'
            return self.rom_num_notation.name + chord_type
        except:
            pass

    # def __init__(self, number: int, type: ChordType):
    #     self.number = RomNumNotations(number),
    #     self.type = type
    #
    # def __init__(self, repr: string):
    #
    #     if repr[-1] == 'm':
    #         self.type = ChordType.Minor
    #         self.number = RomNumNotations[repr[:-1]]
    #     else:
    #         self.type = ChordType.Major
    #         self.number = RomNumNotations[repr]




class McGillChord(Chord):
    unrecognizednotedcounter = 0

    def __init__(self, chord=None, octave=None):

        self.roman_numeral_notation = None
        self.mcgill_chord_name = chord

        split_colon = chord.split(':')
        root_note = split_colon[0]
        chord_without_root = split_colon[1]

        shorthand = re.match(r"[a-zA-Z0-9]+", chord_without_root).group(0)
        parker_chord = mcgill_to_parker_chord.get(shorthand, '')

        if parker_chord == '':
            logger.error(f'[McGillChord.__init__] Could not get Parker chord name for {chord}. Shorthand: {shorthand} (No. {McGillChord.unrecognizednotedcounter})')
            McGillChord.unrecognizednotedcounter += 1
            return

        if callable(parker_chord):
            parker_chord(self, root_note)
        else:
            super().__init__(root_note + parker_chord, octave)
            # because modifying the intervals property leads to undesired behaviour
            self.mcgill_intervals = self.intervals.copy()

        # added notes
        paranthese_split = chord.split('(')
        if len(paranthese_split) != 1:
            added_note = paranthese_split[1].split(')')[0]
            self.ensure_note_exists(added_note)

        # inversion
        inversion_split_str = chord.split('/')
        if len(inversion_split_str) > 1:
            self.invert(inversion_split_str[1])

        if -1 in self.mcgill_intervals:
            logger.error("-1 in intervals: " + self.mcgill_chord_name);

    # def hdim7(self, root_note):
    #     super().__init__(f'{root_note}dimM7')
    #     self.intervals[3] = 10
    #     self.notes[3] = self.notes[3].diminish()

    def add_roman_numeral_notation(self, tonic: string):
        interval1 = note_to_interval[tonic]
        test_name = self.root.base_name + self.root.accidentals.name
        interval2 = note_to_interval[self.root.base_name + self.root.accidentals.name]
        # roman_number_id = abs(note_to_interval[tonic] - note_to_interval[self.root.base_name + self.root.accidentals.name])

        dist = abs(interval1 - interval2)
        if interval1 <= interval2:
            roman_number_id = dist
        else:
            roman_number_id = 12 - dist

        # roman_number_id = min(12 - dist, dist)

        # print(self.intervals)
        # classify as minor or major
        chord_type = MajOrMin.Neither
        if 3 in self.mcgill_intervals:
            chord_type = MajOrMin.Minor
            # roman_number_id += 12
        elif 4 in self.mcgill_intervals:
            chord_type = MajOrMin.Major

        self.chord_type = chord_type

        rom_num_not = RomNumNotations(roman_number_id)
        split_chord = self.mcgill_chord_name.split(':')
        if len(split_chord) == 0 or len(split_chord) > 2:
            x = 42
        self.roman_numeral_notation = RomNumNotation(rom_num_not, rom_num_not.name, chord_type, split_chord[1])

    # def add_roman_numeral_notation_old(self, tonic: string):
    #     roman_number = RomNumNotations(abs(note_to_interval[tonic] - note_to_interval[self.root.base_name]))
    #     # print(self.intervals)
    #     chord_type = ChordType.Neither
    #     for interval in self.mcgill_intervals:
    #         if interval == 4:
    #             chord_type = ChordType.Major
    #             break
    #         elif interval == 3:
    #             chord_type = ChordType.Minor
    #             break
    #
    #     # chord_type =
    #     self.roman_numeral_notation = RomNumNotation(roman_number, chord_type)

    def single_note(self, root_note):
        super().__init__(f'{root_note}5')
        self.mcgill_intervals = self.intervals.copy()
        # logger.debug(f'Creating powerchord with root note {root_note}')
        self.mcgill_intervals = self.mcgill_intervals[:-1]
        self.notes = self.notes[:-1]

    def maj11(self, root_note):
        super().__init__(f'{root_note}11')
        self.mcgill_intervals = self.intervals.copy()

        self.mcgill_intervals[2] = 11
        self.notes[2] = self.notes[2].augment()

    # octaves are not correct but they won't be taken into account
    def invert(self, inversion: string):

        index = self.ensure_note_exists(inversion)

        self.notes = self.notes[index:] + self.notes[:index]
        self.mcgill_intervals = self.mcgill_intervals[index:] + self.mcgill_intervals[:index]


    # TODO check for dim7
    def interval_to_int(self, interval):
        if isinstance(interval, Aug):
            return interval.amount + 1
        if isinstance(interval, Dim):
            return interval.amount - 1
        return interval


    # ensures note is part of chord and returns index of self.notes where the note was added
    def ensure_note_exists(self, scale_no: str) -> int:
        # scale = self.get_scale()
        # added_note = scale[scale_no-1]
        interval = degree_to_interval.get(scale_no, -1)

        for i in range(len(self.mcgill_intervals)):
            if interval == self.mcgill_intervals[i]:
                return i

            lower_interval = self.interval_to_int(self.mcgill_intervals[i])
            if i + 1 != len(self.mcgill_intervals):
                upper_interval = self.interval_to_int(self.mcgill_intervals[i + 1])

            #if i + 1 == len(self.intervals) or self.intervals[i] < interval < self.intervals[i + 1]:
            if i + 1 == len(self.mcgill_intervals) or lower_interval < interval < upper_interval:
                index = i + 1
                root_note = self.notes[0]
                added_note = root_note.clone().set_transpose(interval)
                self.notes.insert(index, added_note)
                self.mcgill_intervals.insert(index, interval)
                return index

    # ensures note is part of chord and returns index of self.notes where the note was added
    def ensure_note_exists_old(self, interval) -> int:
        for i in range(len(self.mcgill_intervals)):
            if interval == self.mcgill_intervals[i]:
                return i
            if i + 1 == len(self.mcgill_intervals) or self.mcgill_intervals[i] < interval < self.mcgill_intervals[i + 1]:
                index = i + 1
                root_note = self.notes[0]
                added_note = root_note.clone().set_transpose(interval)
                self.notes.insert(index, added_note)
                self.mcgill_intervals.insert(index, interval)
                return index


mcgill_to_parker_chord = {
    '1': McGillChord.single_note,
    'maj': 'M',
    'min': 'm',
    '5': '5',
    'maj6': 'M6',
    'min6': 'm6',
    'hdim7': 'm7b5',
    '7': '7',
    'min7': 'm7',
    'maj7': 'M7',
    'minmaj7': 'mM7',
    'dim7': 'dim7',
    '9': '9',
    'maj9': 'M9',
    'min9': 'm9',
    '11': '11',
    'min11': 'm11',
    'maj11': McGillChord.maj11,
    '13': '13',
    'maj13': 'M13',
    'min13': 'm13',
    'sus2': 'sus2',
    'sus4': 'sus4',
    'dim': 'dim',
    'aug': 'aug'
}

    #
# class Chord:
#     # intervals are described as the number of semitones
#     def __init__(self, root_note: string, integer_notation: List[int]):
#         self.notes = list(map(lambda i: Note((Note(root_note) + i) % 12), integer_notation))
#         x = 1
#
#
# class MajorChord(Chord):
#     def __init__(self, root_note: string):
#         super().__init__(root_note, [0, 4, 7])
#
#
# class Note(Enum):
#     C = 0
#     Db = 1
#     D = 2
#     Eb = 3
#     E = 4
#     F = 5
#     Gb = 6
#     G = 7
#     Ab = 8
#     A = 9
#     Bb = 10
#     B = 11
