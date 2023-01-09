import logging
from typing import TextIO
import ply.lex as lex
from parker.chords import *

# from src.models.mcgill_songdata.mgill_chord import McGillChord
from src.models.mcgill_songdata.mgill_chord import McGillChord

logger = logging.getLogger(__name__)

tokens = (
    'SECTION_NAME',
    'SECTION_ID',
    'BAR_LINE',
    'CHORD',
    'INSTRUMENT',
    'DOT',
    'COMMA',
    'REPEAT',
    'TONIC_CHANGE',
    'SILENCE_END',
    'ARROW',
    'NOTHING',
    'METRE_CHANGE',
    'PAUSE',
    'ASTERIX'
)


# t_SECTION_NAME = r"([a-z]|-)+[a-z][^(,|\n)]*" old
# t_SECTION_NAME = r"[a-z]+[a-z-]+,?[^:]"
# t_SECTION_ID = r"[A-Z]'*?,"
t_BAR_LINE = r"\|"
t_INSTRUMENT = r"((\([a-z ]+\)?)|([a-z ]+?\)))[^(\s|\n)]*"
t_DOT = r"\."
t_COMMA = r","
t_REPEAT = r"x[0-9]+"
t_TONIC_CHANGE = r"tonic:\s(A|B|C|D|E|F|G)b?\#?"
t_SILENCE_END = r"(silence|end)"
t_ARROW = r"->"
t_NOTHING = r"Z"
t_METRE_CHANGE = r"\([1-9]/[1-9]\)|(metre: [1-9]/[1-9])"
t_PAUSE = r"(&pause)|N"
t_ASTERIX = r"\*"

t_ignore = ' \n'


def t_CHORD(tok):
    r"[C|D|E|F|G|A|B](b|\#)?:.*?[^ ]*"

    tok.value = McGillChord(tok.value)
    return tok


def t_SECTION_NAME(tok):
    r"[a-z]+[a-z- ]+(,|\n)"

    tok.value = tok.value[:-1]
    return tok


def t_SECTION_ID(tok):
    r"[A-Z]'*?,"

    tok.value = tok.value[:-1]
    return tok


def t_error(tok):
    logger.warning("Illegal character '%s'" % tok.value[0])
    tok.lexer.skip(1)


global lexer
lexer = lex.lex()



