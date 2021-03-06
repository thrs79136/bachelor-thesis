import json
import logging
import string
from typing import List, TextIO
from enum import Enum
import re

import parker.chords
from parker.chords import Chord

from src.helper.mcgill_lexer import lexer
from src.models.mgill_chord import RomNumNotation, McGillChord

logger = logging.getLogger(__name__)


class Bar:
    def __init__(self):
        self.content = []

    def __str__(self):
        return ', '.join([f'{chord.root.base_name}{chord.extension}' for chord in self.content])


# contains bars
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


class InstrumentType(Enum):
    BEGINNING = 0
    END = 1
    SECTION = 2


class Instrument:
    def __init__(self, name):


        self.name = re.sub('[(),]', '', name)

         #print(f'{name} -> {self.name}')


        if self.name == 'flute)':
            x = 2

        opening_brace = '(' in name
        closing_brace = ')' in name
        if opening_brace and not closing_brace:
            self.instrumentType = InstrumentType.BEGINNING
        elif not opening_brace and closing_brace:
            self.instrumentType = InstrumentType.END
        else:
            self.instrumentType = InstrumentType.SECTION


class Repetition:
    def __init__(self, count):
        self.count = int(count)


class TonicChange:
    def __init__(self, tonic):
        self.tonic = tonic
        print(self.tonic)


class Pause:
    def __init__(self):
        pass


class McGillSongData:
    def __init__(self, id: string, parse_file = True):

        self.id: int = id
        self.metre: string = None
        self.tonic: string = None
        self.sections: List[Section] = None
        self.instruments = set()
        self.tonic_changes = []
        self.metre_changes = []
        if parse_file:
            self.readfile()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def readfile(self):
        filepath = f'../data/songs/mcgill-billboard/{self.id.zfill(4)}/salami_chords.txt'
        f = open(filepath, 'r')
        f.readline(); f.readline()

        # read metre and tonic
        line1 = f.readline()
        line2 = f.readline()[9:-1]
        if line1.startswith('# metre'):
            self.metre = line1[9:-1]
            self.tonic = line2
        else:
            self.tonic = line1[9:-1]
            self.metre = line2

        self.sections = []
        self.parse_chords(f)

        f.close()

    def parse_chords(self, file: TextIO):
        chords_text = ''
        for i, line in enumerate(file):
            splitstring = line.split('\t', 1)
            if len(splitstring) == 1:
                splitstring = line.split(' ', 1)
            if len(splitstring) > 1:
                section_info = splitstring[1]
                chords_text += section_info

        lexer.input(chords_text)

        current_section: Section = None
        current_bar: Bar = None

        while True:
            tok = lexer.token()
            if not tok:
                # finished lexing, add last section
                self.sections.append(current_section)
                break



            # print(f'{tok.value} (type: {tok.type})')
            # try:
            #     logger.debug(f'{tok.value} (type: {tok.type})')
            # except Exception:
            #     if self.id == '22':
            #         x =1
            #     pass

            # if self.id == '22':
            #     print(f'{tok.value} (type: {tok.type})')

            if tok.type == 'SILENCE_END':
                pass
            elif tok.type == 'SECTION_ID':
                section_name = lexer.token().value
                if current_section is not None:
                    self.sections.append(current_section)
                    # add progression before creating new section
                    current_section.add_chord_progression()
                    # print(current_section.chord_progression)

                current_section = Section(tok.value, section_name)
            elif tok.type == 'BAR_LINE':
                if current_section is not None and current_bar is not None and len(current_bar.content) != 0:
                    current_section.content.append(current_bar)
                current_bar = Bar()
            elif tok.type == 'INSTRUMENT':
                instrument = Instrument(tok.value)
                current_section.content.append(instrument)
                self.instruments.add(instrument.name)
            elif tok.type == 'CHORD':
                chord = tok.value
                chord.add_roman_numeral_notation(self.tonic)
                current_bar.content.append(chord)
            elif tok.type == 'REPEAT':
                current_section.content.append(Repetition(tok.value[1:]))
            elif tok.type == 'PAUSE':
                current_bar.content.append(Pause())
            elif tok.type == 'DOT':
                current_bar.content.append(current_bar.content[-1])
            elif tok.type == 'TONIC_CHANGE':
                #current_section.content.append(TonicChange(tok.value.split(' ')[1]))
                self.tonic_changes.append(tok.value.split(' ')[1])
                if current_section.tonic_change is not None:
                    x = 42
                current_section.tonic_change = tok.value.split(' ')[1]
                print('tonic change', self.id)
            elif tok.type == 'METRE_CHANGE':
                value = tok.value
                current_section.content.append(value)
                self.metre_changes.append(value)



