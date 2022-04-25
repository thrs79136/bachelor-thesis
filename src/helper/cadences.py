from typing import List

from src.models.mgill_chord import RomNumNotations, RomNumNotation
from src.models.song import Song


class Cadences:
    def __init__(self):
        # V-I or V-i
        self.authentic_cadences = 0
        # IV-I (major or minor)
        self.plagal_cadences = 0
        # phrase ends on V
        self.half_cadences = 0
        # V-iv
        self.deceptive_cadences = 0


def identify_cadences(song: Song):
    cadences = Cadences()

    for section in song.mcgill_billboard_song_data.sections:
        prog = section.chord_progression
        # authentic cadence
        if prog[-2] == RomNumNotations.V and (prog[-1].roman_number == RomNumNotations.I):
            cadences.authentic_cadences += 1
        # plagal cadence

        # half cadence

        # deceptive cadence

        #print(section.chord_progression)

    debug_var = 1

