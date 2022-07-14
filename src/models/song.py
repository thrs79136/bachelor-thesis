import json
from typing import List, Iterable
import re
import logging

from src.helper.lastfm_helper import LastFmHelper
from src.models.mcgill_songdata import McGillSongData, Section, Bar
from src.models.mgill_chord import MajOrMin, note_to_interval, McGillChord
from src.models.scales import circle_of_fifths, get_corresponding_scale_distance_for_chord, is_part_of_pentatonic_scale, \
    part_of_scale
from src.models.spotify_song_data import SpotifySongData
from src.helper.spotify_api import get_song_data_by_spotify_id, get_spotify_song_id
from src.shared import settings
import ast

logger = logging.getLogger(__name__)

global key_dict
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

key_dict2 = {0: 'C',
            1: 'Db',
            2: 'D',
            3: 'Eb',
            4: 'E',
            5: 'F',
            6: 'Gb',
            7: 'G',
            8: 'Ab',
            9: 'A',
            10: 'Bb',
            11: 'B'
             }

class Song:
    def __init__(self,
                 mcgill_billboard_id: str,
                 artist: str,
                 song_name: str,
                 chart_year: int,
                 peak_chart_position: int,
                 genres: List[str] = [],
                 spotify_song_data: SpotifySongData = None,
                 mcgill_billboard_song_data: McGillSongData = None,
                 load_api_song_data: bool = True
                 ):

        self.spotify_id = None
        self.mcgill_billboard_id = mcgill_billboard_id
        self.artist = artist
        self.song_name = song_name
        self.chart_year = chart_year
        self.peak_chart_position = peak_chart_position
        self.genres = genres
        self.spotify_song_data = spotify_song_data
        self.mcgill_billboard_song_data = mcgill_billboard_song_data
        if self.mcgill_billboard_song_data is None:
            logger.debug(f'[Song.__init__] Reading McGillSongData for "{repr(self)}"')
            self.mcgill_billboard_song_data = McGillSongData(mcgill_billboard_id)
        if load_api_song_data:
            self.add_song_data()
        self.cadences = None

    @classmethod
    def from_csv_row(cls, csv_row: Iterable):
        id = csv_row['mcgill_billboard_id']
        artist = csv_row['artist']
        song_name = csv_row['song_name']
        chart_year = int(csv_row['chart_year'])
        peak_chart_position = int(csv_row['peak_chart_position'])
        genres = ast.literal_eval(csv_row['genres'])
        spotify_song_data = SpotifySongData.from_csv(csv_row['spotify_song_data'])
        return cls(id, artist, song_name, chart_year, peak_chart_position, genres, spotify_song_data, load_api_song_data=False)

    @classmethod
    def from_mcgill_csv_row(cls, csv_row: Iterable):
        artist = csv_row['artist']
        if artist == '':
            return None
        id = csv_row['id']
        title = csv_row['title']
        chart_year = int(csv_row['chart_date'][0:4])
        peak_rank = int(csv_row['peak_rank'])
        return cls(id, artist, title, chart_year, peak_rank)

    # single section
    @classmethod
    def from_code(cls, chord_names):

        mc_gill = McGillSongData('-1', False)
        mc_gill.tonic = 'C'
        #mc_gill.sections.append(())
        bars = []
        for i, chord_name in enumerate(chord_names):
            if i % 4 == 0:
                bar = Bar()
                bars.append(bar)
            chord = McGillChord(chord_name)
            bar.content.append(chord)

        section = Section(None, None)
        section.content = bars
        mc_gill.sections = [section]

        spotify_data = SpotifySongData({'mode': 1})


        song = cls(None, None, None, None, None,
                   mcgill_billboard_song_data=mc_gill, spotify_song_data=spotify_data, load_api_song_data=False)
        return song



    def add_song_data(self):
        # spotify
        self.spotify_id = get_spotify_song_id(self.song_name, self.artist)
        spotify_song_data = get_song_data_by_spotify_id(self.spotify_id)
        self.set_spotify_song_data(spotify_song_data)

        # TODO remove return
        return
        # lastfm for genres
        tags = LastFmHelper.get_track_tags(self.song_name, self.artist)

        if tags is not None:
            song_genres = []
            for tag in tags:
                if tag in settings.all_genres:
                    song_genres.append(tag)

            if len(song_genres) == 0:
                logger.warning(f'{self}: Could not found any genres')
                tags_str = ', '.join(list(map(lambda tag_name: f'\'{tag_name}\'', tags)))
                logger.warning(f'Tags: {tags_str}')

            self.set_genres(song_genres)

    def set_spotify_song_data(self, spotify_song_data: SpotifySongData):
        self.spotify_song_data = spotify_song_data

    def set_mcgill_billboard_song_data(self, mcgill_song_data: McGillSongData):
        self.mcgill_billboard_song_data = mcgill_song_data

    def set_genres(self, genres: List[str]):
        self.genres = genres

    def get_csv_row(self) -> Iterable:
        song_data = [self.mcgill_billboard_id, self.artist, f'{self.song_name}', self.chart_year,
                     self.peak_chart_position, self.genres, repr(self.spotify_song_data), self.spotify_id]
        return song_data

    def get_peak_chart_position(self):
        return self.peak_chart_position

    def get_decade(self):
        year = int(self.chart_year)
        return year - (year % 10)

    def get_spotify_feature(self, key):
        return self.spotify_song_data.audio_features_dictionary[key]

    def get_different_sections_count(self):
        section_ids = set()
        for section in self.mcgill_billboard_song_data.sections:
            section_ids.add(section.id)

        return len(section_ids)

    def get_different_chords_count(self):
        different_chords_dict = {}

        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_chords()
            for chord in chords:
                res = different_chords_dict.get(chord.mcgill_chord_name, -1)
                if res == -1:
                    different_chords_dict[chord.mcgill_chord_name] = True

        return len(different_chords_dict.items())

    def get_metre_changes_count(self):
        return len(self.mcgill_billboard_song_data.metre_changes)


    def get_non_triad_rate(self):
        analyzed_chords_count = 0
        non_triad_chords = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            analyzed_chords_count += len(chords)
            for chord in chords:
                if 7 not in chord.mcgill_intervals or (3 not in chord.mcgill_intervals and 4 not in chord.mcgill_intervals):
                    non_triad_chords += 1
                # if chord.mcgill_intervals != [0, 3, 7] and chord.mcgill_intervals != [0, 4, 7]:
                #     non_triad_chords += 1

        return non_triad_chords / analyzed_chords_count

    def get_tonic_changes_count(self):
        return len(self.mcgill_billboard_song_data.tonic_changes)

    def get_minor_count(self):
        major_chords = 0
        minor_chords = 0
        neither_chords = 0
        chords_count = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            chords_count += len(chords)
            for chord in chords:
                chord_type = MajOrMin.Neither
                if 3 in chord.mcgill_intervals:
                    chord_type = MajOrMin.Minor
                    minor_chords += 1
                elif 4 in chord.mcgill_intervals:
                    chord_type = MajOrMin.Major
                    major_chords += 1

                if 3 in chord.mcgill_intervals and 4 in chord.mcgill_intervals:
                    neither_chords += 1

        return minor_chords / chords_count


    def get_tension_use(self):
        tension_numbers = ['7', '9', '11', '13']

        count = 0
        total_count = 0

        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()
            total_count += len(chords)
            for chord in chords:
                chord.mcgill_chord_name
                added_notes = re.findall(r'\d+', chord.mcgill_chord_name)

                for num in tension_numbers:
                    if num in added_notes:
                        count += 1
                        break

        return count / total_count


    def get_foreign_scale_notes(self):
        total_notes_count = 0
        foreign_notes = 0

        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()

            for chord in chords:
                total_notes_count += len(chord.notes)
                foreign_notes += part_of_scale(chord, self.mcgill_billboard_song_data.tonic)

        return foreign_notes / total_notes_count

    def get_section_repetitions_count(self):
        section_repetitions = {}
        for section in self.mcgill_billboard_song_data.sections:
            if section_repetitions.get(section.id, -1) == -1:
                section_repetitions[section.id] = 0
            else:
                section_repetitions[section.id] += 1

        return sum(section_repetitions.values())

    def bars_per_section(self):
        multiple_of_eight = 0
        for section in self.mcgill_billboard_song_data.sections:
            bar_count = 0
            for elem in section.content:
                if isinstance(elem, Bar):
                    bar_count += 1
            if bar_count % 8 == 0:
                multiple_of_eight += 1

        return multiple_of_eight / len(self.mcgill_billboard_song_data.sections)


    def another_test(self, transition_test):
        count = 0
        total_transitions_count = 0

        last_chord = None

        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()
            total_transitions_count += len(chords)
            for chord in chords:
                # first chord
                if last_chord is None:
                    last_chord = chord.roman_numeral_notation.roman_number
                    continue

                rom_num = chord.roman_numeral_notation.roman_number


                if last_chord == rom_num:
                    continue
                transition = (last_chord, rom_num)
                count += transition_test[transition]

                last_chord = rom_num

        total_transitions_count -= 1

        return count / total_transitions_count

    def chord_transition_test(self, transition: tuple):
        count = 0
        total_transitions_count = 0

        last_chord = None

        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()
            total_transitions_count += len(chords)
            for chord in chords:
                # first chord
                if last_chord is None:
                    last_chord = chord.roman_numeral_notation.roman_number
                    continue

                rom_num = chord.roman_numeral_notation.roman_number

                if transition[0] == last_chord and transition[1] == rom_num:
                    count += 1

                last_chord = rom_num

        total_transitions_count -= 1

        return count / total_transitions_count


    def chord_frequency2(self, rom_num_check):
        count = 0
        total_chords_count = 0
        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()
            total_chords_count += len(chords)
            for chord in chords:
                # type = chord.roman_numeral_notation.maj_or_min
                # if type == MajOrMin.Major or type == MajOrMin.Minor:
                rom_num = str(chord.roman_numeral_notation)
                if rom_num == rom_num_check:
                    count += 1

        return count / total_chords_count

    def chord_frequency(self, rom_num_check):
        count = 0
        total_chords_count = 0
        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()
            total_chords_count += len(chords)
            for chord in chords:
                rom_num = chord.roman_numeral_notation.roman_number
                if rom_num == rom_num_check:
                    count += 1

        return count / total_chords_count

    def pentatonic_notes(self):
        count = 0
        total_chords_count = 0

        pentatonic_count = 0
        total_notes_count = 0
        for section in self.mcgill_billboard_song_data.sections:
            chords = section.get_progression_chords()
            total_chords_count += len(chords)
            for chord in chords:
                total_notes_count += len(chord.notes)
                pentatonic_count += is_part_of_pentatonic_scale(chord, self.mcgill_billboard_song_data.tonic)
        return pentatonic_count / total_notes_count


    #TODO make this the only fn
    def analyze_different_keys_general(self, process_result_fn, process_final_result_fn, different_chords_once=False, use_previous_harmony=False):
        result = 0

        different_chords_dict = {}

       # tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        tonic = self.mcgill_billboard_song_data.tonic
        min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary[
                                           'mode'] == 1 else MajOrMin.Minor

        analyzed_chords_count = 0
        previous_harmony = None

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            tonic_change = section.get_tonic_change_at_end()
            analyzed_chords_count += len(chords)

            if not different_chords_once:
                for chord in chords:
                    previous_harmony_key = previous_harmony if use_previous_harmony is not None else None
                    dist, previous_harmony, scale_id = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj, previous_scale_key=previous_harmony_key)
                    result = process_result_fn(result, dist, scale_id)
                    # result += dist

                if tonic_change is not None:
                    tonic = tonic_change

            else:
                for chord in chords:
                    if different_chords_dict.get(chord.mcgill_chord_name, -1) == -1:
                        different_chords_dict[chord.mcgill_chord_name] = chord

        if different_chords_once:
            for chord in different_chords_dict.values():
                dist, previous_harmony = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj)
                result = process_result_fn(result, dist)

        result = process_final_result_fn(result, analyzed_chords_count)
        return result
        #return sum / analyzed_chords_count

    def analyze_different_keys(self, use_previous_harmony=True):
        sum = 0

        different_chords_dict = {}

       # tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        tonic = self.mcgill_billboard_song_data.tonic
        min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary[
                                           'mode'] == 1 else MajOrMin.Minor

        analyzed_chords_count = 0
        previous_harmony = None

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            tonic_change = section.get_tonic_change_at_end()
            analyzed_chords_count += len(chords)
            for chord in chords:
                previous_harmony_key = previous_harmony if use_previous_harmony is not None else None
                dist, previous_harmony = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj, previous_scale_key=previous_harmony_key)
                sum += dist

            if tonic_change is not None:
                tonic = tonic_change

        return sum / analyzed_chords_count

    def analyze_different_keys_different_chords(self):
        sum = 0

        different_chords_dict = {}

       # tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        tonic = self.mcgill_billboard_song_data.tonic
        min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary[
                                           'mode'] == 1 else MajOrMin.Minor

        analyzed_chords_count = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            tonic_change = section.get_tonic_change_at_end()
            #analyzed_chords_count += len(chords)
            for chord in chords:
                if different_chords_dict.get(chord.mcgill_chord_name, -1) == -1:
                    different_chords_dict[chord.mcgill_chord_name] = chord
                    dist, previous_harmony = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj)
                    sum += dist

            if tonic_change is not None:
                tonic = tonic_change

        return sum / len(different_chords_dict)

    def analyze_different_keys_largest_distance(self):
        max_distance = 0

        different_chords_dict = {}

       # tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        tonic = self.mcgill_billboard_song_data.tonic
        min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary[
                                           'mode'] == 1 else MajOrMin.Minor

        analyzed_chords_count = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            tonic_change = section.get_tonic_change_at_end()
            #analyzed_chords_count += len(chords)
            for chord in chords:
                if different_chords_dict.get(chord.mcgill_chord_name, -1) == -1:
                    different_chords_dict[chord.mcgill_chord_name] = chord
                    dist = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj)
                    max_distance = max(max_distance, dist)

            if tonic_change is not None:
                tonic = tonic_change

        return max_distance

    def analyze_different_keys_largest_distance(self):
        max_distance = 0

        different_chords_dict = {}

       # tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        tonic = self.mcgill_billboard_song_data.tonic
        min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary[
                                           'mode'] == 1 else MajOrMin.Minor

        analyzed_chords_count = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            tonic_change = section.get_tonic_change_at_end()
            #analyzed_chords_count += len(chords)
            for chord in chords:
                if different_chords_dict.get(chord.mcgill_chord_name, -1) == -1:
                    different_chords_dict[chord.mcgill_chord_name] = chord
                    dist, previous_harmony = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj)
                    max_distance = max(max_distance, dist)

            if tonic_change is not None:
                tonic = tonic_change

        return max_distance


    def analyze_different_keys2(self):
        sum = 0

        different_chords_dict = {}

        tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        tonic = self.mcgill_billboard_song_data.tonic
        analyzed_chords_count = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            #tonic_change = section.get_tonic_change_at_end()
            analyzed_chords_count += len(chords)
            for chord in chords:
                if different_chords_dict.get(chord.mcgill_chord_name, -1):
                    different_chords_dict[chord.mcgill_chord_name] = chord

        for chord in different_chords_dict.values():
            min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary[
                                               'mode'] == 1 else MajOrMin.Minor
            dist, prev_harm, test = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj)
            sum += dist

        return sum / len(different_chords_dict)

    def analyze_different_keys_old(self):
        sum = 0

        tonic = key_dict2[self.spotify_song_data.audio_features_dictionary['key']]
        analyzed_chords_count = 0

        sections = self.mcgill_billboard_song_data.sections
        for section in sections:
            chords = section.get_progression_chords()
            analyzed_chords_count += len(chords)
            for chord in chords:
                min_or_maj = MajOrMin.Major if self.spotify_song_data.audio_features_dictionary['mode'] == 1 else MajOrMin.Minor
                dist = get_corresponding_scale_distance_for_chord(chord, tonic, min_or_maj)

                if dist == 7:
                    bp = self.song_name + ' - ' + self.artist
                    v = 1

                sum += dist

        return sum/analyzed_chords_count

    def get_genres(self):
        return self.genres

    def get_used_instruments(self):
        return self.mcgill_billboard_song_data.instruments

    def get_metre(self):
        return self.mcgill_billboard_song_data.metre

    def get_mode(self):
        mode = self.spotify_song_data.audio_features_dictionary['mode']
        if mode == 1:
            return 'Dur'
        else:
            return 'Moll'

    def get_key(self):
        key = self.spotify_song_data.audio_features_dictionary['key']
        return key_dict[key]

    def __str__(self):
        return f'{self.mcgill_billboard_id} {self.artist} - {self.song_name}'

    def __repr__(self):
        return f'{self.mcgill_billboard_id} {self.artist} - {self.song_name}'

    # compare songs by peak chart position
    def __lt__(self, other):
        return self.peak_chart_position < other.peak_chart_position

