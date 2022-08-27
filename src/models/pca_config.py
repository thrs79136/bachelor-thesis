from src.shared import song_features


class PCAConfig:
    def __init__(self, feature_names, color_fn, color_labels):
        self.features = [dictionaries.song_features_dict[name] for name in feature_names]
        # self.feature_names = feature_names
        self.color_fn = color_fn
        self.color_labels = list(color_labels.items())
        self.all_colors = list(color_labels.values())

    def get_song_color(self, song):
        return self.color_fn(song)
