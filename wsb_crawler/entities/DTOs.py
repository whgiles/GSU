from abc import ABC, abstractmethod


class FullSubmissionSummary(ABC):
    partial_submission_summaries = list()
    meta_summary = None

    def __init__(self, rockets: int, sentiment: float):
        self.rockets = rockets
        self.sum_of_positive_sentiment = float()
        self.sum_of_negative_sentiment = float()
        self.number_of_positive_sentiment = int()
        self.number_of_negative_sentiment = float()
        self.analyze_sentiment(sentiment)

    def analyze_sentiment(self, sentiment: float):
        if sentiment > 0:
            self.sum_of_positive_sentiment = sentiment
            self.number_of_positive_sentiment = 1
        elif sentiment < 0:
            self.sum_of_negative_sentiment = sentiment
            self.number_of_negative_sentiment = 1

    @abstractmethod
    def add_to_full_summary(self):
        pass

    @classmethod
    def dump_class_vars(cls):
        cls.meta_summary = list()
        cls.partial_submission_summaries = list()


class SubmissionTickerSummary(FullSubmissionSummary):

    def __init__(self, ticker: str, rockets: int, sentiment: float):
        super().__init__(rockets, sentiment)
        self.ticker = ticker

    def add_to_full_summary(self):
        super().partial_submission_summaries.append(self)


class SubmissionMetaSummary(FullSubmissionSummary):
    name = 'meta'

    def __init__(self, rockets: int, sentiment: float):
        super().__init__(rockets, sentiment)

    def add_to_full_summary(self):
        if super().meta_summary is not None:
            raise Exception("A SubmissionMetaSummary already exists in super. "
                            "Try calling FullSubmissionSummary.dump_class_vars()")
        FullSubmissionSummary.meta_summary = self
