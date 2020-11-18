import pandas as pd

df = pd.read_csv('../data/happened_at.csv', sep=',')

df = df.drop(['case_id'], axis=1)

df.to_csv('../data/locations.csv', sep=',', index=False)