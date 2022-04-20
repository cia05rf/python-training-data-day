"""Tutorial on manipulating data
For full reference of manipulations visit:
- https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
- https://pandas.pydata.org/docs/reference/api/pandas.Series.html
"""
# Import data


# Work out total_paid
# Investigate columns to work out if item_total is for
# 1 item or the quantity ordered
# Find the most common

# Grab the most common item

# See if the item_total varies


# Now lets calc the total_paid
# The fastest way to do this is vectorised


# What if we want to mark the capital

# We could use a conditional statement

# Now let's apply a tax

# Is the same as

# Let's fill the nan


# What if we wanted to do all this in one function for each row
# (just humour me, this is a slower way of doing things)

# Show how iterrows works

# Show df and look for added columns


# Introducing tqdm


# How about we apply a different tax for each city
# Example using iterrows

# Example using loc

# Example using merge
