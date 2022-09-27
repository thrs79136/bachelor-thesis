from collections import OrderedDict

from src.models.mgill_chord import note_to_interval, MajOrMin, McGillChord

key_dict = {0: 'C',
            1: 'Des',
            2: 'D',
            3: 'Es',
            4: 'E',
            5: 'F',
            6: 'Ges',
            7: 'G',
            8: 'As',
            9: 'A',
            10: 'B',
            11: 'H'}

major_intervals = [0, 2, 4, 5, 7, 9, 11]
# minor_intervals = [0, 2, 3, 5, 7, 8, 10]

class Scale:
    def __init__(self, tonic, circlePos):
        self.tonic_name = tonic
        self.tonic_number = note_to_interval[tonic]
        self.circlePos = circlePos
        tonic_number = note_to_interval[tonic]
        self.major_notes = [(tonic_number + interval) % 12 for interval in major_intervals]
        # self.minor_notes = [(tonic_number + interval) % 12 for interval in minor_intervals]

    def check_if_notes_are_part_of_scale(self, note_names):
        note_ids = [note_to_interval[note] for note in note_names]

        return set(note_ids) <= set(self.major_notes)

    def check_single_note(self, note_name):
        note_id = note_to_interval[note_name]
        return note_id in self.major_notes

    def get_notes(self):
        return [key_dict[note] for note in self.major_notes]


circle_of_fifths = {
    note_to_interval['C']: Scale('C', 0),
    note_to_interval['G']: Scale('G', 1),
    note_to_interval['D']: Scale('D', 2),
    note_to_interval['A']: Scale('A', 3),
    note_to_interval['E']: Scale('E', 4),
    note_to_interval['B']: Scale('B', 5),
    note_to_interval['Gb']: Scale('Gb', 6),
    note_to_interval['Db']: Scale('Db', 7),
    note_to_interval['Ab']: Scale('Ab', 8),
    note_to_interval['Eb']: Scale('Eb', 9),
    note_to_interval['Bb']: Scale('Bb', 10),
    note_to_interval['F']: Scale('F', 11),
}

def get_scale_distance(scale_key_1, scale_key_2):

    # idx_1 = list(circle_of_fifths.keys()).index(scale_key_1)
    # idx_2 = list(circle_of_fifths.keys()).index(scale_key_2)

    i = (scale_key_1 - scale_key_2) % 12
    j = (scale_key_2 - scale_key_1) % 1
    if i < j:
        return -i
    return j


def get_minor_scale_id(major_tonic):
    return (note_to_interval[major_tonic] - 9) % 12


# TODO create result class
def get_corresponding_scale_distance_for_chord(chord: McGillChord, tonic, maj_or_min, previous_scale_key = None):
    note_names = [f'{note.base_name}{note.accidentals.name}' for note in chord.notes]

    if previous_scale_key is None:
        if maj_or_min == MajOrMin.Major:
            scale_key = note_to_interval[tonic]
        else:
            scale_key = get_minor_scale_id(tonic)
    else:
        scale_key = previous_scale_key

    if circle_of_fifths[scale_key].check_if_notes_are_part_of_scale(note_names):
        return 0, None, 0

    # check neighboring scales from lowest to highest distance
    for i in range(1, 7):
        check_scale_key = (scale_key + i) % 12
        if circle_of_fifths[check_scale_key].check_if_notes_are_part_of_scale(note_names):
            # print(chord.mcgill_chord_name + ' key: ' + str(circle_of_fifths[check_scale_key].tonic_name))
            return i/6, check_scale_key, i
        check_scale_key = (scale_key - i) % 12
        if circle_of_fifths[check_scale_key].check_if_notes_are_part_of_scale(note_names):
            # print(chord.mcgill_chord_name + ' key: ' + str(circle_of_fifths[check_scale_key].tonic_name))
            return i/6, check_scale_key, -i


    root = chord.root.base_name + chord.root.accidentals.name
    chord_scale_key = note_to_interval[root]
    if chord.chord_type == MajOrMin.Minor:
        chord_scale_key = get_minor_scale_id(tonic)
    elif chord.chord_type == MajOrMin.Major:
        x = 42

    if chord.chord_type == MajOrMin.Neither:
        cloned_chord = chord.clone()

        notes_without_tensions = []
        for i,v in enumerate(chord.mcgill_intervals):
            x = 42
        indices = [i for i, v in enumerate(chord.mcgill_intervals) if v <= 11]


        test_res = get_corresponding_scale_distance_for_chord(clone_chord, tonic, maj_or_min, previous_scale_key)
        x = 42
    res = get_scale_distance(scale_key, chord_scale_key)
    return abs(res)/6, chord_scale_key, res


pentatonic_maj_intervals = [0, 2, 4, 7, 9]
pentatonic_min_intervals = [0, 3, 5, 7, 10]



def is_part_of_pentatonic_scale(chord: McGillChord, tonic):
    global pentatonic_min_intervals

    tonic_id = note_to_interval[tonic]

    count = 0
    for note in chord.notes:
        name = note.base_name + note.accidentals.name
        note_id = note_to_interval[name]

        for interval in pentatonic_min_intervals:
            if (tonic_id + interval) % 12 == note_id:
                count += 1
                continue

    return count


def part_of_scale(chord: McGillChord, tonic):
    tonic_id = note_to_interval[tonic]
    scale = circle_of_fifths[tonic_id]

    count = 0

    for note in chord.notes:
        name = note.base_name + note.accidentals.name
        if not scale.check_single_note(name):
            count += 1

    return count



