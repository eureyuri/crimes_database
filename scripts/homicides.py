import pandas as pd

df = pd.read_csv('../data/SHR76_17.csv', sep=',', nrows=10000, skiprows=range(1, 750000))

df = df[['ID', 'Homicide', 'Situation', 'OffSex', 'OffAge', 'OffRace']]
df = df.rename({'ID': 'case_id', 'Homicide': 'action_type', 'Situation': 'situation',
                'OffSex': 'sex', 'OffAge': 'age', 'OffRace': 'race'}, axis=1)

df.drop_duplicates().drop_duplicates(subset='case_id', keep='first').to_csv('../data/homicides.csv', sep=',', index=False)