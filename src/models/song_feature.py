class SongFeature:

    def __init__(self, feature_id, feature_display_name, feature_fn, parameters=[]):
        self.feature_id = feature_id
        self.feature_display_name = feature_display_name
        self.feature_fn = feature_fn
        self.parameters = parameters

