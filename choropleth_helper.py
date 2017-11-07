import plotly.graph_objs as go
from plotly.offline import plot, iplot
import os
import shutil
import time

def choropleth(df, year, gender, metric_name, chart_title, bar_title, download_dir, output_dir):
    year = str(year)
    gender = gender.split()
    df = df.loc[(df['Year'] == year) & (df['Gender'].isin(gender))]
    print(df)

    scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
        [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

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
        showlakes= False),
        title = chart_title,
        )

    choromap = go.Figure(data=[data], layout=layout)
    if len(gender) == 1:
        fname = ' '.join(filter(None, [year, gender[0], metric_name]))
    else:
        fname = ' '.join(filter(None, [year, metric_name]))

    plot(choromap, image_filename = fname, image = 'png', image_width = 1200, image_height = 1000)
    time.sleep(3)
    if os.path.exists(output_dir + fname + '.png'):
        shutil.move(download_dir + fname + '.png', output_dir + fname + '.png')
    else:
        shutil.move(download_dir + fname + '.png', output_dir)