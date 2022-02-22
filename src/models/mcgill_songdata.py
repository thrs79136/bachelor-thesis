import logging
import string
from typing import List, TextIO
import re

import parker.chords
from parker.chords import Chord

from src.helper.mcgill_lexer import lexer

logger = logging.getLogger(__name__)

class Bar:
    def __init__(self, chords: List[Chord]):
        self.chords = chords


class Section:
    def __init__(self, id, name, bars: List[Bar]):
        pass


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

        while True:
            tok = lexer.token()
            if not tok:
                break

            if type(tok.value) is parker.chords.Chord:
                print('Hallo ein Chord')
            else:
                print(tok.value)




