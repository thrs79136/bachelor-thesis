class SongFeature:

    def __init__(self, feature_id, feature_display_name, feature_fn, parameters=[], is_numerical=True):
        self.feature_id = feature_id
        self.feature_display_name = feature_display_name
        self.feature_fn = feature_fn
        self.parameters = parameters
        self.is_numerical = is_numerical
