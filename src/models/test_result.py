class TestResult:

    def __init__(self, feature, pvalue):
        self.feature = feature
        # self.correlation = correlation
        self.pvalue = pvalue

    def __str__(self):
        return f'{self.feature.feature_id.replace("_", " ")} & {round(self.pvalue, 5)}'
