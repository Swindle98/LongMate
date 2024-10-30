# (The eventual home of) LongMate

*(Almost) Everything you need for processing longitudinal metagenomic count data in one place!*

This python package exists because many tools for analysis of counts tables focus on the comparisons of an A vs B group. My PhD project involved the investigation of 3 different groups, identifying differnces and trends across the groups. This package aims to combine many of the script in one simple API, to lower the barrier to entry for this kind of study for others. A major aim for this project is clear documentation that explains why (and a little bit of how) certain methods are implemented. If you find that any of the documentation for this package needs more explanation, please submit it as an issue so I can clarify futher for other potential users.

Aims:

- PC/laptop compatible
- Deal with inconsistent time points.

## Installation

LongMate can be installed using PIP (WIP)

### TheSequencer

Due to not having a working version of the Sequencer available from PyPI The sequencer needs to be installed directly from gihub.

With pip:

``` bash
pip install thesequencer@git+https://github.com/dalya/Sequencer
```

With pipenv:

``` bash
pipenv install git+https://github.com/dalya/Sequencer#egg=theSequencer
```

## Paradigms/Background info

### Whats a Metagenomic count table and what formats does longMate take?

This package is designed to help analyse metagenomic (mixed species) sequencing data from 1 or more groups of species where repeated samples are taken over a sereis of time points (longitudinal). One of the first steps in analysing the raw reads, can be to align these reads to known reads of interest, and count how many matches are found.

This could identify:

- Species (taxonomic profiler , such as nf_core/taxprofiler)
- Resitance genes (such as AMR++)
- Virulence genes

The end product of this is a very lage table with a list of features and how many times each feature was counted in each sample. LongMate assumes that the profiling has already been done and assist with analysising these count tables, ideniftying trends and producing figures.

LongMate is designed to be profiler agnositic, taking any longitudinal count data with features representing columns, and samples represented by columns. Each sample name must be unique. All the counts must be integers.

e.g for a taxonomic profiler it could look like:

|Feature   | Sample1 | Sample2 | Sample3 | Sample4 | ... |
|----------|---------|---------|---------|---------|-----|
|Species 1 | 10      | 12      | 15      | 20      | ... |
|Speceis 2 | 5       | 0       | 7       | 0       | ... |
|...       | ...     | ...     | ...     | ...     | ... |

LongMate exclusivily takes this in the form of a Pandas dataframe.

### Multiple groups of samples

If you study involves following multiple groups through the longitudinal study and you want to make use of LongMates tools for identifying differences between these groups and the overall trends of the study then you can supply the groups in the form of a dictionary, where the key is the corresponding sample (as labeled on the columm), and the value is the group the sample belongs to (int or str).

e.g. `{'Sample1': 1, 'Sample2' : 2, 'Sample3': 1, 'Sample4': 2, ..}`

Would signify that samples 1 and 3 belong to one a group labelled 1 and samples 2 and 3 belong to a group labelled 2.

TODO: Alternatively this information can be provided as a list where the index of the list matches the index of the columns of the table 

e.g. the above dictionary could be supplied as a list like this:

`[1, 2, 1, 2, ... ]`

### Providing time values

As longitudinal studies measure the changes of things over time, providing the time point is a pretty essential step. Time values are provided in a similar way to sample groups with a dictionary or list. 

For dictionary:
key = Sample (str)
Value = Timevalue (int or float from T=0).

e.g. in a study where each group was sampled every 5 days:
 `{'Sample1': 0, 'Sample2' : 5, 'Sample3': 0, 'Sample4': 5, ...}`

For a list:
The index represents the column index and the value (int or float) represents the time since t=0. e.g. The dictionary above would look like this:
`[0, 5, 0, 5, ...]`

## Literature using LongMate