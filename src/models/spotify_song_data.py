import ast
import string

audio_feature_keys = ['danceability', 'duration_ms', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo']


class SpotifySongData:


    def __init__(self, audio_features_dictionary):
        self.audio_features_dictionary = audio_features_dictionary

    @classmethod
    def from_spotify_api_response(cls, audio_features_response):
        global audio_feature_keys

        audio_features_dictionary = {key: audio_features_response[0][key] for key in audio_feature_keys}
        return cls(audio_features_dictionary)

    @classmethod
    def from_csv(cls, audio_features: string):
        return cls(ast.literal_eval(audio_features))

    def get_csv_row(self):
        return [self.danceability, self.energy, self.key, self.loudness, self.mode, self.speechinesss,
                self.acousticness, self.instrumentalness, self.liveness, self.valence, self.tempo]

    def __repr__(self):
        return str(self.audio_features_dictionary)
