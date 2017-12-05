import pandas as pd
import matplotlib.pyplot as plt
import itertools
import plotly.graph_objs as go
from plotly.offline import plot, iplot
import os
import shutil
import visualization as vs
import sys
import seaborn as sns


# Fill in below with proper paths:
#     download_path = Directory where browser downloads plots from plotly into
#     output_path = Directory where output files are stored
download_path = '/Users/jason.wang/Downloads/'
output_path = '/Users/jason.wang/Documents/Analytics Projects/Gun Control/output/'


sg_df = pd.read_csv('files/state_gender.txt', sep = '\t')

# * Filling DataFrame with all possible combinations of State, Year and Gender so we can infer some values
# later during aggregation by taking the average there is missing data. Marking columns that were previously missing
# so we can denote that on US map representation
# * Cleaning up some redundant columns. Removed some rows where data had not been collected yet
# Recalculating the rate per 100k
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

#Drop some useless data and left merge so we don't have missing keys on year and state
sg_df.drop(['Notes', 'Crude Rate','Gender Code', 'Year Code', 'State Code'], inplace = True, axis = 1)
sg_df = df1.merge(sg_df, how = 'left').fillna(0)

#Use District of Columbia to hold dummy data about the max Death value for each gender so
#colorbar in choropleth is consistent
sg_df.loc[(sg_df['State'] == 'District of Columbia') & (sg_df['Gender'] == 'Male'),['Deaths']]\
    = max(sg_df[sg_df['Gender'] == 'Male']['Deaths'])
sg_df.loc[(sg_df['State'] == 'District of Columbia') & (sg_df['Gender'] == 'Female'),['Deaths']]\
    = max(sg_df[sg_df['Gender'] == 'Female']['Deaths'])


sg_df['State Code'] = sg_df['State'].map(inverted)
sg_df.Year = sg_df.Year.astype(int).astype(str)
sg_df.Population = sg_df.Population.astype(float)

sg_df['Rate'] = (sg_df.Deaths/sg_df.Population) * 100000
sg_df['Missing'] = (sg_df['Deaths'] == 0)
sg_df = sg_df[['State', 'State Code', 'Year', 'Gender', 'Deaths', 'Population', 'Rate', 'Missing']]


#Analysis of trends
#Filter out any states that don't have complete data
#Calculate percent change in deaths since base year of 1999
temp = sg_df.groupby(['State', 'Gender']).filter(lambda x: x['Rate'].isnull().sum() < 1).copy()
temp = temp[temp['State'] != 'District of Columbia']
temp['Net Percent Change'] = temp.groupby(['State', 'Gender'])['Deaths'].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
temp['Rolling Percent Change'] = temp.groupby(['State', 'Gender'])['Deaths'].pct_change() * 100
trend_df = temp.sort_values(by = ['State', 'Gender', 'Year'])
print(temp)


#TODO: Need to rotate DataFrame (after filtering by gender) so each row is a state and every column is a different year
trend_df = trend_df[trend_df['Gender'] == 'Male']

matrix = trend_df.pivot(index = 'State', columns = 'Year', values = 'Net Percent Change')
plt.figure(figsize = (15,10))
p = sns.heatmap(data = matrix, annot = True, cmap = 'RdBu_r', fmt = '.1f')
p.set_xticklabels(p.get_xticklabels(), rotation = 90)
p.set_yticklabels(p.get_yticklabels(), rotation = 0)
plt.title('Percent Change in Firearm Deaths by State Compared to 1999')

plt.show()

sys.exit()

# Analysis by State, Year and Gender
year_list = list(sg_df['Year'].unique())
gender_list = ['Male' , 'Female']
split_gender = True
metric = 'Rate'
metric_dir = output_path + metric + '/'
gender_list = ['Female']
for year in year_list:
    if split_gender:
        for gender in gender_list:
            output_dir = metric_dir + gender + '/'
            vs.choropleth(sg_df, year, gender, metric, download_path, output_dir)
    else:
        output_dir = metric_dir + 'Combined/'
        vs.choropleth(sg_df, year, gender_list, metric, download_path, output_dir)