import logging
import string
import re
from enum import Enum
from operator import mod
from typing import List

from parker.chords import Chord, SHORTHAND_TO_TRANSPOSE, SHORTHAND_TO_SCALE
from parker.scales import *

logger = logging.getLogger(__name__)

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
    }




class McGillChord(Chord):
    unrecognizednotedcounter = 0

    def __init__(self, chord=None, octave=None):

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

        # added notes
        paranthese_split = chord.split('(')
        if len(paranthese_split) != 1:
            added_note = paranthese_split[1].split(')')[0]
            self.ensure_note_exists(added_note)

        # inversion
        inversion_split_str = chord.split('/')
        if len(inversion_split_str) > 1:
            self.invert(inversion_split_str[1])

    # def hdim7(self, root_note):
    #     super().__init__(f'{root_note}dimM7')
    #     self.intervals[3] = 10
    #     self.notes[3] = self.notes[3].diminish()

    def single_note(self, root_note):
        super().__init__(f'{root_note}5')
        # logger.debug(f'Creating powerchord with root note {root_note}')
        self.intervals = self.intervals[:-1]
        self.notes = self.notes[:-1]

    def maj11(self, root_note):
        super().__init__(f'{root_note}11')

        self.intervals[2] = 11
        self.notes[2] = self.notes[2].augment()

    # octaves are not correct but they won't be taken into account
    def invert(self, inversion: string):

        index = self.ensure_note_exists(inversion)

        self.notes = self.notes[index:] + self.notes[:index]
        self.intervals = self.intervals[index:] + self.intervals[:index]



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

        for i in range(len(self.intervals)):
            if interval == self.intervals[i]:
                return i

            lower_interval = self.interval_to_int(self.intervals[i])
            if i + 1 != len(self.intervals):
                upper_interval = self.interval_to_int(self.intervals[i + 1])

            #if i + 1 == len(self.intervals) or self.intervals[i] < interval < self.intervals[i + 1]:
            if i + 1 == len(self.intervals) or lower_interval < interval < upper_interval:
                index = i + 1
                root_note = self.notes[0]
                added_note = root_note.clone().set_transpose(interval)
                self.notes.insert(index, added_note)
                self.intervals.insert(index, interval)
                return index

    # ensures note is part of chord and returns index of self.notes where the note was added
    def ensure_note_exists_old(self, interval) -> int:
        for i in range(len(self.intervals)):
            if interval == self.intervals[i]:
                return i
            if i + 1 == len(self.intervals) or self.intervals[i] < interval < self.intervals[i + 1]:
                index = i + 1
                root_note = self.notes[0]
                added_note = root_note.clone().set_transpose(interval)
                self.notes.insert(index, added_note)
                self.intervals.insert(index, interval)
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
    'maj11': McGillChord.maj11,
    '13': '13',
    'min11': 'm11',
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
