import LongMate
import pandas as pd


# Generating a test table:

features = ['species1', 'species2', 'species3', 'species4', 'species5']
sample1 = [5,4,5,3,1]
sample2 = [4,7,3,2,1]
sample3 = [10,3,4,2,1]
sample4 = [4,5,6,2,1]
sample5 = [3,4,5,2,0]
columns = [ f"Sample{i}" for i in range(1,6)]

df = pd.DataFrame([sample1, sample2, sample3, sample4, sample5], index = features, columns = columns)

print(f"Original table:\n{df}\n")


# Creating a LongMate object:
timepoints = [1,1,2,2,3]
groups = ['A','B','A','B','A']

test = LongMate.CountsTable(df, timepoints, groups)


print(f"Table with timepoints and groups:\n{test.counts}\n")
print(f"Timepoints: {test.time}\n")
print(f"Groups: {test.groups}\n")

print('simpson diversity: \n', test.alpha.simpson(), "\n")

plt = test.alpha.plot("simpson", by_group = True)

#plt.savefig("test_figs/simpson_plot.png")

print( test.min_max_within_feature() )