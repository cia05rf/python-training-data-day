# Import the pandas library
import pandas as pd
import numpy as np

# What is a pandas series?
# A pandas Series is a one-dimensional labelled data structure which can hold
# data such as strings, integers and even other Python objects. It is built
# on top of numpy array and is the primary data structure to hold
# one-dimensional data in pandas.

# Create series from a list.

data_list = ['Jeff Bezos', 'Elon Musk',
             'Bernard Arnault', 'Bill Gates', 'Warren Bufett']

series = pd.Series(data=data_list)
print(f'Whole series :\n{series}')
print()
print(f'Series element 2 :\n{series[2]}')

# Can also create series from dictionary, tuple, numpy array etc.

# Create the indices
indices = ['Amazon', 'Tesla', 'Louis Vuitton',
           'Microsoft', 'Berkshire Hathaway']

# Pass the indexes to the series constructor
series = pd.Series(data=data_list, index=indices)

print(f'Whole series :\n{series}')
print()
print(f'Series element 2 :\n{series[2]}')
print()
print(f"Series referenced by index :\n{series['Amazon']}")

# Can iterate over a series
print('Iterating over series')
for element in series:
    print(element)

# Can convert to other data types
print(list(series))
print(np.array(series))
print(series.to_numpy())

# Can access the index directly
print(series.index)

# Can do lots of other operations. Full list can be found in the help here :
# https://pandas.pydata.org/docs/reference/api/pandas.Series.html
# e.g.

a = pd.Series([1, 2, 3, 4])
b = pd.Series([1, 2, 3, 4])

print(a.pow(b))

# What is a pandas dataframe?
# DataFrame is a 2-dimensional labeled data structure with columns of
# potentially different types. You can think of it like a spreadsheet or SQL
# table, or a dict of Series objects. It is generally the most commonly used
# pandas object. Like Series, DataFrame accepts many different kinds of input:
# * Dict of 1D ndarrays, lists, dicts, or Series
# * 2-D numpy.ndarray
# * Structured or record ndarray
# * A Series
# * Another DataFrame

# From dict of series

d = {
    "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "e"]),
    "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
}

df = pd.DataFrame(d)
print(df)

# From list of dictionaries

li = [{'points': 50, 'time': '5:00', 'year': 2010},
      {'points': 25, 'time': '6:00', 'month': 'february'},
      {'points': 90, 'time': '9:00', 'month': 'january'},
      {'points_h1': 20, 'month': 'june'}]

df = pd.DataFrame(li)
print(df)

# Access the index
print(df.index)
# Access the columns
print(df.columns)
# Acces the datatypes
print(df.dtypes)

# Shape of dataframe
print(df.shape)

# Select a single column as a series
series = df['points']
print(series)

# Accessing the dataframe
df.index = [1, 7, 8, 19]
print(df)
# Select everything
print(df.loc[:, :])

# Select certain columns
print(df.loc[:, ['time', 'month']])

# Select by index
print(df.loc[[1, 8], :])
# N.B This is not selecting by position - the following will return an error
print(df.loc[[0, 1], :])

# Select by boolean series
print(df['points'] >= 50)
print(df.loc[df['points'] >= 50, :])

# We can also shortcut this, if just filtering on rows
print(df[df['points'] >= 50])

# If you want to select by position use iloc
print(df.iloc[[0, 1], :])

# You can use loc and iloc to set values

df.loc[df['points'] >= 50, 'points 50 or over'] = 'yes'
print(df)

# Time as index

days = pd.date_range("01/01/2022", periods=365, freq="D")
mylist = [x for x in range(365)]
df = pd.DataFrame(mylist, columns=['number'])
df.index = days
print(df)

print(df.loc[df.index < '2022-01-05 08:00:00'])

# For datetime index we can use resample as a grouping
print(df.resample("M").max())

# Keep a mind on referencing

print(df)

df2 = df
df2['new column'] = 1
print(df)

# Create a copy if you want to modify without modifying original

df3 = df.copy()
df3['new column2'] = 1
print(df)
print(df3)

# Read csv
df = pd.read_csv('./Data/2022-02-nottinghamshire-street.csv')
print(df)

help(pd.read_csv)

# Write excel
df.to_excel('./Data/nottinghamshire_out.xlsx', index=False, startrow=2,
            startcol=2)
