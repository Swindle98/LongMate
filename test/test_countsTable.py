import pandas as pd
from .countsTable import CountsTable

def test_counts_table_init():
    # Test case 1: Valid inputs
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    timepoints = ['t1', 't2', 't3']
    groups = ['group1', 'group2']
    time_units = "day"
    counts_table = CountsTable(df, timepoints, groups, time_units)
    assert counts_table.counts.equals(df)
    assert counts_table.original_counts.equals(df)
    assert counts_table.time_units == "day"
    assert counts_table.time == {0: 't1', 1: 't2', 2: 't3'}
    assert counts_table.groups == {0: 'group1', 1: 'group2'}
    assert isinstance(counts_table.alpha, diversity.Alpha)

    # Test case 2: Invalid inputs
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    timepoints = ['t1', 't2']
    groups = ['group1', 'group2', 'group3']
    time_units = "hour"
    try:
        counts_table = CountsTable(df, timepoints, groups, time_units)
        assert False  # The above line should raise a ValueError
    except ValueError:
        assert True

    # Test case 3: Empty DataFrame
    df = pd.DataFrame()
    timepoints = ['t1', 't2', 't3']
    groups = ['group1', 'group2']
    time_units = "day"
    counts_table = CountsTable(df, timepoints, groups, time_units)
    assert counts_table.counts.empty
    assert counts_table.original_counts.empty
    assert counts_table.time_units == "day"
    assert counts_table.time == {}
    assert counts_table.groups == {}
    assert isinstance(counts_table.alpha, diversity.Alpha)