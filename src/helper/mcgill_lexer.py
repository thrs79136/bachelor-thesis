import logging
from typing import TextIO
import ply.lex as lex
from parker.chords import *

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
    'SILENCE_END'
)

t_SECTION_NAME = r"[a-z]+?,"
t_SECTION_ID = r"[A-Z]'*?,"
t_BAR_LINE = r"\|"
t_INSTRUMENT = r"((\([a-z]*?)|([a-z]*?\)))"
t_DOT = r"\."
t_COMMA = r","
t_SILENCE_END = r"(silence|end)"

t_ignore = ' \n'


def t_CHORD(t):
    r"[C|D|E|F|G|A|B]b?:.*?[^ ]*"
    try:
        chord = Chord(t.value[0] + mcgill_to_parker_chord[t.value[2:]])
        return chord
    except:
        print(f'Could not find chord {t.value}')
        logger.error(f'Could not find chord {t.value}')
    return t


def t_error(t):
    logger.warning("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


global lexer
lexer = lex.lex()



