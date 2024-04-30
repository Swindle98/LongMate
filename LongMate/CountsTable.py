

class CountsTable:
    """
    A top level class encompassing the manipulation of count tables and analysis functions.
    """
        # Constructor

    def __init__(self, df, timepoints, groups):

        self.counts_type_check(df)
        self.counts = df
        self.import_timepoints(timepoints)
        self.import_groups(groups)



    # Attributes
    


    # Methods
    def import_groups(self, groups):
        """
        Import the groups for the analysis from a list or dictionary. The groups are added as a row on the dataframe and the dictionary is assigned to the groups attribute.
        """
        if not isinstance(groups, [list, dict]):
            raise TypeError("The groups must be supllioed as a list or dictionary.")
        
        if isinstance(groups, list):
            """
             If the groups are supplied as a list, then the groups are assigned to the samples in the order they are presented.
             a dictionary is then generated and assigned to the groups attribute.
            """
            self.counts['groups'] = groups
            self.groups = {i: groups[i] for i in range(0, len(groups))}

        if isinstance(groups, dict):
            """
            If the groups are supplied as a dictionary, then the groups are assigned to the samples based on the species.
            The dictionary is then assigned to the groups attribute.
            """
            self.groups = groups
            for key in groups.keys():
                self.counts.loc[self.counts['species'] == key, 'groups'] = groups[key]


    def import_timepoints(self, timepoints):
        """
        Import the timepoints for the analysis from a list or dictionary. The timepoints are added as a row on the dataframe and the dictionary is assigned to the timepoints attribute.
        """
        if not isinstance(timepoints, [list, dict]):
            raise TypeError("The timepoints must be supplied as a list or dictionary.")
        
        if isinstance(timepoints, list):
            """
            If the timepoints are supplied as a list, then the timepoints are assigned to the samples in the order they are presented.
            a dictionary is then generated and assigned to the timepoints attribute.
            """
            self.counts['timepoints'] = timepoints
            self.timepoints = {i: timepoints[i] for i in range(0, len(timepoints))}

        if isinstance(timepoints, dict):
            """
            If the timepoints are supplied as a dictionary, then the timepoints are assigned to the samples based on the species.
            The dictionary is then assigned to the timepoints attribute.
            """
            self.timepoints = timepoints
            for key in timepoints.keys():
                self.counts.loc[self.counts['species'] == key, 'timepoints'] = timepoints[key]
            

    def counts_type_check(self):
        """
        Check the type of the counts table.
        """
        if not isinstance(self.counts, pd.DataFrame):
            raise TypeError("The counts table must be a pandas DataFrame.")
        


