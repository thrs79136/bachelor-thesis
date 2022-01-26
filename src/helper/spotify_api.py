import string
import os
import spotipy
import logging
from .. import settings
from spotipy.oauth2 import SpotifyClientCredentials

from src.models.spotify_song_data import SpotifySongData

global spotify_client
logger = logging.getLogger(__name__)


def init():
    global spotify_client
    os.environ["SPOTIPY_CLIENT_ID"] = "f07521880b844d5395aa7dde0588a6bf"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "ade1c1e5bb314845a334a7b890f1968a"
    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def get_song_data(song_name: str, artist: str) -> SpotifySongData:
    global spotify_client

    id = __get_spotify_song_id(song_name, artist)

    if id is None:
        return None
    audio_features = get_audio_features(id)
    return SpotifySongData.from_spotify_api_response(audio_features)


def get_audio_features(song_id: string):
    global spotify_client
    return spotify_client.audio_features([song_id])


def __get_spotify_song_id(song_name: str, artist: str) -> string:
    global spotify_client

    try:
        # print(spotify)
        searchResult = spotify_client.search(q=f'artist:{artist} track:{song_name}', type='track')
    except:
        logger.error('Failed to execute search query')
        return None

    allTracks = searchResult['tracks']['items']
    if len(allTracks) == 0:
        logger.warning(f'Song \'{artist} - {song_name}\' could not be found on Spotify')
        return None
    return allTracks[0]['id']


