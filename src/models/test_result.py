class TestResult:

    def __init__(self, feature_id, correlation, pvalue):
        self.feature_id = feature_id
        self.correlation = correlation
        self.pvalue = pvalue

    def __str__(self):
        return f'{self.feature_id.replace("_", " ")} & {round(self.correlation, 5)} & {round(self.pvalue, 5)}'

