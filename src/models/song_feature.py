class SongFeature:

    def __init__(self, feature_id, feature_display_name, latex_name, feature_fn, parameters=[], is_numerical=True, is_boolean=False):
        self.feature_id = feature_id
        self.feature_display_name = feature_display_name
        self.latex_name = latex_name
        self.feature_fn = feature_fn
        self.parameters = parameters
        self.is_numerical = is_numerical
        self.is_boolean = is_boolean



