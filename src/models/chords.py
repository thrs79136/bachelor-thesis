import string
from enum import Enum
from operator import mod
from typing import List

#
# class Chord:
#     # intervals are described as the number of semitones
#     def __init__(self, root_note: string, integer_notation: List[int]):
#         self.notes = list(map(lambda i: Note((Note(root_note) + i) % 12), integer_notation))
#         x = 1
#
#
# # exampe: C E G
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
