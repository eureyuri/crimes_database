import pandas as pd

df = pd.read_csv('../data/SHR76_17.csv', sep=',', nrows=10000, skiprows=range(1, 750000))

df = df[['ID', 'VicSex', 'VicAge', 'VicRace', 'Relationship']]
df = df.rename({'ID': 'case_id', 'VicSex': 'sex', 'VicAge': 'age', 'VicRace': 'race', 'Relationship': 'relation'}, axis=1)
df['homicide_victim_id'] = 1;

df.drop_duplicates().drop_duplicates(subset='case_id', keep='first').to_csv('../data/kill_homicides.csv', sep=',', index=False)