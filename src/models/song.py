from typing import List

class SpotifySongData:
    def __init__(self, audio_features_response):
        dict = audio_features_response[0]
        self.danceability = dict['danceability']
        self.energy = dict['energy']
        self.key = dict['key']
        self.loudness = dict['loudness']
        self.mode = dict['mode']
        self.speechinesss = dict['speechiness']
        self.acousticness = dict['acousticness']
        self.instrumentalness = dict['instrumentalness']
        self.liveness = dict['liveness']
        self.valence = dict['valence']
        self.tempo = dict['tempo']


class McGilBillboardSongData:
    def __init__(self, id):
        self.id = id


class Song:
    def __init__(self, artist, song_name):
        self.artist = artist
        self.song_name = song_name
        self.spotify_song_data = None
        self.mcgill_billboard_song_data = None
        self.genres = None

    def set_spotify_song_data(self, spotify_song_data: SpotifySongData):
        self.spotify_song_data = spotify_song_data

    def set_mcgill_billboard_song_data(self, mcgill_song_data: McGilBillboardSongData):
        self.mcgill_billboard_song_data = mcgill_song_data

    def set_genres(self, genres: List[str]):
        self.genres = genres

    def __str__(self):
        return self.artist + ' - ' + self.song_name

    def __repr__(self):
        return self.artist + " - " + self.song_name
