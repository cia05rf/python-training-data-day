import pandas as pd
import seaborn as sns

# Read in example dataset
df = sns.load_dataset('titanic')

# 1. Get the average (mean) survival rate by class

# 2. Get the minimum fare by class and sex

# 3. Get the median of the fare (median_fare), mean survival rate (mean_sr)
#    and a count of number of people in each grouping by class and sex.
#    Note: can use the aggregation method "size"

# 4. Get the mean fare by class and sex, but have class as a column

# 5. Plot fare against age in a scatter plot















































# Solution
# 1. Get the average survival rate by pclass

print(df.groupby('class')['survived'].mean())

# 2. Get the minimum fare by class and sex

print(df.groupby(['class', 'sex'])['fare'].min())

# 3. Get the median of the fare (median_fare), mean survival rate (mean_sr)
#    and a count of number of people in each grouping by class and sex.
#    Note: can use the aggregation method "size"

print(df
      .groupby(['class', 'sex'])
      .agg(median_fare=pd.NamedAgg(column='fare', aggfunc="median"),
           mean_sr=pd.NamedAgg(column='survived', aggfunc="mean"),
           count=pd.NamedAgg(column='survived', aggfunc="size"))
      )

# 4. Get the mean fare by class and sex, but have class as a column

print(df.pivot_table(values='fare', index='sex',
                     columns='class', aggfunc='mean'))


# 5. Plot fare against age in a scatter plot
import matplotlib

df.plot(kind='scatter', x='fare', y='age')