import string
from typing import List, TextIO
import json

from src.helper.mcgill_lexer import lexer
from src.models.mcgill_songdata.bar import Bar

from src.models.mcgill_songdata.section import Section
from src.models.mcgill_songdata.repetition import Repetition
from src.models.mcgill_songdata.pause import Pause
from src.models.mcgill_songdata.instrument import Instrument


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

            if tok.type == 'SILENCE_END':
                pass
            elif tok.type == 'SECTION_ID':
                section_name = lexer.token().value
                if current_section is not None:
                    self.sections.append(current_section)
                    # add progression before creating new section
                    current_section.add_chord_progression()

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
                self.tonic_changes.append(tok.value.split(' ')[1])
                current_section.tonic_change = tok.value.split(' ')[1]
            elif tok.type == 'METRE_CHANGE':
                value = tok.value
                current_section.content.append(value)
                self.metre_changes.append(value)

