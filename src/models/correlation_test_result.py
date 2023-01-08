from src.models.test_result import TestResult


class CorrelationTestResult(TestResult):
    def __init__(self, feature, correlation, pvalue):
        super().__init__(feature, pvalue)
        self.feature = feature
        self.correlation = correlation
        self.pvalue = pvalue

    def __str__(self):
        return f'{self.feature.feature_id.replace("_", " ")} & {round(self.correlation, 5)} & {round(self.pvalue, 5)}'

