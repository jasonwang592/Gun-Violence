import pandas as pd
import visualization

df = pd.read_csv('files/GunViolence.csv')
df['Incident Date'] = pd.to_datetime(df['Incident Date'])
df['MonthYear'] = df['Incident Date'].apply(lambda x: x.strftime('%m/%Y'))
df['Month'] = pd.DatetimeIndex(df['Incident Date']).month
df['Year'] = pd.DatetimeIndex(df['Incident Date']).year
df = df[['Incident Date', 'Year', 'Month', 'MonthYear', 'City Or County', 'Address', 'Killed', 'Injured']]
df['Total'] = df['Killed'] + df['Injured']


monthyear_df = df.groupby(['Month','Year'], as_index = False)[['Killed','Injured']].sum()
monthyear_df = monthyear_df.sort_values(by = ['Year','Month'])
print(monthyear_df)