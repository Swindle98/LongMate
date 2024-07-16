import pandas as pd
from . import diversity
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from feature_engine.selection import DropCorrelatedFeatures, DropDuplicateFeatures
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import copy
import sequencer
import networkx as nx

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
        self.counts = self.add_multi_index(df, groups, timepoints)
        self.original_counts = self.counts
        self.time_units = time_units
        self.time = self.get_index_dict(self.counts, 'time')
        self.groups = self.get_index_dict(self.counts, 'group')

        self.dataframes = {
        "original": self.original_counts,
        "greater_than_0": self.get_appearance_subset(0),
        "greater_than_10": self.get_appearance_subset(10),
        "greater_than_20": self.get_appearance_subset(20),
        "greater_than_30": self.get_appearance_subset(30),
        "greater_than_40": self.get_appearance_subset(40),
        "greater_than_50": self.get_appearance_subset(50),
        "greater_than_60": self.get_appearance_subset(60),
        "greater_than_70": self.get_appearance_subset(70),
        "greater_than_90": self.get_appearance_subset(90),
        "in_all_timepoints": self.get_appearance_subset(100),
        "average_of_timepoints": self.get_average_of_timepoints()
        }
        self.alpha = diversity.Alpha(self.counts, self.time_units)
        

    
    # Methods

    def add_dataframe(self, df, name):
        """
        Add a dataframe to the object.
        df: pandas DataFrame or function that returns a DataFrame.
        name: str, the name of the dataframe.
        """
        self.counts_type_check(df)
        self.dataframes[name] = df


    def deepcopy_with_update_counts(self, new_counts):
        """
        Create a copy of the object and update the counts attribute (this is used at the end of each method to update the 
        counts attribute without altering the original object).
        """
        new = copy.deepcopy(self)
        new.counts = new_counts
        new.alpha = diversity.Alpha(new.counts, new.time_units)
        return new

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
    
    def make_multi_index(self, df, groups, time):
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

    def add_multi_index(self, df, groups, time):
        """
        Add a multiindex to the counts table.
        df: pandas DataFrame (counts table)
        groups: list or dictionary
        time: list or dictionary
        """
       
        Transposed_df = df.T
        multi_index = self.make_multi_index(Transposed_df, groups, time)
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

    

    def get_appearance_subset(self, group):
        """
        Creates subsets of the counts table based on the number of sampels that a feature appears in.
        !this will assume that 0 values aren't present in your data (could just be too low for the detection limit)
        group: int, the % of samples a feature must appear in to be included.
        """
        appearances = self.counts.gt(0).sum(axis=1)
        new_df = self.counts.loc[appearances >= group]
        return new_df
    
    def get_average_of_timepoints(self):
        """
        provides the average counts for each feature per timepoint.
        """
        return self.counts.groupby(level=0, axis=1).mean()

    def set_counts(self, df="original"):
        f"""
        Set the counts table attribute to another dataframe present in the object (${self.dataframes.keys()}).
        If no argument is provided, the original counts table is used.
        df: str or None, the counts table.
        """
        dataframes = self.dataframes

        if isinstance(df, str):
            if df not in dataframes.keys():
                raise ValueError(f"""The dataframe must be one of the following:${dataframes.keys()}""")
            else :
                self.counts = dataframes[df]
        else:
            raise TypeError("The dataframe must be a string or empty.")
    

    # Common pre-processing steps (may be moved to a separate class):

    def time_cut_off(self, time):
        """
        Cut off the counts table at a certain timepoint.
        time: int, the timepoint to cut off at.
        """
        new_df = self.counts.loc[:, self.counts.columns.get_level_values(0) <= time]
        return self.deepcopy_with_update_counts(new_df) 

    def min_max_within_feature(self):
        """
        Normalise the counts table by the minimum and maximum values within each feature.
        """
        def normalize(row):
            return (row - row.min()) / (row.max() - row.min())

        
        df_normalized = self.counts.apply(normalize, axis=1)

        return self.deepcopy_with_update_counts(df_normalized) 

    def regression(self, degrees = 2):
        """
        Perform a linear regression each feature of the counts table.
        degrees: int, the degree of the polynomial.
        """
        regressed_features = []
        for i in self.counts.iterrows():
            name = i[0]
            x = i[1].index.get_level_values(0)
            y = i[1].to_numpy()
            x = x.values.reshape(-1,1)
            '''print(f"""name: {name}
X: {x}
Y: {y}
==================
            """)'''
            poly = PolynomialFeatures(degrees)
            x_poly = poly.fit_transform(x)
            poly.fit(x_poly, y)
            lin = LinearRegression()
            lin.fit(x_poly, y)
            predicted_time = np.array(range(x.min(), x.max()+1)).reshape(-1,1)
            #print('predicted time points:', predicted_time)
            y_pred = lin.predict(poly.fit_transform(predicted_time))
            series = pd.Series(y_pred, index = predicted_time.flatten(), name=name)
            series.index.name = 'time'
            #print(series)
            regressed_features.append(series)
    

        rf_df = pd.DataFrame(regressed_features)
        print(rf_df)
        return self.deepcopy_with_update_counts(rf_df)
        
        
        
    def drop_correlated_features(self, threshold):
        """
        Drop features that are highly correlated.
        threshold: float, the threshold for dropping features.
        """
        drop_correlated = DropCorrelatedFeatures(method='pearson', threshold = threshold)
        print(self.counts.T)
        dropped = drop_correlated.fit_transform(self.counts.T, self.counts.T)
        copied_obj = self.deepcopy_with_update_counts(dropped.T)
        copied_obj.correlated_feature_dict_ = drop_correlated.correlated_feature_dict_
        copied_obj.correlated_feature_sets_ = drop_correlated.correlated_feature_sets_

        return copied_obj
    
    def drop_duplicated_features(self):
        """
        Drop duplicated features.
        """
        drop_duplicated = DropDuplicateFeatures()
        dropped = drop_duplicated.fit_transform(self.counts.T, self.counts.T)
        copied_obj = self.deepcopy_with_update_counts(dropped.T)
        copied_obj.duplicated_feature_sets_ = drop_duplicated.duplicated_feature_sets_
        return copied_obj




    # Clustering methods (may be moved to a separate class):

    def the_sequencer(self, output_dir, N_best_estimators=3):
        """
        Perform the Sequencer algorithm.
        """
       

        new_index = np.arange(len(self.counts.columns))
        grid_series = pd.Series(self.counts.columns.to_numpy(), index=new_index)
        grid = grid_series.index.to_numpy()

        objects_list = self.counts.to_numpy()
        estimator_list = ['EMD', 'energy', 'L2']
        seq = sequencer.Sequencer(grid, objects_list, estimator_list)

        # execute the Sequencer
        output_directory_path = "sequencer_output_directory"
        final_elongation, final_sequence = seq.execute(output_dir,to_average_N_best_estimators=True, number_of_best_estimators=N_best_estimators)
        print(grid_series)
        print(final_sequence)

        index = self.counts.index
        new_df = self.counts.loc[index[final_sequence]]
        print(new_df)

        new_obj = self.deepcopy_with_update_counts(new_df)
        new_obj.seq_obj = seq

        return new_obj
    
    def k_means_cluster(self, n_clusters):
        """
        Perform k-means clustering.
        n_clusters: int, the number of clusters.
        """

        pass
        

    def PCA(self):
        """
        Perform PCA.
        """
        pass


