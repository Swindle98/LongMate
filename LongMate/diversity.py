import pandas as pd
import skbio as sk
import matplotlib.pyplot as plt


class DiversityCore():
    """
    A parent class that contains the core attributes and methods for the Alpha and Beta diversity classes.
    """
    def __init__(self, counts, time_units = "time"):
        self.counts = counts
        self.time_units = time_units


class Alpha(DiversityCore):
    def __init__(self, counts, time_units):
        super().__init__(counts, time_units)
        
    def simpson(self):
        """
        Calculate the Simpson diversity index.

        returns a pandas series for simpson diversity of each sample.
        """
        counts = self.counts.T
        if not isinstance(counts, pd.DataFrame):
            raise TypeError("The input must be a pandas DataFrame.")
        return sk.diversity.alpha_diversity("simpson", counts, ids=counts.index)
    
    def shannon(self):
        """
        Calculate the Shannon diversity index.

        returns a pandas series for shannon diversity of each sample.
        """
        counts = self.counts
        if not isinstance(counts, pd.DataFrame):
            raise TypeError("The input must be a pandas DataFrame.")
        return sk.diversity.alpha_diversity("shannon", counts, ids=counts.columns)

    def plot(self, method, by_group = False):
        """
        Plot the diversity over time.
        method: str, the diversity index to plot.
        
        """
        if not isinstance(method, str):
            raise TypeError("The method must be a string.")
        
        diversity = self.get_diversity(method)
        
        if by_group == False:
            """
            plots all alpha values together on the same plot.
            """
            plt.plot(diversity.index.get_level_values(0), diversity)
            plt.xlabel(f"Time ({self.time_units})")

        if by_group == True:
            """
            plots each group seperately on the same plot.
            """
            group_labels = diversity.index.get_level_values(1).unique()
            for group in group_labels:
                plt.plot(diversity.loc[:, group].index.get_level_values(0), diversity.loc[:, group], label = group)
        


        plt.ylabel("Diversity")
        plt.title(f"{method.capitalize()} Diversity Over Time")
        return plt
        
    def get_diversity(self, method):
        """
        Get the diversity index.
        method: str, the diversity index to calculate.
        """
        if not isinstance(method, str):
            raise TypeError("The method must be a string.")
        
        if method == "simpson":
            return self.simpson()

        elif method == "shannon":
            return self.shannon()
        else:
            raise ValueError("Method isn't recognised.")


class Beta(DiversityCore):

    def __init__(self, counts):
        super().__init__(counts)

        pass