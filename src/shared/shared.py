import pandas as pd

from src.helper.absolute_surprise import get_song_surprise, get_different_progressions_feature
from src.helper.absolute_surprise_chords import get_song_chord_surprise
from src.models.song import Song
from src.models.song_feature import SongFeature
from sklearn import preprocessing

mcgill_F1 = 11

# ₀₁₂₃₄₅₆₇₈₉

def init_song_features():
    global song_features_dict
    # pandas dataframes
    global mcgill_df
    global normalized_mcgill_df
    global spotify_year_df

    global feature_file_path
    global non_y_axis_features

song_features_dict = {
    'decade': SongFeature('decade', 'Jahrzehnt', '', Song.get_decade, is_nominal=True),
    'year': SongFeature('year', 'Jahr', '', Song.get_chart_year),
    'artist': SongFeature('artist', 'Künstler', '', Song.get_artist, is_numerical=False),
    'chart_pos': SongFeature('chart_pos', 'Höchste Chartposition', '', Song.get_peak_chart_position),
    'genre': SongFeature('genre', 'Genre', '', Song.get_genres_id, is_numerical=False, is_nominal=True),

    # Spotify
    'spotify_popularity': SongFeature('spotify_popularity', 'Spotify Popularity', '', Song.get_spotify_popularity),

    'acousticness': SongFeature('acousticness', 'Acousticness', '1', Song.get_spotify_feature, ['acousticness']),
    'danceability': SongFeature('danceability', 'Danceability', '2', Song.get_spotify_feature, ['danceability']),
    'duration_ms': SongFeature('duration_ms', 'Liedlänge in s', '3', Song.get_spotify_feature, ['duration_ms']),
    'energy': SongFeature('energy', 'Energy', '4', Song.get_spotify_feature, ['energy']),
    'instrumentalness': SongFeature('instrumentalness', 'Instrumentalness', '5', Song.get_spotify_feature, ['instrumentalness']),
    'key': SongFeature('key', 'Tonart', '6', Song.get_spotify_feature, ['key'], is_nominal=True, nominal_labels=['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/B', 'H']),
    'loudness': SongFeature('loudness', 'Lautstärke in dB',     '7', Song.get_spotify_feature, ['loudness']),
    'mode': SongFeature('mode', 'Tongeschlecht',                '8', Song.get_spotify_feature, parameters=['mode'], is_nominal=True, nominal_labels=['Moll', 'Dur']),
    'speechiness': SongFeature('speechiness', 'Speechiness',    '9', Song.get_spotify_feature, parameters=['speechiness']),
    'tempo': SongFeature('tempo', 'Tempo',                      '10', Song.get_spotify_feature, parameters=['tempo']),
    'valence': SongFeature('valence', 'Stimmung',               '11', Song.get_spotify_feature, parameters=['valence']),

    # McGil BillBoard
    # chord type percentages
    'minor_percentage': SongFeature('minor_percentage', 'Anteil von Mollakkorden', '12', Song.get_minor_count),
    'major_percentage': SongFeature('major_percentage', 'Anteil von Durakkorden', '13', Song.get_major_count),
    'neither_chords': SongFeature('neither_chords', 'Anteil von Akkorden ohne Terz', '14', Song.get_neither_count),

    'get_added_seventh_use': SongFeature('get_added_seventh_use', 'Anteil von Septakkorden', '15',
                                         Song.get_added_seventh_use),
    # too many 0 values
    # 'get_added_sixth_use': SongFeature('get_added_sixth_use', 'Anteil von Sextakkorden', '', Song.get_added_sixth_use),
    # 'power_chords': SongFeature('power_chords', 'Powerchords', '', Song.get_power_chord_use),


    'non_triad_chords_percentage': SongFeature('non_triad_chords_percentage',
                                               'Akkorde, die keinen Dreiklang enthalten', '16',
                                               Song.get_non_triad_rate),
    'minor_or_major': SongFeature('minor_or_major', 'Anteil von Moll- oder Durdreiklängen', '17',
                                  Song.standard_chord_perc),

    'tonic_percentage': SongFeature('tonic_percentage', 'Anteil der Tonika', 'Tonika', Song.chord_frequency, ['I']),
    'supertonic_percentage': SongFeature('supertonic_percentage', 'Anteil der Supertonika', 'Supertonika', Song.chord_frequency,
                                         ['II']),
    'dominant_percentage': SongFeature('dominant_percentage', 'Anteil der Dominante', 'Dominante', Song.chord_frequency,
                                       ['V']),
    # 'i_to_v': SongFeature('i_to_v', 'Häufigkeit des Übergangs I->V', '', Song.chord_transition_test,
    #                       parameters=[('I', 'V')]),
    'v_to_i': SongFeature('v_to_i', 'Häufigkeit des Übergangs V->I', '18', Song.chord_transition_test,
                          parameters=[('V', 'I')]),



    'circle_of_fifths_dist': SongFeature('circle_of_fifths_dist', 'Abstände im Quintenzirkel', '19', Song.analyze_different_keys2),
    'circle_of_fifths_dist_largest_dist': SongFeature('circle_of_fifths_dist_largest_dist', 'Abstände im Quintenzirkel (Größte Distanz)', '20', Song.analyze_different_keys_largest_distance),

    'chord_distances': SongFeature('chord_distances', 'Akkordabstände', '21', Song.get_chord_distances),
    'chord_distances2': SongFeature('chord_distances2', 'Akkordabstände (Bassnote)', '22', Song.get_chord_distances2),

    'different_chords': SongFeature('different_chords', 'Anzahl verschiedener Akkorde',  '23', Song.get_different_chords_count),
    'different_progressions': SongFeature('different_progressions', 'Verschiedene Akkordfolgen', '24', get_different_progressions_feature),
    'different_notes': SongFeature('different_notes', 'Anzahl verschiedener Noten', '25', Song.get_different_notes_count),
    'average_chord_count_per_bar': SongFeature('average_chord_count_per_bar', 'Anzahl verschiedener Akkorde pro Takt', '26', Song.get_average_chords_per_bar),

    'different_sections_count': SongFeature('different_sections_count', 'Anzahl verschiedener Sektionen', '27',
                                            Song.get_different_sections_count),

    'section_repetitions': SongFeature('section_repetitions', 'Anzahl von Wiederholungen bereits gespielter Sektionen',
                                       '28', Song.get_section_repetitions_count),
    'chorus_repetitions': SongFeature('chorus_repetitions', 'Anzahl Wiederholungen des Rephrains', '29', Song.get_chorus_repetitions),

    'guitar': SongFeature('guitar', 'Vorkommen von Gitarre', 'Gitarre', Song.get_instrument_usage, parameters=['guitar'], is_boolean=True, nominal_labels=["Keine Verwendung von Gitarre", "Verwendung von Gitarre"]),
    'synthesizer': SongFeature('synthesizer', 'Vorkommen von Synthesizer', 'Synthesizer', Song.get_instrument_usage, parameters=['synthesizer'], is_boolean=True, nominal_labels=["Keine Verwendung von keinen Synthesizer", "Verwendung von Synthesizer"]),
    'piano': SongFeature('piano', 'Vorkommen von Klavier', 'Klavier', Song.get_instrument_usage,
                         parameters=['piano'], is_boolean=True, nominal_labels=["Keine Verwendung von Klavier", "Verwendung von Klavier"]),
    'saxophone': SongFeature('saxophone', 'Vorkommen von Saxophon', 'Saxophon', Song.get_instrument_usage,
                             parameters=['saxophone'], is_boolean=True, nominal_labels=["Keine Verwendung von Saxophon", "Verwendung von Saxophon"]),
    'strings': SongFeature('strings', 'Vorkommen von Streichinstrumenten', 'Streichinstrumente', Song.get_instrument_usage,
                           parameters=['strings'], is_boolean=True, nominal_labels=["Keine Verwendung von Streichinstrumenten", "Verwendung von Streichinstrumenten"]),
    'trumpet': SongFeature('trumpet', 'Vorkommen von Trompete', 'Trompete', Song.get_instrument_usage,
                           parameters=['trumpet'], is_boolean=True, nominal_labels=["Keine Verwendung von Trompete", "Verwendung von Trompete"]),

    # Sentiment Analysis
    'love': SongFeature('love', 'Sentiment: Liebe',                 'Liebe',  Song.get_sentiment, parameters=['love'], is_sentiment_feature=True),
    'anger': SongFeature('anger', 'Sentiment: Wut',                 'Wut',    Song.get_sentiment, parameters=['anger'], is_sentiment_feature=True),
    'sadness': SongFeature('sadness', 'Sentiment: Trauer',          'Trauer', Song.get_sentiment, parameters=['sadness'], is_sentiment_feature=True),
    'joy': SongFeature('joy', 'Sentiment: Freude',                  'Freude', Song.get_sentiment, parameters=['joy'], is_sentiment_feature=True),
    # 'fear': SongFeature('fear', 'Sentiment: Angst',                 'Angst',  Song.get_sentiment, parameters=['fear'], is_sentiment_feature=True),
    # 'surprise': SongFeature('surprise', 'Sentiment: Überraschung',  'Überraschung', Song.get_sentiment, parameters=['surprise'], is_sentiment_feature=True),

    'negative': SongFeature('negative', 'Sentiment: Negativ',       'Negativ', Song.get_sentiment_pos_neg, parameters=['NEGATIVE'], is_sentiment_feature=True),
    'positive': SongFeature('positive', 'Sentiment: Positiv',       'Positiv', Song.get_sentiment_pos_neg, parameters=['POSITIVE'], is_sentiment_feature=True),

    # 'chord_distances': SongFeature('chord_distances', 'Akkordabstände', '', Song.get_chord_distances),

    # 'III_percentage': SongFeature('III_percentage', 'Anteil der III', '', Song.chord_frequency, ['III']),
    # 'IV_percentage': SongFeature('IV_percentage', 'Anteil der IV', '', Song.chord_frequency2,
    #                                      ['IV']),
    # 'VI_percentage': SongFeature('VI_percentage', 'Anteil der VI', '', Song.chord_frequency, ['VI']),
    # 'VII_percentage': SongFeature('VII_percentage', 'Anteil der VII', '', Song.chord_frequency, ['VII']),
}

non_y_axis_features = ['decade', 'year', 'artist', 'chart_pos', 'genre', 'spotify_popularity']


def normalize(df):
    df_z_scaled = df.copy()

    # apply normalization technique to Column 1
    columns = [feature.feature_id for feature in song_features_dict.values() if feature.feature_id not in non_y_axis_features and feature.is_numerical]
    for column in columns:
        df_z_scaled[column] = (df_z_scaled[column] - df_z_scaled[column].mean()) / df_z_scaled[column].std()

    # view normalized data
    return df_z_scaled

feature_file_path = '../data/csv/song_features.csv'
dataset2_path = '../data/csv/years/spotify.csv'

mcgill_df = pd.read_csv(feature_file_path)
normalized_mcgill_df = normalize(mcgill_df)

spotify_year_df = pd.read_csv(dataset2_path)

