from src.helper.absolute_surprise import get_song_surprise, get_different_progressions_feature
from src.helper.absolute_surprise_chords import get_song_chord_surprise
from src.models.song import Song
from src.models.song_feature import SongFeature


def init_song_features():
    global song_features_dict

    song_features_dict = {
        'decade': SongFeature('decade', 'Jahrzehnt', Song.get_decade),
        'year': SongFeature('year', 'Jahr', Song.get_chart_year),
        'artist': SongFeature('artist', 'Künstler', Song.get_artist),

        'minor_percentage': SongFeature('minor_percentage', 'Anteil von Mollakkorden', Song.get_minor_count),
        'major_percentage': SongFeature('major_percentage', 'Anteil von Durakkorden', Song.get_major_count),

        'absolute_surprise': SongFeature('absolute_surprise', 'Überraschende Akkordfolgen', get_song_surprise),
        'circle_of_fifths_dist': SongFeature('circle_of_fifths_dist', 'Abstände im Quintenzirkel', Song.analyze_different_keys2),
        'circle_of_fifths_dist_largest_dist': SongFeature('circle_of_fifths_dist_largest_dist', 'Abstände im Quintenzirkel (Groesste Distanz)', Song.analyze_different_keys_largest_distance),
        'danceability': SongFeature('danceability', 'Danceability', Song.get_spotify_feature, ['danceability']),
        'energy': SongFeature('energy', 'Energy', Song.get_spotify_feature, ['energy']),
        'tonic_percentage': SongFeature('tonic_percentage', 'Anteil der Tonika', Song.chord_frequency, ['I']),
        'supertonic_percentage': SongFeature('tonic_percentage', 'Anteil der Supertonika', Song.chord_frequency2, ['II']),
        'dominant_percentage': SongFeature('dominant_percentage', 'Anteil der Dominante', Song.chord_frequency, ['V']),
        'non_triad_chords_percentage': SongFeature('non_triad_chords_percentage', 'Akkorde, die keinen Dreiklang enthalten', Song.get_non_triad_rate),
        'different_sections_count': SongFeature('different_sections_count', 'Anzahl verschiedener Sektionen', Song.get_different_sections_count),
        'get_added_seventh_use': SongFeature('get_added_seventh_use', 'Anteil von Septakkorden', Song.get_added_seventh_use),
        'get_added_sixth_use': SongFeature('get_added_sixth_use', '6-Akkorde', Song.get_added_sixth_use),
        'power_chords': SongFeature('power_chords', 'Powerchords', Song.get_power_chord_use),
        'neither_chords': SongFeature('neither_chords', 'Weder Moll noch Dur', Song.get_neither_count),

        'section_repetitions': SongFeature('section_repetitions', 'Anzahl von Wiederholungen bereits gespielter Sektionen',
                                               Song.get_section_repetitions_count),
        'i_to_v': SongFeature('i_to_v', 'Häufigkeit vom Übergang von I zu V', Song.chord_transition_test, parameters=[('I', 'V')]),
        'v_to_i': SongFeature('v_to_i', 'Häufigkeit vom Übergang von V zu I', Song.chord_transition_test,
                              parameters=[('V', 'I')]),

        'chart_pos': SongFeature('chart_pos', 'Höchste Chartposition', Song.get_peak_chart_position),
        'spotify_popularity': SongFeature('spotify_popularity', 'Spotify Popularity', Song.get_spotify_popularity),
        'genre': SongFeature('genre', 'Genre', Song.get_genres_id),
        'mode': SongFeature('mode', 'Tongeschlecht', Song.get_spotify_feature, parameters=['mode']),

        'tempo': SongFeature('tempo', 'Tempo', Song.get_spotify_feature, parameters=['tempo']),
        'valence': SongFeature('Valence', 'valence', Song.get_spotify_feature, parameters=['valence']),
        'duration': SongFeature('Dauer in ms', 'duration', Song.get_spotify_feature, parameters=['duration_ms']),
        'chord_distances': SongFeature('Akkordabstände', 'chord_distances', Song.get_chord_distances),
        'different_chords': SongFeature('Verschiedene Akkorde', 'different_chords', Song.get_different_chords_count),
        'different_progressions': SongFeature('Verschiedene Akkordfolgen', 'different_progressions', get_different_progressions_feature),
        'chord_surprise': SongFeature('Überraschende Akkorde', 'chord_surprise', get_song_chord_surprise),
        'different_notes': SongFeature('Anzahl erschiedener Noten', 'different_notes', Song.get_different_notes_count)


        # 'chord_distances': SongFeature('chord_distances', 'Akkordabstände', Song.get_chord_distances),



    # 'III_percentage': SongFeature('III_percentage', 'Anteil der III', Song.chord_frequency, ['III']),
        # 'IV_percentage': SongFeature('IV_percentage', 'Anteil der IV', Song.chord_frequency2,
        #                                      ['IV']),
        # 'VI_percentage': SongFeature('VI_percentage', 'Anteil der VI', Song.chord_frequency, ['VI']),
        # 'VII_percentage': SongFeature('VII_percentage', 'Anteil der VII', Song.chord_frequency, ['VII']),
    }
