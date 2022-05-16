from src.models.mcgill_songdata import Section
from src.models.mgill_chord import MajOrMin, RomNumNotations, RomNumNotation
from typing import List

from src.models.song import Song


class Progression:
    def __init__(self, chords: List[str]):
        self.repr = ', '.join(chords)
        self.chords = []
        for chord in chords:
            chord_type = MajOrMin.Major
            if chord.islower():
                chord_type = MajOrMin.Minor
            chord_name = chord.upper()
            if chord_name[0] == 'B':
                chord_name = chord_name[1:]
            self.chords.append(RomNumNotation(RomNumNotations[chord_name], chord_name, chord_type))

    def __getitem__(self, index):
        return self.chords[index]

    def __len__(self):
        return len(self.chords)

    def __repr__(self):
        return self.repr


progressions = [

    Progression(['I', 'V', 'vi', 'IV']),
    Progression(['vi', 'IV', 'I', 'V']),
    Progression(['ii', 'V', 'I']),
    Progression(['I', 'IV', 'V']),
    Progression(['I', 'IV', 'vi', 'V']),
    Progression(['i', 'bIII', 'bVII', 'IV']),
    Progression(['i', 'bVII', 'v', 'bVI']),
    Progression(['I', 'V', 'ii', 'IV'])
]

progressions_dict = {}


def section_contains_progressions(section: Section) -> dict:
    used_progressions = {}
    automaton_index = {}

    for index, prog in enumerate(progressions):
        automaton_index[index] = 0
        used_progressions[prog] = False

    song_prog = section.chord_progression
    for chord_index, chord in enumerate(song_prog):
        for p_index, progression in enumerate(progressions):
            if progression[automaton_index[p_index]] == chord:
                automaton_index[p_index] += 1
                if automaton_index[p_index] == len(progression):
                    # found end of progression
                    automaton_index[p_index] = 0
                    used_progressions[progression] = True
            else:
                automaton_index[p_index] = 0
    return used_progressions

prog_count_dict = {}

def count_progression(prog: List[RomNumNotation]):
    print(prog)
    prog_str = ','.join([repr(chord) for chord in prog])
    if prog_count_dict.get(prog_str, -1) == -1:
        prog_count_dict[prog_str] = 1
    else:
        prog_count_dict[prog_str] += 1


def find_progressions(songs: List[Song]):
    for song in songs:
        for section in song.mcgill_billboard_song_data.sections:
            prog_length = len(section.chord_progression)
            for i in range(prog_length - 3):
                #sub_progression1 = section.chord_progression[i:i+3]
                sub_progression2 = section.chord_progression[i:i+4]
                #count_progression(sub_progression1)
                count_progression(sub_progression2)

            #sub_progression = section.chord_progression[-3:]
            #count_progression(sub_progression)

    sorted_progressions = {k: v for k, v in sorted(prog_count_dict.items(), key=lambda item: item[1], reverse=True)}
    breap_koint = 1


def identify_chord_progressions(songs: List[Song]):
    find_progressions(songs)


    count_dict = {}
    for prog in progressions:
        count_dict[prog] = 0
    for song in songs:
        for section in song.mcgill_billboard_song_data.sections:
            used_progressions = section_contains_progressions(section)
            for k, v in used_progressions.items():
                if v:
                    count_dict[k] += 1
                    print(f'{song}, {section.name}, {k}')

    a = count_dict

