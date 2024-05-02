import pandas as pd
from . import diversity

class CountsTable:
    """
    A top level class encompassing the manipulation of count tables and analysis functions.
    """
        # Constructor

    def __init__(self, df, timepoints, groups, time_units = "day"):
        """
        Constructor for the CountsTable class.
        df: pandas DataFrame
        timepoints: list
        groups: list
        time_type: str , This is mainly for labeling axis on plots.
        """
        self.counts_type_check(df)
        self.counts = self.add_multiindex(df, groups, timepoints)
        self.time_units = time_units
        self.time = self.get_index_dict(self.counts, 'time')
        self.groups = self.get_index_dict(self.counts, 'group')

        self.alpha = diversity.Alpha(self.counts, self.time_units)
        

    
    # Methods

    def dict_to_list(self, dictionary, index):
        """
        takes a (potentially unordered dictionary), and converts it to 
        a list that matches the order of the index provided.
        dictionary: dictionary
        index: list
        """
        if not isinstance(dictionary, dict):
            raise TypeError("The input must be a dictionary.")
        if not isinstance(index, list):
            raise TypeError("The index must be a list.")
        
        dict_list = []
        for key in index:
            dict_list.append(dictionary[key])
        return dict_list
    
    def make_multiindex(self, df, groups, time):
        """
        Create a multiindex from the groups and timepoints.
        df: pandas DataFrame (counts table)
        groups: list or dictionary
        time: list or dictionary
        """

        #Check the types of the groups and timepoints
        if not isinstance(groups, (list, dict)):
            raise TypeError("The groups must be supplied as a list or dictionary.")
        if not isinstance(time, (list, dict)):
            raise TypeError("The timepoints must be supplied as a list or dictionary.")
        if not isinstance(df, pd.DataFrame):
            raise TypeError("The counts table must be a pandas DataFrame.")
        
        #Get the index as a lit, Check the lengths of the groups, timepoints, and index to ensure they match
        index = df.index.tolist()
        if len(index) != len(groups) or len(index) != len(time):
            raise ValueError("The length of the groups, timepoints, and index must be the same.")

        #If the groups and timepoints are supplied as dictionaries, convert them to lists
        if isinstance(groups, dict):
            groups = self.dict_to_list(groups, index)
        if isinstance(time, dict):
            time = self.dict_to_list(time, index)
                
        #Create a list of tuples with the timepoints and groups
        tuples = list(zip(time, groups, index))
        multi_index = pd.MultiIndex.from_tuples(tuples, names=['time', 'group', 'samples'])
        return multi_index

    def add_multiindex(self, df, groups, time):
        """
        Add a multiindex to the counts table.
        df: pandas DataFrame (counts table)
        groups: list or dictionary
        time: list or dictionary
        """
        Transposed_df = df.T
        multi_index = self.make_multiindex(Transposed_df, groups, time)
        Transposed_df.index = multi_index
        print(Transposed_df)
        return Transposed_df.T #Return the dataframe in the same layout as recieved.
      
    def counts_type_check(self, df):
        """
        Check the type of the counts table.
        """
        if not isinstance(df, pd.DataFrame):
            raise TypeError("The counts table must be a pandas DataFrame.")
        
    def get_index_dict(self, df, column):
        """
        Get a dictionary of {sample: time} from the counts table.
        """
        df = df.T.index.to_frame().set_index('samples')
        return df[column].to_dict()
    




