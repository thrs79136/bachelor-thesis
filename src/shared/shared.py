import pandas as pd

from src.helper.absolute_surprise import get_song_surprise, get_different_progressions_feature
from src.helper.absolute_surprise_chords import get_song_chord_surprise
from src.models.song import Song
from src.models.song_feature import SongFeature
from sklearn import preprocessing



def init_song_features():
    global song_features_dict
    # pandas dataframes
    global mcgill_df
    global sentiment_df
    global normalized_mcgill_df
    global spotify_year_df

    global feature_file_path
    global non_musical_features

song_features_dict = {
    'decade': SongFeature('decade', 'Jahrzehnt', '', Song.get_decade, is_nominal=True),
    'year': SongFeature('year', 'Jahr', '', Song.get_chart_year),
    'artist': SongFeature('artist', 'Künstler', '', Song.get_artist, is_numerical=False),
    'chart_pos': SongFeature('chart_pos', 'Höchste Chartposition', '', Song.get_peak_chart_position),
    'genre': SongFeature('genre', 'Genre', '', Song.get_genres_id, is_numerical=False, is_nominal=True),
    'genre_groups': SongFeature('genre_groups', 'Genre Group', '', Song.get_group_genres, is_numerical=False, is_nominal=True),

    # Spotify
    'spotify_popularity': SongFeature('spotify_popularity', 'Spotify Popularity', '', Song.get_spotify_popularity),
    'spotify_id': SongFeature('spotify_id', 'Spotify Id', '', Song.get_spotify_id, is_numerical=False),

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
    'minor_chords': SongFeature('minor_chords', 'Anteil von Mollakkorden', '12', Song.get_minor_count),
    'major_chords': SongFeature('major_chords', 'Anteil von Durakkorden', '13', Song.get_major_count),
    'neither_chords': SongFeature('neither_chords', 'Anteil von Akkorden ohne Terz', '14', Song.get_neither_count),

    'seventh_chords': SongFeature('seventh_chords', 'Anteil von Septakkorden', '15',
                                         Song.get_added_seventh_use),

    'non_triad_chords': SongFeature('non_triad_chords',
                                               'Anteil Akkorde ohne Dreiklang', '16',
                                               Song.get_non_triad_rate),
    'standard_triads': SongFeature('standard_triads', 'Anteil von Moll- oder Durdreiklängen', '17',
                                  Song.standard_chord_perc),

    'tonic_chords': SongFeature('tonic_chords', 'Anteil der Tonika', '18', Song.chord_frequency, ['I']),
    'supertonic_chords': SongFeature('supertonic_chords', 'Anteil der Supertonika', '19', Song.chord_frequency,
                                         ['II']),
    'dominant_chords': SongFeature('dominant_chords', 'Anteil der Dominante', '20', Song.chord_frequency,
                                       ['V']),
    'v_to_i': SongFeature('v_to_i', 'Häufigkeit des Übergangs V->I', '21', Song.chord_transition_test,
                          parameters=[('V', 'I')]),

    'circle_of_fifths': SongFeature('circle_of_fifths', 'Abstände im Quintenzirkel', '22', Song.analyze_different_keys2),
    'circle_of_fifths_max': SongFeature('circle_of_fifths_max', 'Abstände im Quintenzirkel (Größte Distanz)', '23', Song.analyze_different_keys_largest_distance),

    'root_distances': SongFeature('root_distances', 'Akkordabstände', '24', Song.get_chord_distances),
    'bass_distances': SongFeature('bass_distances', 'Akkordabstände (Bassnote)', '25', Song.get_chord_distances2),

    'different_chords': SongFeature('different_chords', 'Anzahl verschiedener Akkorde',  '26', Song.get_different_chords_count),
    'different_progressions': SongFeature('different_progressions', 'Verschiedene Akkordfolgen', '27', get_different_progressions_feature),
    'different_notes': SongFeature('different_notes', 'Anzahl verschiedener Noten', '28', Song.get_different_notes_count),
    'chords_per_bar': SongFeature('chords_per_bar', 'Anzahl verschiedener Akkorde pro Takt', '29', Song.get_average_chords_per_bar),

    'different_sections': SongFeature('different_sections', 'Anzahl verschiedener Sektionen', '30',
                                            Song.get_different_sections_count),

    'section_repetitions': SongFeature('section_repetitions', 'Anzahl Wiederholungen bereits gespielter Sektionen',
                                       '31', Song.get_section_repetitions_count),
    'chorus_repetitions': SongFeature('chorus_repetitions', 'Anzahl Wiederholungen des Rephrains', '32', Song.get_chorus_repetitions),

    'guitar': SongFeature('guitar', 'Vorkommen von Gitarre', '33', Song.get_instrument_usage, parameters=['guitar'], is_boolean=True, nominal_labels=["Ohne Gitarre", "Mit Gitarre"]),
    'synthesizer': SongFeature('synthesizer', 'Vorkommen von Synthesizer', '34', Song.get_instrument_usage, parameters=['synthesizer'], is_boolean=True, nominal_labels=["Ohne Synthesizer", "Mit Synthesizer"]),
    'piano': SongFeature('piano', 'Vorkommen von Klavier', '35', Song.get_instrument_usage,
                         parameters=['piano'], is_boolean=True, nominal_labels=["Ohne Klavier", "Mit Klavier"]),
    'saxophone': SongFeature('saxophone', 'Vorkommen von Saxophon', '36', Song.get_instrument_usage,
                             parameters=['saxophone'], is_boolean=True, nominal_labels=["Ohne Saxophon", "Mit Saxophon"]),
    'trumpet': SongFeature('trumpet', 'Vorkommen von Trompete', '37', Song.get_instrument_usage,
                           parameters=['trumpet'], is_boolean=True,
                           nominal_labels=["Ohne Trompete", "Mit Trompete"]),
    'strings': SongFeature('strings', 'Vorkommen von Streichinstrumenten', '38', Song.get_instrument_usage,
                           parameters=['strings'], is_boolean=True, nominal_labels=["Ohne Streichinstrumente", "Mit Streichinstrumenten"]),

    # Sentiment Analysis
    'love': SongFeature('love', 'Sentiment: Liebe',                 '39',  Song.get_sentiment, parameters=['love'], is_sentiment_feature=True),
    'anger': SongFeature('anger', 'Sentiment: Wut',                 '40',    Song.get_sentiment, parameters=['anger'], is_sentiment_feature=True),
    'sadness': SongFeature('sadness', 'Sentiment: Trauer',          '41', Song.get_sentiment, parameters=['sadness'], is_sentiment_feature=True),
    'joy': SongFeature('joy', 'Sentiment: Freude',                  '42', Song.get_sentiment, parameters=['joy'], is_sentiment_feature=True),

    'negative': SongFeature('negative', 'Sentiment: Negativ',       '43', Song.get_sentiment_pos_neg, parameters=['NEGATIVE'], is_sentiment_feature=True),
    'positive': SongFeature('positive', 'Sentiment: Positiv',       '44', Song.get_sentiment_pos_neg, parameters=['POSITIVE'], is_sentiment_feature=True),
}

non_musical_features = ['decade', 'year', 'artist', 'chart_pos', 'genre', 'spotify_popularity', 'spotify_id', 'genre_groups']


def normalize(df):
    df_z_scaled = df.copy()

    # apply normalization technique to Column 1
    columns = [feature.feature_id for feature in song_features_dict.values() if feature.feature_id not in non_musical_features and feature.is_numerical]
    for column in columns:
        df_z_scaled[column] = (df_z_scaled[column] - df_z_scaled[column].mean()) / df_z_scaled[column].std()

    # view normalized data
    return df_z_scaled

feature_file_path = '../data/csv/song_features.csv'
median_file_path = '../data/csv/year_features.csv'

mcgill_df = pd.read_csv(feature_file_path)
sentiment_df = mcgill_df[~mcgill_df['joy'].isnull()]
normalized_mcgill_df = normalize(mcgill_df)
median_df = pd.read_csv(median_file_path)
