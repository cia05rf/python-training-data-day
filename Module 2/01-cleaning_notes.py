"""Thsi section of training will look at cleaning a dataset"""

from datetime import timedelta
import pandas as pd
import re

# Import data
df = pd.read_csv("../Data/orders_data.csv")
display(df)

# NULLS
# Dealing with nulls
# How does isnull work
display(df.isnull())
# Remove line with NaN
df_row_filter = df.isnull().sum(axis=1)
display(df_row_filter)
df = df[df_row_filter == 0]
display(df)
# Best is to deal with them col by col
df = pd.read_csv("../Data/orders_data.csv")
display(df.isnull().sum())
# Get rid of rows
df = df[~df.item_total.isnull()]
display(df.isnull().sum())
# Set null values
df["shipping_fee"] = df.shipping_fee.fillna(0)
display(df.isnull().sum())


# DATATYPES
# Check data types
display(df.dtypes)

# "object" is usually a string
# Try modifying date
# df["new_date"] = df.order_date + timedelta(days=1) # WILL ERROR

# Convert columns to correct data types - datetime example
df["order_date"] = df.order_date.astype("datetime64")
df["new_date"] = df.order_date + timedelta(days=1)
display(df[["order_date", "new_date"]])

# Convert columns to correct data types - numeric example
# df["item_total"] = df.item_total.astype(float) # WILL ERROR

df["item_total"] = [
    re.sub("[^\d\.]", "", str(v))
    for v in df.item_total
]
df["item_total"] = df.item_total.astype(float)
df["shipping_fee"] = [
    re.sub("[^\d\.]", "", str(v))
    for v in df.shipping_fee
]
df["shipping_fee"] = df.shipping_fee.astype(float)

# Export the cleaned version
df.to_csv("../Data/orders_data_cl.csv", index=False)