import LongMate
import pandas as pd

import warnings

warnings.filterwarnings("ignore")
# Generating a test table:

features = ['species1', 'species2', 'species3', 'species4', 'species5', 'speciesS']
sample1 = pd.Series([5,4,5,3,1,1], index = features, name = "Sample1")
sample2 = pd.Series([4,7,3,2,1,1], index = features, name = "Sample2")
sample3 = pd.Series([10,3,4,2,1,1], index = features, name = "Sample3")
sample4 = pd.Series([4,5,6,2,1,1], index = features, name = "Sample4")
sample5 = pd.Series([3,4,5,2,2,2], index = features, name = "Sample5")
columns = [ f"Sample{i}" for i in range(1,6)]

df = pd.DataFrame([sample1, sample2, sample3, sample4, sample5]).T

print(f"Original table:\n{df}\n")


# Creating a LongMate object:
timepoints = [1,1,2,2,3]
groups = ['A','B','A','B','A']

test = LongMate.CountsTable(df, timepoints, groups)


print(f"Table with timepoints and groups:\n{test.counts}\n")
print(f"Timepoints: {test.time}\n")
print(f"Groups: {test.groups}\n")

print('simpson diversity: \n', test.alpha.simpson(), "\n")

#plt = test.alpha.plot("simpson", by_group = True)

#plt.savefig("test_figs/simpson_plot.png")

normalised = test.min_max_within_feature()
print("----------------- \n REALLY OBV BIT OF TEXT \n -----------------")
print("normalised", '\n',  normalised.counts, '\n', normalised.original_counts)


#print(species_time_series)
regressed = test.regression()
print(f"regressed counts \n{regressed.counts}" )


print("regressed normalised counts: \n")
print(test.counts)
regressed_normalised = test.min_max_within_feature().regression()
print(regressed_normalised.counts)


feature_dropped = test.drop_features(0.9)
print(f"feature dropped counts \n{feature_dropped.counts}" )

print("corration sets: \n", feature_dropped.correlated_feature_dict_)

returned = test.the_sequencer(".")

print("The sequencer: \n", returned)