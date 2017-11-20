import pandas as pd
import visualization as vs
import calendar
import sys
import plotly.graph_objs as go
from plotly.offline import plot, iplot

download_path = '/Users/jason.wang/Downloads/'
output_path = '/Users/jason.wang/Documents/Analytics Projects/Gun Control/output/'
df = pd.read_csv('files/GunViolence.csv')

#Clean the data a bit and break out some new columns
df['Incident Date'] = pd.to_datetime(df['Incident Date'])
df['MonthYear'] = df['Incident Date'].apply(lambda x: x.strftime('%m/%Y'))
df['Month'] = pd.DatetimeIndex(df['Incident Date']).month
df['MonthName'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
df['Year'] = pd.DatetimeIndex(df['Incident Date']).year
df = df[['Incident Date', 'Year', 'Month', 'MonthName', 'MonthYear', 'City Or County', 'Address', 'Killed', 'Injured']]
df['Total'] = df['Killed'] + df['Injured']

#Create a new DataFrame grouped by Month and Year and sum up all statistics within
monthyear_df = df.groupby(['Month', 'MonthName', 'Year'], as_index = False)[['Killed','Injured']].sum()
monthyear_df = monthyear_df.sort_values(by = ['Year','Month'])

#Generate histogram for all data
vs.hist(df, download_path, output_path)
sys.exit()

#Generate stacked bar charts for each year illustrating metrics
year_list = list(monthyear_df['Year'].unique())
output_dir = output_path + 'EDA/'
for year in year_list:
  vs.stackedBar(monthyear_df, year, download_path, output_dir)