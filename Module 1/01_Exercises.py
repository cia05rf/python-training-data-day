import pandas as pd

# 1. Read in the data from Data/iris.csv

# 2. How many columns are there?

# 3. How many rows are there?

# 4. What are the names of the columns?

# 5. Select records where the petal length is > 1.5, select only petal.length
#    and variety

# 6. Create a new variable "over 2 pl" which shows whether the petal length is
#    over 2

# 7. Output the results to excel in the Data directory called 'filtered.xlsx',
#    without an index

























# Solution

# 1. Read in the data from Data/iris.csv

iris = pd.read_csv('./Data/iris.csv')

# 2. How many columns are there?

print(iris.shape[1])

# 3. How many rows are there?

print(iris.shape[0])

# 4. What are the names of the columns?
print(iris.columns)

# 5. Select records where the petal length is > 1.5, select only petal.length
#    and variety

filtered = iris.loc[iris['petal.length'] > 1.5, ['petal.length', 'variety']]

# 6. Create a new variable "over 2 pl" which shows whether the petal length is
#    over 2

filtered.loc[filtered['petal.length'] > 2, 'over 2 pl'] = True
filtered['over 2 pl'] = (filtered['petal.length'] > 2)

# 7. Output the results to excel in the Data directory called 'filtered.xlsx',
#    without an index
filtered.to_excel('./Data/filtered.xlsx', index=False)
