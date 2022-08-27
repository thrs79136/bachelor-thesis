from typing import List

import pandas as pd

from src.models.spotify_track import SpotifyTrack, audio_feature_keys


class SpotifyPlaylist:
    def __init__(self, tracks):
        self.tracks: List[SpotifyTrack] = tracks

    def to_dataframe(self):
        data = []
        for track in self.tracks:
            data_dict = {
                'id': track.spotify_id,
                'artists': track.artists,
                'name': track.name
            }

            for feature in audio_feature_keys:
                data_dict[feature] = track.audio_features[feature]

            data.append(
                data_dict
            )

        return pd.DataFrame(data)