import pandas as pd
import numpy as np
import datetime

df = pd.read_csv('data/SHR76_17.csv', sep=',', nrows=10000, skiprows=range(1, 750000))
# df = pd.read_csv('SHR76_17.csv', sep=',', nrows=10)

# Crimes
df = df[['ID', 'Year', 'Month']]
df = df.rename({'ID': 'case_id', 'Year': 'year', 'Month': 'month'}, axis=1)
for index, row in df.iterrows():
    month = row['month']
    month_num = datetime.datetime.strptime(month, '%B').month
    df.loc[index, 'month'] = month_num

df.drop_duplicates().to_csv('data/crimes.csv', sep=',', index=False)