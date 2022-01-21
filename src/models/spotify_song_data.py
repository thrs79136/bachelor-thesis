class SpotifySongData:

    audio_feature_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

    def __init__(self, audio_features_dictionary):
        self.audio_features_dictionary = audio_features_dictionary

    @classmethod
    def from_spotify_api_response(cls, audio_features_response):
        audio_features_dictionary = {key: audio_features_response[0][key] for key in SpotifySongData.audio_feature_keys}
        return cls(audio_features_dictionary)

    def get_csv_row(self):
        return [self.danceability, self.energy, self.key, self.loudness, self.mode, self.speechinesss,
                self.acousticness, self.instrumentalness, self.liveness, self.valence, self.tempo]

    def __repr__(self):
        return f'{self.audio_features_dictionary}'
