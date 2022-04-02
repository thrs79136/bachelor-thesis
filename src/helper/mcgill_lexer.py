import logging
from typing import TextIO
import ply.lex as lex
from parker.chords import *

from src.models.mgill_chord import McGillChord

logger = logging.getLogger(__name__)

mcgill_to_parker_chord = {
    'maj': 'M',
    'min': 'm'
}

tokens = (
    'SECTION_NAME',
    'SECTION_ID',
    'BAR_LINE',
    'CHORD',
    'INSTRUMENT',
    'DOT',
    'COMMA',
    'SILENCE_END',
    'ARROW',
    'NOTHING',
    'METRE_CHANGE'
)

t_SECTION_NAME = r"[a-z]+?[^,]*"
t_SECTION_ID = r"[A-Z]'*?,"
t_BAR_LINE = r"\|"
t_INSTRUMENT = r"((\([a-z]+\)?)|([a-z]+?\)))[^( |\n)]*"
t_DOT = r"\."
t_COMMA = r","
t_SILENCE_END = r"(silence|end)"
t_ARROW = r"->"
t_NOTHING = r"N|Z"
t_METRE_CHANGE = r"\([1-9]/[1-9]\)"

t_ignore = ' \n'


def t_CHORD(tok):
    r"[C|D|E|F|G|A|B](b|\#)?:.*?[^ ]*"

    tok.value = McGillChord(tok.value)
    return tok

    # parker_chord_name = mcgill_to_parker_chord.get(t.value[2:], '')
    # if parker_chord_name == '':
    #     print(f'Could not find chord {t.value}')
    #     logger.error(f'Could not find chord {t.value}')
    # chord = Chord(t.value[0] + parker_chord_name)
    # t.value = chord
    # return t


def t_error(tok):
    logger.warning("Illegal character '%s'" % tok.value[0])
    tok.lexer.skip(1)


global lexer
lexer = lex.lex()



