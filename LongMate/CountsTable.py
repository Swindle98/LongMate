

class CountsTable:
    """
    A top level class encompassing the manipulation of count tables and analysis functions.
    """
    # Attributes



    # Methods

    def counts_type_check(self):
        """
        Check the type of the counts table.
        """
        if not isinstance(self.counts, pd.DataFrame):
            raise TypeError("The counts table must be a pandas DataFrame.")
        

    # Constructor

    def __init__(self, df):

        counts_type_check(df)
        self.counts = df