import pandas as pd
import googlemaps
import pickle

'''Initial cleaning of csv file. Concatenates what information we have into an incomplete address.
Then uses geopy to return a full address, latitude and longitude.
Should only be run on the first pass of this script
'''

df = pd.read_csv('files/GunViolence.csv')
gmaps = googlemaps.Client(key = 'AIzaSyC3qJs4tvgvBwtOkV6ouw4Gs8nlaJyv4ws')

df['Incomplete Address'] = df['Address'] + ', ' + df['City Or County'] + ', ' + df['State']
numrows = df.shape[0]
error_rows = []
for index, row in df.iterrows():
  if index % 10 == 0:
    print('Processing row ' + str(index) + ' of ' + str(numrows))
  geocode_result = gmaps.geocode(row['Incomplete Address'])
  try:
    df.loc[index, 'Full Address'] = geocode_result[0]['formatted_address']
    df.loc[index, 'Latitude'] = geocode_result[0]['geometry']['location']['lat']
    df.loc[index, 'Longitude'] = geocode_result[0]['geometry']['location']['lng']
  except IndexError as err:
    print('No geocode found for: ' + row['Incomplete Address'])
    error_rows.append([index, row])
    pass

pickle.dump(df, open('output/gun_violence.pickle', 'wb'))