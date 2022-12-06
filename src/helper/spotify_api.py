import string
import os
import spotipy
import logging

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from src.models.spotify_song_data import SpotifySongData

global spotify_client
logger = logging.getLogger(__name__)


def init_spotify():
    global spotify_client
    os.environ["SPOTIPY_CLIENT_ID"] = "f07521880b844d5395aa7dde0588a6bf"
    os.environ["SPOTIPY_CLIENT_SECRET"] = "ade1c1e5bb314845a334a7b890f1968a"
    spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    print(spotify_client)


playlist_ids = {
    '1950s': '37i9dQZF1DWSV3Tk4GO2fq',
    '1960s': '37i9dQZF1DXaKIA8E7WcJj',
    '1970s': '37i9dQZF1DWTJ7xPn4vNaz',
    '1980s': '37i9dQZF1DX4UtSsGT1Sbe',
    '1990s': '37i9dQZF1DXbTxeAdrVG2l',
    '2000s': '37i9dQZF1DX4o1oenSJRJd',
    '2010s': '37i9dQZF1DX5Ejj0EkURtP',
}

playlist_ids_genres = {
    'hiphop': '37i9dQZF1EQnqst5TRi17F',
    'pop': '37i9dQZF1DX7C2BlYJgCS5',
    'rock': '37i9dQZF1DX4vth7idTQch',
    'blues': '37i9dQZF1DXd9rSDyQguIk',
    'jazz': '37i9dQZF1DXbITWG1ZJKYt',
    'country': '37i9dQZF1DWZBCPUIUs2iR'
}

def get_playlist_genre(genre):
    print(f'get playlist for genre {genre}')
    results = spotify_client.playlist_tracks(playlist_ids_genres[genre])
    tracks = results['items']
    while results['next'] and len(tracks) < 50:
        results = spotify_client.next(results)
        tracks.extend(results['items'])
    return tracks

def get_playlist_tracks(decade):
    results = spotify_client.playlist_tracks(playlist_ids[decade])
    tracks = results['items']
    while results['next']:
        results = spotify_client.next(results)
        tracks.extend(results['items'])
    return tracks

# unused
def get_track_analysis(song):
    return spotify_client.audio_analysis(song.spotify_id)


def get_spotify_song_id(song_name: str, artist: str) -> string:
    global spotify_client

    print(f'{artist} - {song_name}')
    if song_name == 'Pressure':
        x = 2

    try:
        searchResult = spotify_client.search(q=f'artist:{artist} track:{song_name}', type='track')
    except:
        logger.error('Failed to execute search query')
        return None

    allTracks = searchResult['tracks']['items']
    if len(allTracks) == 0:
        logger.warning(f'Song \'{artist} - {song_name}\' could not be found on Spotify')
        return None
    for track in allTracks:
        if track is not None:
            return track['id']


def get_song_data_by_spotify_id(spotify_id) -> SpotifySongData:
    global spotify_client

    audio_features = get_audio_features(spotify_id)
    return SpotifySongData.from_spotify_api_response(audio_features)


def get_audio_features(song_id: string):
    global spotify_client
    return spotify_client.audio_features([song_id])


def get_popularity(song_id: string):
    global spotify_client

    res = spotify_client.track(song_id)
    return res['popularity']

def get_spotify_genres(song_id: string):
    global spotify_client

    res = spotify_client.track(song_id)
    artists = res['artists']
    if len(artists) == 0:
        return
    artist_id = res['artists'][0]['id']
    result = spotify_client.artist(artist_id)
    genres = result['genres']
    if len(genres) == 0:
        print(artists[0]['name'])
        return []
    return genres
