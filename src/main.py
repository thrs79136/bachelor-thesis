
# songs = []

# for dir_name in os.listdir('./data/mcgill-billboard/'):
#     f = open('./data/mcgill-billboard/' + dir_name + '/salami_chords.txt')
#     title = f.readline()[9:-1]
#     artist = f.readline()[10:-1]
#     songs.append(Song(dir_name, title, artist))

# print(songs)
import string

import settings
from spotify_api import SpotifyHelper

from src.lastfm_helper import LastFmHelper
from src.models.song import Song, SpotifySongData

genres = [
    'acoustic',
    'afrobeat',
    'alt-rock',
    'alternative',
    'ambient',
    'anime',
    'black-metal',
    'bluegrass',
    'blues',
    'bossanova',
    'brazil',
    'breakbeat',
    'british',
    'cantopop',
    'chicago-house',
    'children',
    'chill',
    'classical',
    'club',
    'comedy',
    'country',
    'dance',
    'dancehall',
    'death-metal',
    'deep-house',
    'detroit-techno',
    'disco',
    'disney',
    'drum-and-bass',
    'dub',
    'dubstep',
    'edm',
    'electro',
    'electronic',
    'emo',
    'folk',
    'forro',
    'french',
    'funk',
    'garage',
    'german',
    'gospel',
    'goth',
    'grindcore',
    'groove',
    'grunge',
    'guitar',
    'happy',
    'hard-rock',
    'hardcore',
    'hardstyle',
    'heavy-metal',
    'hip-hop',
    'holidays',
    'honky-tonk',
    'house',
    'idm',
    'indian',
    'indie',
    'indie-pop',
    'industrial',
    'iranian',
    'j-dance',
    'j-idol',
    'j-pop',
    'j-rock',
    'jazz',
    'k-pop',
    'kids',
    'latin',
    'latino',
    'malay',
    'mandopop',
    'metal',
    'metal-misc',
    'metalcore',
    'minimal-techno',
    'movies',
    'mpb',
    'new-age',
    'new-release',
    'opera',
    'pagode',
    'party',
    'philippines-opm',
    'piano',
    'pop',
    'pop-film',
    'post-dubstep',
    'power-pop',
    'progressive-house',
    'psych-rock',
    'punk',
    'punk-rock',
    'r-n-b',
    'rainy-day',
    'reggae',
    'reggaeton',
    'road-trip',
    'rock',
    'rock-n-roll',
    'rockabilly',
    'romance',
    'sad',
    'salsa',
    'samba',
    'sertanejo',
    'show-tunes',
    'singer-songwriter',
    'ska',
    'sleep',
    'songwriter',
    'soul',
    'soundtracks',
    'spanish',
    'study',
    'summer',
    'swedish',
    'synth-pop',
    'tango',
    'techno',
    'trance',
    'trip-hop',
    'turkish',
    'work-out',
    'world-music'
  ]


def merge_song_data(mcgill_billboard_id, artist: str, song_name: str) -> Song:
    song = Song(artist, song_name)
    # spotify
    spotify_song_data = SpotifyHelper.get_song_data(song)
    song.set_spotify_song_data(spotify_song_data)
    # lastfm for genres
    tags = LastFmHelper.get_track_tags(song)

    if tags is not None:
        song_genres = []
        for tag in tags:
            if tag in genres:
                song_genres.append(tag)

        if len(song_genres) == 0:
            settings.logger.warning(f'{song}: Could not found any genres')
            tags_str = ', '.join(list(map(lambda tag_name: f'\'{tag_name}\'', tags)))
            settings.logger.warning(f'Tags: {tags_str}')

        song.set_genres(song_genres)

    return song

settings.init_logger()
SpotifyHelper.init_spotify_client()

song = merge_song_data(1, '', 'niqihhifio')
x = 1

# 25tZHMv3ctlzqDaHAeuU9c
