"""Tutorial on manipulating data"""
from time import sleep
import pandas as pd
# from tqdm import tqdm

df = pd.read_csv("../Data/orders_data_cl.csv")

# Work out total_paid
# Investigate columns to work out if item_total is for
# 1 item or the quantity ordered
# Find the most common
display(df.sku.value_counts())
# Grab the most common item
df_slice = df[df.sku == "SKU:  DN-0WDX-VYOT"]
# See if the item_total varies
display(df_slice.item_total.describe())

# Now lets calc the total_paid
# The fastest way to do this is vectorised
df["total_paid"] = df.item_total + df.shipping_fee
display(df[["item_total", "shipping_fee", "total_paid"]])

# What if we want to mark the capital
display(df.ship_city.describe())
# We could use a conditional statement
df["capital_shipping"] = df.ship_city == "MUMBAI,"
# Now let's apply a tax
df.loc[df.capital_shipping, "capital_tax"] = 0.1
# Is the same as
df.loc[df.ship_city == "MUMBAI,", "capital_tax"] = 0.1
# Let's fill the nan
df["capital_tax"] = df.capital_tax.fillna(0)
display(df)

# What if we wanted to do all this in one function for each row
# (just humour me, this is a slower way of doing things)
df = pd.read_csv("../Data/orders_data_cl.csv")
# Show how iterrows works
for i, r in df.iterrows():
    display(i, r)
    break
for i, r in df.iterrows():
    r["total_paid"] = r.item_total + r.shipping_fee
    if r.ship_city == "MUMBAI,":
        r["capital_tax"] = 0.1
    else:
        r["capital_tax"] = 0
    display(r)
    # df.ioc[i] = r
    # break
# Show df and look for added columns
display(df)

# Introducing tqdm
# for i,r in tqdm(df.iterrows(), total=df.shape, desc="I'm sleepy"):
#     sleep(1)
#     pass

# How about we apply a different tax for each city
# Example using iterrows
df = pd.read_csv("../Data/orders_data_cl.csv")
for i, r in df.iterrows():
    if r.ship_city == "MUMBAI,":
        r["capital_tax"] = 0.1
    elif r.ship_city == "BENGALURU,":
        r["capital_tax"] = 0.2
    elif r.ship_city == "KOLKATA,":
        r["capital_tax"] = 0.3
    elif r.ship_city == "HYDERABAD,":
        r["capital_tax"] = 0.4
    elif r.ship_city == "CHENNAI,":
        r["capital_tax"] = 0.5
    display(r)
    # df.ioc[i] = r
    # break
# Example using loc
df = pd.read_csv("../Data/orders_data_cl.csv")
df.loc[df.ship_city == "MUMBAI,", "capital_tax"] = 0.1
df.loc[df.ship_city == "BENGALURU,", "capital_tax"] = 0.2
df.loc[df.ship_city == "KOLKATA,", "capital_tax"] = 0.3
df.loc[df.ship_city == "HYDERABAD,", "capital_tax"] = 0.4
df.loc[df.ship_city == "CHENNAI,", "capital_tax"] = 0.5
# Example using merge
df = pd.read_csv("../Data/orders_data_cl.csv")
tax_rates_df = pd.read_csv("../Data/tax_rates.csv")
display(tax_rates_df)
df = pd.merge(
    df,
    tax_rates_df,
    on="ship_city",
    how="inner"
)
display(df)
