import pandas as pd
import numpy as np
import timeit
import matplotlib
import plotly.io as pio
import seaborn as sns
import plotly.express as px
pio.renderers.default = 'browser'

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# In Module 3 we will be focussing on data manipulation within pandas
# This will cover:
#   * Aggregation
#   * Pivoting data
#   * Vectorisation
#   * Formatting data
#   * Plotting (basic)

df = pd.read_csv('./Data/iris.csv')
df['random'] = np.random.choice(['A', 'B', 'C'], len(df))

# Aggregation
# One of the most useful things to do with data is to aggregate it. The most
# common way to do this in pandas is with the .groupby() method.

# Lets sum up all columns by the variety

grouped = df.groupby('variety').sum()
print(grouped)

# Can also group by multiple columns

grouped2 = df.groupby(['variety', 'random']).sum()
print(grouped2)

# N.B. The grouping is put as the index by default
print(grouped2.index)
print(grouped2.columns)

# We can reset the index by using reset_index method

gp2_reindex = grouped2.reset_index()
print(gp2_reindex)
print(gp2_reindex.index)
print(gp2_reindex.columns)

# If we dont want that to happen in the first place, we can specify in our
# groupby statement

grouped2 = df.groupby(['variety', 'random'], as_index=False).sum()
print(grouped2)
print(grouped2.index)
print(grouped2.columns)

# Can iterate through groups

for name, group in df.groupby(['variety', 'random']):
    print(name)
    print(group)

# We can do many other built in aggregations

print(df.groupby(['variety'], as_index=False).mean())
print(df.groupby(['variety'], as_index=False).std())
print(df.groupby(['variety'], as_index=False).median())
dir(df.groupby(['variety'], as_index=False))

# Can also do named aggregations, and different aggregations for each column
agg = df.groupby('variety').agg(
    min_sl=pd.NamedAgg(column="sepal.length", aggfunc="min"),
    max_sw=pd.NamedAgg(column="sepal.width", aggfunc="max"),
    average_pl=pd.NamedAgg(column="petal.length",
                           aggfunc=lambda x: np.mean(x)),
    average_pl_plus2=pd.NamedAgg(column="petal.length",
                                 aggfunc=lambda x: np.mean(x+2))
)
print(agg)

# Can do other methods with a DataFrameGroupBy object
sort_df = df.sort_values(['variety', 'sepal.length']).reset_index(drop=True)
shifted = df.sort_values('sepal.length').groupby('variety').shift(1)
print(sort_df.head(10))
print(shifted.head(10))
print(sort_df.join(shifted.rename(columns=lambda x: x+"_lag")))

# Can do lots of other things with grouped data - look in help for more info

################
# Pivoting Data
################

# In addition to grouping data we may wish to convert from wide to long format
# or vice versa

# For example, we may wish to group by variety and the random column, but have
# the random column across the top. We can do this with pivot_table

pivoted = df.pivot_table(values='sepal.length', index='variety',
                         columns='random', aggfunc='mean')
print(pivoted)
print(pivoted.columns)
print(pivoted.index)

# N.B. this will put create indexes for rows / columns
# Can reset index and rename axis

pivot_unindex = pivoted.reset_index().rename_axis(None, axis=1)
print(pivot_unindex)
print(pivot_unindex.columns)
print(pivot_unindex.index)

# We could do the same as above by grouping and then transposing the data

grouped = (df
           .groupby(['variety', 'random'], as_index=False)['sepal.length']
           .mean()
           )
print(grouped)

grouped_pivoted = grouped.pivot(index='variety', columns='random',
                                values='sepal.length')
print(grouped_pivoted)

# Can also unpivot the data

pivot_unpivoted = pd.melt(pivot_unindex, id_vars='variety',
                          value_vars=['A', 'B', 'C'], var_name='random',
                          value_name='sepal.length')
print(pivot_unpivoted.sort_values(['variety', 'random']))
print(grouped.sort_values(['variety', 'random']))

###############
# Vectorisation
###############

# In pandas, and python in general, there are multiple ways of doing things
# With pandas, you should use vectorised implementation where you can
# This is because vectorised implementations are often highly performant and
# the underlying code is written in C, and we should try to avoid iterating
# within python as its slower due to something technical (SIMD or something)

# The Zen of Pandas Optimization
# - Avoid loops, if you can
# - If you must loop, use apply, not iteration functions
# - If you must apply, use Cython to make it faster
# - Vectorization is usually better than scalar operations
# - Vector operations on NumPy arrays are more efficient than on native
#   Pandas series


def haversine(lat1, lon1, lat2, lon2):
    miles_constant = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    mi = miles_constant * c
    return mi


df = pd.read_csv('./Data/2022-02-nottinghamshire-street.csv')

# Using iterrows

%%timeit
haversine_series = []
for index, row in df.iterrows():
    haversine_series.append(haversine(40.671, -73.985,
                                      row['Latitude'], row['Longitude']))
df['distance'] = haversine_series

# Using apply

%%timeit
df['distance'] = df.apply(lambda row:
                          haversine(40.671, -73.985,
                                    row['Latitude'], row['Longitude']), axis=1)

# Vectorised
%%timeit
df['distance'] = haversine(40.671, -73.985, df['Latitude'], df['Longitude'])

# Vecotorised using numpy
%%timeit
df['distance'] = haversine(40.671, -73.985,
                           df['Latitude'].values, df['Longitude'].values)

###################
# Formatting data
###################

# Use astype method to change the type of a column

df['Latitude_str'] = df['Latitude'].astype(str)
df['Month_date'] = pd.to_datetime(df['Month'], format='%Y-%m')
df['Year'] = df['Month_date'].dt.year
print(df.iloc[0])
print(df.dtypes)

# Best thing to do is get the correct type on input. Whether its from SQL
# or specified in the read_csv etc.

###########
# Plotting
###########

# There are many variants of plotting in python. Here we only present some
# high level concepts / packages that are used

# matplotlib
# seaborn
# plotly

pd.options.plotting.backend = "matplotlib"
df.plot.scatter(x='Longitude', y='Latitude')

# Change backend to seaborn

sns.scatterplot(data=df, x='Longitude', y='Latitude')

# Change backend to plotly

pd.options.plotting.backend = "plotly"
fig = df.plot.scatter(x='Longitude', y='Latitude')
fig.show()

# Can do multi-faceted plots e.g.

sns.set_theme(style="ticks")

df = sns.load_dataset("penguins")
sns.pairplot(df, hue="species")

# Can do something similar in plotly

fig = px.scatter_matrix(df,
                        dimensions=['bill_length_mm', 'bill_depth_mm',
                                    'flipper_length_mm', 'body_mass_g'],
                        color="species")
fig.show()

# Notable other mentions:
# bokeh
# holoviz
# Folium (map)
# plotnine (Mace)