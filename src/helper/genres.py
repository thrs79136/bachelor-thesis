from collections import defaultdict

genres_genres = ['rock', 'pop-rock', 'pop', 'soul', 'country', 'funk-soul']
genres_accepted_genres = ['rock', 'pop', 'country', 'funk', 'soul']


def create_genres_dict(songs):
    genre_dict = defaultdict(list)
    classified_songs_count = 0

    for song in songs:
        song_genres = '-'.join(sorted([genre for genre in song.genres if genre in genres_accepted_genres]))
        if song_genres in genres_genres:
            genre_dict[song_genres].append(song)
            classified_songs_count += 1

    print('classified songs count:' + str(classified_songs_count))
    return genre_dict

def transform_genre_to_string(song):
    return '-'.join(sorted([genre for genre in song.genres if genre in genres_accepted_genres]))

def transform_genre_string(genre):
    return '-'.join(sorted([g for g in genre.split('.') if g in genres_accepted_genres]))

def create_genres_df(df):
    df = df.drop(df[~df.genre.map(transform_genre_string).isin(genres_genres)].index)
    return df
