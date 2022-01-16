from src.models.song import Song, SpotifySongData
import string
import os
import spotipy
import settings
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyHelper:

    spotify: SpotifyClientCredentials

    @staticmethod
    def init_spotify_client():
        os.environ["SPOTIPY_CLIENT_ID"] = "f07521880b844d5395aa7dde0588a6bf"
        os.environ["SPOTIPY_CLIENT_SECRET"] = "ade1c1e5bb314845a334a7b890f1968a"
        SpotifyHelper.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    @staticmethod
    def get_song_data(song: Song) -> SpotifySongData:
        id = SpotifyHelper.__get_spotify_song_id(song)
        if id is None:
            return None
        audio_features = SpotifyHelper.__get_audio_features(id)
        return SpotifySongData(audio_features)

    @staticmethod
    def __get_audio_features(song_id: string):
        return SpotifyHelper.spotify.audio_features([song_id])

    @staticmethod
    def __get_spotify_song_id(song: Song) -> string:
        try:
            searchResult = SpotifyHelper.spotify.search(q=f'artist:{song.artist} track:{song.song_name}', type='track')
        except:
            settings.logger.error('Failed to execute search query')
            return None

        allTracks = searchResult['tracks']['items']
        if len(allTracks) == 0:
            settings.logger.warning(f'Song \'{song}\' could not be found on Spotify')
            return None
        return allTracks[0]['id']
