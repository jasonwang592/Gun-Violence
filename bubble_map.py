import plotly.graph_objs as go
from plotly.offline import plot, iplot
import pandas as pd

def bubbleMap(df):
  df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'
  limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
  colors = ["rgb(0,116,217)","rgb(255,65,54)","rgb(133,20,75)","rgb(255,133,27)","lightgrey"]
  cities = []
  scale = 5000
