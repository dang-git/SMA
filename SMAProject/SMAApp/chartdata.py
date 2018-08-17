class ChartData:
    """ Chartdata Object """

    # Used slots so chartdata will have smaller size in bytes
    __slots__ = ["timeline", "source", "composition", "hashtags", "sentiments", "polarity_table"]

    def __init__(self,timeline=None,source=None,composition=None,hashtags=None,sentiments=None,polarity_table=None):
        self.timeline = timeline or {}
        self.source = source or {}
        self.composition = composition or {}
        self.hashtags = hashtags or {}
        self.sentiments = sentiments or {}
        self.polarity_table = polarity_table or {}