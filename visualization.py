import plotly.graph_objs as go
from plotly.offline import plot, iplot
import os
import pandas as pd
import shutil
import math
import time
import numpy as np
import calendar

def bubbleMap(df, month, year, metric, download_dir, output_dir):
  abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
  df = df[(df['Month'] == abbr_to_num[month]) & (df['Year'] == year)]
  df.is_copy = False
  df.loc[:, 'text'] = df['City Or County'] + '<br>' + (df[metric]).astype(str)
  df.loc[:,metric] = df[metric].astype(float)

  if metric == 'Injured' or 'Killed':
    limits = [(0,2),(3,5),(6,9),(10,25),(26,450)]
  else:
    limits = [(0,4),(5,6),(7,9),(10,50),(50,500)]
  scale = 100.

  colors = ['rgb(153,255,153)', 'rgb(255,133,27)', 'rgb(0,116,217)', 'rgb(255,112,102)', 'rgb(255,36,20)']
  locations = []
  for i in range(len(limits)):
    lim = limits[i]
    # df_sub = df[lim[0]:lim[1]]
    df_sub = df[(df[metric] >= lim[0]) & (df[metric] < lim[1])]
    location = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df_sub['Longitude'],
        lat = df_sub['Latitude'],
        text = df_sub['City Or County'],
        marker = dict(
            #TODO: Figure out some kind of mapping function to compress and stretch scale
            size = (df_sub[metric]) ** (1/2.) * 10,
            color = colors[i],
            line = dict(width = 0.5, color = 'rgb(40,40,40)'),
            sizemode = 'diameter',
            opacity = 0.6
        ),
        name = '{0} - {1}'.format(lim[0],lim[1]))
    locations.append(location)

  if metric == 'Injured':
    title = 'Gun Violence Injuries, 2014 - 2017' + '<br>' + ' '.join([month, year])
  elif metric == 'Killed':
    title = 'Gun Violence Injuries, 2014 - 2017' + '<br>' + ' '.join([month, year])
  else:
    title = 'Combined Gun Violence Injuries and Deaths, 2014 - 2017' + '<br>' + ' '.join([month, year])

  layout = dict(
        title = title,
        showlegend = True,
        geo = dict(
            scope = 'usa',
            projection = dict( type = 'albers usa' ),
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth = 1,
            countrywidth = 1,
            subunitcolor = "rgb(255, 255, 255)",
            countrycolor = "rgb(255, 255, 255)"
        ),
    )

  fig = dict(data = locations, layout = layout)

  fname =  ' '.join([year, str(abbr_to_num[month]), 'Bubble Map'])
  plot(fig, image_filename = fname, image = 'png', image_width = 1200, image_height = 1000)
  time.sleep(3)

  output_dir += metric + '/'
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  try:
    if os.path.exists(output_dir + fname + '.png'):
      shutil.move(download_dir + fname + '.png', output_dir + fname + '.png')
    else:
      shutil.move(download_dir + fname + '.png', output_dir)
  except FileNotFoundError as err:
    print('Graph not generated in time for: ' + fname + '. Run this bubble map separately.')


def hist(df, download_dir, output_dir, cutoff = None):
  '''Generates a histogram of injury and death counts

  Args:
    df            (DataFrame): DataFrame containing gun violence data
    download_dir  (str)      : String for download directory where to find images after Plotly generates them
    output_dir    (str)      : String for output directory for where to move images after generation
    cutoff        (int)      : If provided, cuts off number of injuries or deaths at the cutoff arg

  Raises:
    FileNotFoundError: If image file is not generated fast enough, file will not be found to move from
      download directory to output directory. Raises an error with message on what image failed to generate.
  '''

  if cutoff:
    df = df[(df['Killed'] < cutoff) & (df['Injured'] < cutoff)]
  x0 = df['Killed']
  x1 = df['Injured']

  trace0 = go.Histogram(
      x=x0,
      text = x0,
      name = 'Killed',
      opacity = 0.6
  )
  trace1 = go.Histogram(
      x=x1,
      text = x1,
      name = 'Injured',
      opacity = 0.6
  )

  data = [trace0, trace1]

  layout = go.Layout(
    barmode='stack',
    title = 'Injury and Death Frequency, Gun Violence 2014-2017',
    xaxis = dict(title = 'Number Injured or Killed',
      tick0 = 0,
      dtick = 1
      ),
    yaxis = dict(title = 'Number of Occurrences')
    )

  hist = go.Figure(data = data, layout = layout)

  fname = 'Injury and Death Histogram'
  if cutoff:
    fname = fname + ' cutoff at ' + str(cutoff)
  plot(hist, image_filename = fname, image = 'png', image_width = 1200, image_height = 1000)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  try:
    if os.path.exists(output_dir + fname + '.png'):
      shutil.move(download_dir + fname + '.png', output_dir + fname + '.png')
    else:
      shutil.move(download_dir + fname + '.png', output_dir)
  except FileNotFoundError as err:
    print('Graph not generated in time for: ' + fname + '. Run this histogram separately.')

def stackedBar(df, year, download_dir, output_dir):
  '''Takes a dataframe and then keeps the rows for the year argument and plots a stacked bar
  chart of the injuries and deaths in each month

  Args:
    df            (DataFrame): DataFrame containing pertinent information
    year          (str)    : Year string to filter DataFrame by
    download_dir  (str)      : String for download directory where to find images after Plotly generates them
    output_dir    (str)      : String for output directory for where to move images after generation

  Raises:
    FileNotFoundError: If image file is not generated fast enough, file will not be found to move from
      download directory to output directory. Raises an error with message on what image failed to generate.
  '''
  df = df[df['Year'] == year]
  x = list(df['MonthName'].unique())
  y = list(df['Killed'])
  y2 = list(df['Injured'])

  trace1 = go.Bar(
      x = x,
      y = y,
      text = y,
      name = 'Killed',
      textposition = 'auto',
      marker = dict(
          color ='rgb(158,202,225)',
          line = dict(
              color='rgb(8,48,107)',
              width=1.5),
          ),
      opacity = 0.6
  )

  trace2 = go.Bar(
      x = x,
      y = y2,
      text = y2,
      name = 'Injured',
      textposition = 'auto',
      marker = dict(
          color= 'rgb(58,200,225)',
          line = dict(
              color = 'rgb(8,48,107)',
              width = 1.5),
          ),
      opacity = 0.6
  )

  data = [trace1,trace2]
  layout = go.Layout(
    barmode='stack',
    title = 'Gun Violence Casualties in ' + str(year)
  )
  stackedbar = go.Figure(data = data, layout = layout)

  '''Plot the image and set a wait time so Plotly can generate the plot, save it and then move it to the
  correct output directory. If the process takes too long, increase the sleep time'''
  fname = 'Gun Violence Casualties in ' + str(year)
  plot(stackedbar, image_filename = fname, image = 'png', image_width = 1200, image_height = 1000)
  time.sleep(3)

  output_dir += 'StackedBar/'
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  try:
    if os.path.exists(output_dir + fname + '.png'):
      shutil.move(download_dir + fname + '.png', output_dir + fname + '.png')
    else:
      shutil.move(download_dir + fname + '.png', output_dir)
  except FileNotFoundError as err:
    print('Graph not generated in time for: ' + fname + '. Run this stacked bar chart separately.')

def choropleth(df, year, gender, metric_name, chart_title, bar_title, download_dir, output_dir, include_dc = False):
  '''Splits out dataframe based on filter criteria provided, plots the data on a choropleth via Plotly
  and then saves the image to the user's download directory before moving it to a specific output directory

  Args:
    df            (DataFrame): DataFrame containing relevant data
    year          (str)      : String representing year to filter the data on
    Gender        (list)     : List containing gender(s) to filter data on
    metric        (str)      : The relevant metric that is being plotted
    chart_title   (str)      : String containing chart title
    bar_title     (str)      : String containing colorbar title
    download_dir  (str)      : String for download directory where to find images after Plotly generates them
    output_dir    (str)      : String for output directory for where to move images after generation
    include_dc    (bool)     : Boolean to include DC or not since it introduces severe outliers

  Raises:
    FileNotFoundError: If image file is not generated fast enough, file will not be found to move from
      download directory to output directory. Raises an error with message on what image failed to generate.

  '''
  caption = []
  if include_dc:
    caption = [dict(text = '*Data includes District of Columbia',
              showarrow=False,
              xref="paper", yref="paper",
              x=0.005, y=0.05),
              dict(text = 'DC Death Rate per 100k: ' + str(round(df[df['State Code'] == 'DC']['Rate'].values[0], 2)),
              showarrow=False,
              xref="paper", yref="paper",
              x=0.005, y=0.025)]
  elif not include_dc and metric_name == 'Rate':
    df.loc[(df['State Code'] == 'DC') & (df['Gender'] == gender), ['Rate']] = max(df[(df['State Code'] != 'DC') & (df['Gender'] == gender)]['Rate'])
  else:
    df = df[df['State Code'] != 'DC']

  year = str(year)
  if isinstance(gender, str):
    gender = gender.split()

  #Filter out gender and then build a consistent array for ticks for each gender
  df = df.loc[df['Gender'].isin(gender)]
  if metric_name == 'Deaths':
    tickarray = np.linspace(0, np.nanmax(df['Rate'].values), 11, dtype = int, endpoint = True)
  else:
    tickarray = np.linspace(0, np.nanmax(df['Rate'].values), 11, dtype = float, endpoint = True)
  ticklabs = [str(round(num,1)) for num in tickarray]

  df = df.loc[df['Year'] == year]
  df = df[pd.notnull(df[metric_name])]

  if isinstance(gender, list):
    df = df.groupby('State Code', as_index = False)[[metric_name]].sum()

  scl = [(0.0, 'rgb(254,240,217)'), (0.2, 'rgb(253,212,158)'), (0.4, 'rgb(253,187,132)'),\
      (0.6, 'rgb(252,141,89)'), (0.8, 'rgb(227,74,51)'), (1.0, 'rgb(196, 53, 31)')]

  data = dict(type='choropleth',
      locations = df['State Code'],
      locationmode ='USA-states',
      z = df[metric_name].astype(float),
      colorscale = scl,
      autocolorscale = False,
      colorbar = dict(
        title = bar_title,
        tickmode = 'array',
        tickvals = tickarray,
        ticktext = ticklabs,
        )
      )

  layout = dict(
      geo = dict(scope='usa', projection = dict(type = 'albers usa'),
      showlakes= False, landcolor = 'rgb(213, 213, 211)'),
      title = chart_title,
      annotations = caption
      )

  choromap = go.Figure(data = [data], layout = layout)

  if len(gender) == 1:
      fname = ' '.join(filter(None, [year, gender[0], metric_name]))
  else:
      fname = ' '.join(filter(None, [year, metric_name]))

  '''Plot the image and set a wait time so Plotly can generate the plot, save it and then move it to the
  correct output directory. If the process takes too long, increase the sleep time'''
  plot(choromap, image_filename = fname, image = 'png', image_width = 1200, image_height = 1000)
  time.sleep(2)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  try:
    if os.path.exists(output_dir + fname + '.png'):
      shutil.move(download_dir + fname + '.png', output_dir + fname + '.png')
    else:
      shutil.move(download_dir + fname + '.png', output_dir)
  except FileNotFoundError as err:
    print('Graph not generated in time for: ' + fname + '. Run this choropleth for this separately.')
