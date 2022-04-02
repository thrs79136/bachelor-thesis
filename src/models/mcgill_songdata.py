import logging
import string
from typing import List, TextIO
from enum import Enum
import re

import parker.chords
from parker.chords import Chord

from src.helper.mcgill_lexer import lexer

logger = logging.getLogger(__name__)


class Bar:
    def __init__(self):
        self.chords = []

    def __str__(self):
        return ', '.join([f'{chord.root.base_name}{chord.extension}' for chord in self.chords])


# contains bars
class Section:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.content = []

    def __str__(self):
        return self.name


class InstrumentType(Enum):
    BEGINNING = 0
    END = 1
    SECTION = 2


class Instrument:
    def __init__(self, name):

        opening_brace = name[0] == '('
        closing_brace = name[len(name)-1] == ')'
        if opening_brace and not closing_brace:
            self.name = name[1:]
            self.instrumentType = InstrumentType.BEGINNING
        elif not opening_brace and closing_brace:
            self.name = name[:-1]
            self.instrumentType = InstrumentType.END
        else:
            self.name = name[1:-1]
            self.instrumentType = InstrumentType.SECTION


class McGillSongData:
    def __init__(self, id: string):

        self.id: int = id
        self.metre: string = None
        self.tonic: string = None
        self.sections: List[Section] = None
        self.readfile()

    def readfile(self):
        filepath = f'../data/songs/mcgill-billboard/{self.id.zfill(4)}/salami_chords.txt'
        f = open(filepath, 'r')
        f.readline(); f.readline()

        self.metre = f.readline()[9:-1]
        self.tonic = f.readline()[9:-1]
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
                break

            if tok.type == 'SILENCE_END':
                pass
            elif tok.type == 'SECTION_ID':
                section_name = lexer.token().value
                if current_section is not None:
                    self.sections.append(current_section)
                current_section = Section(tok.value, section_name)
            elif tok.type == 'BAR_LINE':
                if current_bar is not None and len(current_bar.chords) != 0:
                    current_section.content.append(current_bar)
                current_bar = Bar()
            elif tok.type == 'INSTRUMENT':
                current_section.content.append(Instrument(tok.value))
            elif tok.type == 'CHORD':
                current_bar.chords.append(tok.value)
                # print('Chord')
