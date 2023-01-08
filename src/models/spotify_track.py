import pandas as pd

from src.helper.spotify_api import get_audio_features

audio_feature_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

def to_dataframe(tracks, classifier_key, classifier_value_fn):
    data = []
    for track in tracks:
        data_dict = {
            'id': track.spotify_id,
            'artists': track.artists,
            'name': track.name,
            classifier_key: classifier_value_fn(track)
        }

        for feature in audio_feature_keys:
            data_dict[feature] = track.audio_features[feature]

        data.append(
            data_dict
        )

    return pd.DataFrame(data)


class SpotifyTrack:
    def __init__(self, spotify_id, artists, name, popularity, audio_features, decade, genre=None):
        self.spotify_id = spotify_id
        self.artists = artists
        self.name = name
        self.popularity = popularity
        self.audio_features = {key: audio_features[key] for key in audio_feature_keys}
        self.decade = decade
        self.genre = genre

    def get_genre(self):
        return self.genre

    @classmethod
    def from_api_response(cls, response, decade):
        track = response['track']

        track_id = track['id']
        artists = ' & '.join([artist['name'] for artist in track['artists']])
        name = track['name']
        popularity = track['popularity']
        audio_features = get_audio_features(track_id)
        return cls(track_id, artists, name, popularity, audio_features[0], decade)

    @classmethod
    def from_api_response_genre(cls, response, genre):
        track = response['track']

        track_id = track['id']
        artists = ' & '.join([artist['name'] for artist in track['artists']])
        name = track['name']
        popularity = track['popularity']
        audio_features = get_audio_features(track_id)
        if audio_features == [None]:
            return None
        return cls(track_id, artists, name, popularity, audio_features[0], None, genre)
