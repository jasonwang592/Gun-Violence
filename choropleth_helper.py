import plotly.graph_objs as go
from plotly.offline import plot, iplot
import os
import pandas as pd
import shutil
import time

def choropleth(df, year, gender, metric_name, chart_title, bar_title, download_dir, output_dir):
  year = str(year)
  if isinstance(gender, str):
    gender = gender.split()
  df = df.loc[(df['Year'] == year) & (df['Gender'].isin(gender))]
  df = df[pd.notnull(df[metric_name])]

  if isinstance(gender, list):
    df = df.groupby('State Code', as_index = False)[[metric_name]].sum()

  scl = [(0.0, 'rgb(254,240,217)'), (0.2, 'rgb(253,212,158)'), (0.4, 'rgb(253,187,132)'),\
      (0.6, 'rgb(252,141,89)'), (0.8, 'rgb(227,74,51)'), (1.0, 'rgb(196, 53, 31)')]

  data = dict(type='choropleth',
      locations = df['State Code'],
      locationmode ='USA-states',
      z = df[metric_name].astype(int),
      colorscale = scl,
      autocolorscale = False,
      colorbar = dict(title = bar_title)
      )

  layout = dict(
      geo = dict(scope='usa', projection = dict(type = 'albers usa'),
      showlakes= False, landcolor = 'rgb(213, 213, 211)'),
      title = chart_title,
      )

  choromap = go.Figure(data=[data], layout=layout)
  if len(gender) == 1:
      fname = ' '.join(filter(None, [year, gender[0], metric_name]))
  else:
      fname = ' '.join(filter(None, [year, metric_name]))

  '''Plot the image and set a wait time so Plotly can generate the plot, save it and then move it to the
  correct output directory. If the process takes too long, increase the sleep time'''
  plot(choromap, image_filename = fname, image = 'png', image_width = 1200, image_height = 1000)
  time.sleep(3)

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  try:
    if os.path.exists(output_dir + fname + '.png'):
      shutil.move(download_dir + fname + '.png', output_dir + fname + '.png')
    else:
      shutil.move(download_dir + fname + '.png', output_dir)
  except FileNotFoundError as err:
    print('Graph not generated in time for: ' + fname + '. Run this choropleth for this separately.')
