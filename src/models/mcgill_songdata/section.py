# contains bars
import json
from typing import List

from src.models.mcgill_songdata.mgill_chord import RomNumNotation, McGillChord

from src.models.mcgill_songdata.bar import Bar
from src.models.mcgill_songdata.repetition import Repetition


class Section:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.content = []
        self.chord_progression: List[RomNumNotation] = []
        self.tonic_change = None

    def add_chord_progression(self):
        for bar in self.content:
            if isinstance(bar, Bar):
                for chord in bar.content:
                    if isinstance(chord, McGillChord):
                        roman_num = chord.roman_numeral_notation
                        if len(self.chord_progression) != 0:
                            if self.chord_progression[-1] != roman_num:
                                self.chord_progression.append(roman_num)
                        else:
                            self.chord_progression.append(roman_num)
            elif isinstance(bar, Repetition):
                # repetition -> add progression from last bar
                if len(self.chord_progression) == 0:
                    continue

                if self.chord_progression[0] == self.chord_progression[-1]:
                    self.chord_progression.extend(self.chord_progression[1:]*bar.count)
                else:
                    self.chord_progression.extend(self.chord_progression*bar.count)

    def get_chords(self):
        chords = []
        for bar in self.content:
            if isinstance(bar, Bar):
                for chord in bar.content:
                    if isinstance(chord, McGillChord):
                        chords.append(chord)
        return chords

    def get_progression_chords(self):
        chords = []
        for bar in self.content:
            if isinstance(bar, Bar):
                for chord in bar.content:
                    if isinstance(chord, McGillChord):
                        if len(chords) == 0 or chords[len(chords) - 1].mcgill_chord_name != chord.mcgill_chord_name:
                            chords.append(chord)
        return chords

    def get_tonic_change_at_end(self):
        return self.tonic_change


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def __str__(self):
        return self.name
