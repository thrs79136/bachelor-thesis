class SongFeature:

    def __init__(self, feature_id, feature_display_name, latex_id, feature_fn, parameters=[], is_numerical=True, is_boolean=False, is_nominal=False, is_sentiment_feature=False, nominal_labels=None, process_fn=None):
        self.feature_id = feature_id
        self.display_name = feature_display_name
        self.latex_id = latex_id
        self.latex_name = f'F_{{L,{latex_id}}}'
        self.feature_fn = feature_fn
        self.parameters = parameters
        self.is_numerical = is_numerical
        self.is_boolean = is_boolean
        self.is_nominal = is_nominal
        if is_boolean:
            self.is_nominal = True
        self.nominal_labels = nominal_labels
        self.process_fn = process_fn

        self.is_sentiment_feature = is_sentiment_feature

