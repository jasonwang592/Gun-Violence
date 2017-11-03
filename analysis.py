import pandas as pd
import matplotlib.pyplot as plt
import itertools
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import os
import shutil

download_path = '/Users/jason.wang/Downloads/'
output_path = '/Users/jason.wang/Documents/Analytics Projects/Gun Control/output/'


sg_df = pd.read_csv('files/state_gender.txt', sep = '\t')
sga_df = pd.read_csv('files/state_gender_age.txt', sep = '\t')

'''
* Filling DataFrame with all possible combinations of State, Year and Gender so we can infer some values
later during aggregation by taking the average there is missing data. Marking columns that were previously missing
so we can denote that on US map representation
* Cleaning up some redundant columns. Removed some rows where data had not been collected yet
Recalculating the rate per 100k
'''
all_years = [1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
all_genders = ['Male', 'Female']
all_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
	'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky',
	'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
	'Nevada', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
	'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
state_map = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
inverted = {state:abbrev for abbrev,state in state_map.items()}
combined = [all_states, all_years, all_genders]
df1 = pd.DataFrame(columns = ['State', 'Year', 'Gender'], data=list(itertools.product(*combined)))

sg_df.drop(['Notes', 'Crude Rate','Gender Code', 'Year Code', 'State Code'], inplace = True, axis = 1)
sga_df.drop(['Notes', 'Crude Rate', 'Ten-Year Age Groups', 'Gender Code', 'Year Code', 'State Code'],
	inplace = True, axis = 1)

sga_df.rename(columns = {'Ten-Year Age Groups Code': 'Age Group'}, inplace = True)
sg_df = df1.merge(sg_df, how = 'left').fillna(0)
sg_df['State Code'] = sg_df['State'].map(inverted)
sg_df.Year = sg_df.Year.astype(int).astype(str)
sg_df.Population = sg_df.Population.astype(float)
sga_df.Year = sga_df.Year.astype(int).astype(str)
sga_df.Population = sga_df.Population.astype(float)

sga_df['Rate'] = (sga_df.Deaths/sga_df.Population) * 100000
sg_df['Rate'] = (sg_df.Deaths/sg_df.Population) * 100000
sg_df['Missing'] = sg_df['Deaths'] == 0
sg_df = sg_df[['State', 'State Code', 'Year', 'Gender', 'Deaths', 'Population', 'Rate', 'Missing']]


'''Analysis by State, Year and Gender'''
# state_df = sg_df.groupby(['State','Year']).sum()
# print(state_df)
sg_df = sg_df.loc[(sg_df['Year'] == '1999') & (sg_df['Gender'] == 'Male')]
print(sg_df)


scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
            [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

data = dict(type='choropleth',
            locations = sg_df['State Code'],
            locationmode ='USA-states',
            z = sg_df['Deaths'].astype(int),
			colorscale = scl,
			autocolorscale = False,
            colorbar = dict(title = 'Firearm Deaths per 100K')
            )

layout = dict(
		geo = dict(scope='usa', projection = dict(type = 'albers usa'),
					showlakes= False),
		title = 'Firearm Deaths by State in' + year,
             )

choromap = go.Figure(data=[data], layout=layout)
fname = 'test'
plot(choromap, image_filename = 'test', image_width = 1200, image_height = 1000)
# shutil.move(download_path + fname + '.png', output_path + fname + '.png')










