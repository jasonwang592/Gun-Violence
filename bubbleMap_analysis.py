import pandas as pd
import visualization as vs
import calendar
import sys
import plotly.graph_objs as go
import pickle
import geocoder
import os
from plotly.offline import plot, iplot


def generateBubbleMap(df, download_path, output_path, metric = 'Total', year = None, month = None):
  metric = metric.capitalize()
  try:
    if year == None and month == None:
      for year in list(df['Year'].unique()):
        for month in list(df['MonthName'].unique()):
          vs.bubbleMap(df, month, year, metric, download_path, output_path + 'BubbleMap/')
    else:
      vs.bubbleMap(df, month, year, metric, download_path, output_path + 'BubbleMap/')
  except KeyError as e:
    print("Metric not found. Please define metric as either 'Killed' or 'Injured'.")


if __name__ == '__main__':
  download_path = '/Users/jason.wang/Downloads/'
  output_path = '/Users/jason.wang/Documents/Analytics Projects/Gun Control/output/'

  #Load the pickled data that contains longitude/latitude information via Google maps API search
  if os.path.exists(output_path + 'gun_violence.pickle'):
    df = pickle.load(open(output_path + 'gun_violence.pickle','rb'))
  else:
    geocoder.generate_geolocations()
  df.rename(columns = {'# Killed':'Killed', '# Injured':'Injured'}, inplace = True)

  #Clean the data a bit and break out some new columns
  df['Incident Date'] = pd.to_datetime(df['Incident Date'])
  df['MonthYear'] = df['Incident Date'].apply(lambda x: x.strftime('%m/%Y'))
  df['Month'] = pd.DatetimeIndex(df['Incident Date']).month
  df['MonthName'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
  df['Year'] = df['Incident Date'].dt.strftime('%Y')
  df['Year'] = df['Year'].astype('str')
  df = df[['Incident Date', 'Year', 'Month', 'MonthName', 'MonthYear', 'City Or County', 'Full Address',\
    'Latitude', 'Longitude', 'Killed', 'Injured']]
  df['Total'] = df['Killed'] + df['Injured']

  #Create a new DataFrame grouped by Month and Year and sum up all statistics within
  monthyear_df = df.groupby(['Month', 'MonthName', 'Year'], as_index = False)[['Killed','Injured']].sum()
  monthyear_df = monthyear_df.sort_values(by = ['Year','Month'])

  #Generate choronological bubble maps of gun violence killings and injuries
  df = df.sort_values(by = ['Year','Month'])
  # metric = 'Killed'

  generateBubbleMap(df, download_path, output_path)
  # generateBubbleMap(df, download_path, output_path, year = 2017, month = 'Oct')
  sys.exit()

  #Generate histogram for all data
  vs.hist(df, download_path, output_path)

  #Generate stacked bar charts for each year illustrating metrics
  year_list = list(monthyear_df['Year'].unique())
  for year in year_list:
    vs.stackedBar(monthyear_df, year, download_path, output_path + 'EDA/')