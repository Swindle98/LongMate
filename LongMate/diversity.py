import pandas as pd
import skbio as sk


class CommonDiveristy():
    # Attributes
    # Methods
    pass

class Alpha(CommonDiveristy):
    def __init__(self,counts):
        self.counts = counts
        pass

    def simpson(self):
        """
        Calculate the Simpson diversity index.
        """
        if not isinstance(counts, pd.DataFrame):
            raise TypeError("The input must be a pandas DataFrame.")
        return sk.diversity.alpha_diversity("simpson", self.counts, ids = self.counts.columns)





class Beta(CommonDiveristy):

    def __init__(self,):

        pass