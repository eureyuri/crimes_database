import pandas as pd
import random
import string


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


df = pd.read_csv('../data/SHR76_17.csv', sep=',', nrows=10000, skiprows=range(1, 750000))

df = df[['CNTYFIPS', 'ID']]
states = []
cities = []
address1s = []
zips = []

for index, row in df.iterrows():
    address = row['CNTYFIPS']
    address = address.split(',')
    city = address[0]

    try:
        state = address[1][-2:]
    except:
        state = '99'

    states.append(state)
    cities.append(city)
    address1s.append(get_random_alphanumeric_string(10))
    zips.append(random.randint(10000, 99999))

df['state'] = states
df['city'] = city
df['address1'] = address1s
df['zip'] = zips
df = df.drop(['CNTYFIPS'], axis=1)
df = df.rename({'ID': 'case_id'}, axis=1)

df.drop_duplicates().drop_duplicates(subset='case_id', keep='first').to_csv('../data/happened_at.csv', sep=',', index=False)